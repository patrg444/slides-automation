import { NextResponse } from 'next/server';
import { headers } from 'next/headers';
import { db } from '@/db';
import {
  caseStudies,
  caseStudyFiles,
  caseStudyFileStatus,
  caseStudyImages
} from '@/db/schema';
import { eq } from 'drizzle-orm';
import { supabaseServer } from '@/lib/supabaseServer';

// You should store this in environment variables
const WEBHOOK_SECRET = process.env.MARKER_WEBHOOK_SECRET;

interface MarkerResponse {
  output_format: string;
  markdown: string;
  status: string;
  success: boolean;
  images: Record<string, string>;
  metadata: Record<string, any>;
  error: string;
  page_count: number;
}

async function validateWebhook(request: Request) {
  const body = await request.json();
  console.log('Received webhook body:', body);
  const { request_id, request_check_url, webhook_secret } = body;

  console.log('Received webhook secret:', webhook_secret);
  console.log('Expected webhook secret:', WEBHOOK_SECRET);

  if (!webhook_secret || webhook_secret !== WEBHOOK_SECRET) {
    throw new Error('Invalid webhook secret');
  }

  if (!request_id || !request_check_url) {
    throw new Error('Missing required fields');
  }

  return { request_id, request_check_url };
}

async function fetchMarkerResults(
  requestCheckUrl: string
): Promise<MarkerResponse> {
  const response = await fetch(requestCheckUrl, {
    headers: {
      'X-Api-Key': process.env.MARKER_API_KEY || ''
    }
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch results: ${response.statusText}`);
  }

  const result: MarkerResponse = await response.json();
  if (!result.success) {
    throw new Error(result.error || 'Processing failed');
  }

  return result;
}

async function updateCaseStudyFile(requestId: string, result: MarkerResponse) {
  const caseStudyFile = await db
    .update(caseStudyFiles)
    .set({
      status: result.status as (typeof caseStudyFileStatus)[number],
      markdown: result.markdown,
      metadata: result.metadata,
      error: result.error
    })
    .where(eq(caseStudyFiles.request_id, requestId))
    .returning();

  if (!caseStudyFile?.length) {
    throw new Error('Case study file not found');
  }

  return caseStudyFile[0];
}

async function processImages(caseStudyFile: any, result: MarkerResponse) {
  if (!result.images || Object.keys(result.images).length === 0) {
    return;
  }

  const caseStudy = await db
    .select()
    .from(caseStudies)
    .where(eq(caseStudies.id, caseStudyFile.case_study_id))
    .then(([result]) => result);

  if (!caseStudy) {
    throw new Error('Case study not found');
  }

  const userId = caseStudy.user_id;
  for (const [filename, imageBase64] of Object.entries(result.images)) {
    try {
      const imageBuffer = Buffer.from(imageBase64, 'base64');
      const filePath = `${userId}/case_studies/${caseStudyFile.id}/images/${filename}`;

      const { error: uploadError } = await supabaseServer.storage
        .from('files')
        .upload(filePath, imageBuffer, {
          contentType: 'image/jpeg',
          cacheControl: '3600',
          upsert: false
        });

      if (uploadError) {
        console.error(`Failed to upload image ${filename}:`, uploadError);
        continue;
      }

      const {
        data: { publicUrl }
      } = supabaseServer.storage.from('files').getPublicUrl(filePath);

      await db.insert(caseStudyImages).values({
        file_id: caseStudyFile.id,
        image_url: publicUrl
      });
    } catch (error) {
      console.error(`Error processing image ${filename}:`, error);
    }
  }
}

export async function POST(request: Request) {
  try {
    console.log('Processing webhook: ', request);

    const { request_id, request_check_url } = await validateWebhook(request);
    console.log('Validated webhook data:', { request_id, request_check_url });

    const result = await fetchMarkerResults(request_check_url);
    console.log('Marker results:', result);

    console.log(`Processing completed for request: ${request_id}`);
    console.log(`Status: ${result.status}, Page count: ${result.page_count}`);

    const caseStudyFile = await updateCaseStudyFile(request_id, result);
    console.log('Updated case study file:', caseStudyFile);

    // todo: save markdown to storage
    await processImages(caseStudyFile, result);

    return NextResponse.json(
      { message: 'Webhook processed successfully' },
      { status: 200 }
    );
  } catch (error: unknown) {
    console.error('Error processing webhook:', error);

    let status = 500;
    let errorMessage = 'Internal server error';

    if (error instanceof Error) {
      errorMessage = error.message;
      if (errorMessage.includes('Invalid webhook secret')) {
        status = 401;
      } else if (errorMessage.includes('Missing required fields')) {
        status = 400;
      }
    }

    return NextResponse.json({ error: errorMessage }, { status });
  }
}

export async function GET(request: Request) {
  try {
    // Log request details for debugging
    console.log('Test GET request received');
    console.log('Request URL:', request.url);
    console.log('Request method:', request.method);
    console.log(
      'Request headers:',
      Object.fromEntries(request.headers.entries())
    );

    return NextResponse.json(
      {
        message: 'Webhook endpoint is active',
        status: 'operational',
        timestamp: new Date().toISOString()
      },
      { status: 200 }
    );
  } catch (error: unknown) {
    console.error('Error in GET request:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

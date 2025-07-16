'use server';

import { CaseStudy } from '@/types';
import { db } from '@/db';
import { caseStudies, caseStudyFiles } from '@/db/schema';
import { auth } from '@clerk/nextjs/server';
import { downloadFileFromUrl } from '@/utils/file';
import { MarkerApiResponse } from '@/types/marker';

async function processFileWithMarker(file: {
  blob: Blob;
  name: string;
}): Promise<MarkerApiResponse> {
  const formData = new FormData();
  formData.append('file', file.blob, file.name);
  formData.append('langs', 'English');
  formData.append('force_ocr', 'false');
  formData.append('paginate', 'false');
  formData.append('output_format', 'markdown');
  formData.append('use_llm', 'false');
  formData.append('strip_existing_ocr', 'false');
  formData.append('disable_image_extraction', 'false');

  const response = await fetch('https://www.datalab.to/api/v1/marker', {
    method: 'POST',
    headers: {
      'X-Api-Key': process.env.MARKER_API_KEY || ''
    },
    body: formData
  });

  if (!response.ok) {
    throw new Error(`Marker API error: ${response.statusText}`);
  }

  const result = (await response.json()) as MarkerApiResponse;

  if (!result.success) {
    throw new Error(`Marker API error: ${result.error}`);
  }

  return result;
}

export async function createCaseStudy(caseStudy: {
  title: string;
  client: string | null;
  industry: string | null;
  fileUrls: string[];
}): Promise<CaseStudy> {
  const { userId } = await auth();
  if (!userId) throw new Error('User not authenticated');

  // Create case study record
  const [newCaseStudy] = await db
    .insert(caseStudies)
    .values({ user_id: userId, ...caseStudy })
    .returning();

  if (!newCaseStudy) {
    throw new Error(
      'Failed to create case study: No record returned from database'
    );
  }

  await Promise.allSettled(
    caseStudy.fileUrls.map(async (fileUrl) => {
      try {
        const file = await downloadFileFromUrl(fileUrl);
        const result = await processFileWithMarker(file);

        await db.insert(caseStudyFiles).values({
          case_study_id: newCaseStudy.id,
          request_id: result.request_id,
          file_url: fileUrl,
          status: 'processing',
          metadata: result
        });
      } catch (error) {
        console.error(`Error processing file ${fileUrl}:`, error);
      }
    })
  );

  return newCaseStudy;
}

'use server';

import {
  createPartFromText,
  createUserContent,
  GoogleGenAI,
  Type
} from '@google/genai';
import { auth } from '@clerk/nextjs/server';
import { db } from '@/db';
import { caseStudySummaries } from '@/db/schema';
import { CaseStudySummary } from '@/types';

const DEFAULT_MODEL = 'gemini-2.5-flash-preview-04-17';

const SYSTEM_PROMPT = `
As a professional summarizer, create a concise and comprehensive summary of the provided file while adhering to these guidelines:
- Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness.
- Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
- Rely strictly on the provided text, without including external information.
- Format the summary in paragraph form for easy understanding.

The output should be a professional case study with these sections in markdown format:
  - Title: The title of the case study
  - Challenge: Describe the key problems or challenges faced
  - Approach: How the challenge was addressed
  - Solution: The implemented solution
  - Outcomes: Results and benefits achieved
  - Summary: A brief executive summary
  - Key Points: A list of key points
`;

export async function createOnePager(
  fileContent: string,
  caseStudyId: string
): Promise<CaseStudySummary> {
  console.log(
    `[createOnePager] Starting process for case study ID: ${caseStudyId}`
  );
  const { userId } = await auth();
  if (!userId) throw new Error('User not authenticated');
  console.log(`[createOnePager] User authenticated: ${userId}`);

  console.log(`[createOnePager] Calling Gemini API for text completion`);
  const response = await geminiTextCompletion(fileContent);
  console.log(`[createOnePager] Received response from Gemini API`);

  console.log(`[createOnePager] Inserting summary into database`);
  const [summary] = await db
    .insert(caseStudySummaries)
    .values({
      case_study_id: caseStudyId,
      summary: response
    })
    .returning();
  console.log(
    `[createOnePager] Successfully inserted summary with ID: ${summary.id}`
  );

  return summary;
}

async function geminiTextCompletion(
  fileContent: string,
  model: string = DEFAULT_MODEL
): Promise<string> {
  console.log(`[geminiTextCompletion] Starting with model: ${model}`);
  const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
  if (!GEMINI_API_KEY) {
    console.error('[geminiTextCompletion] Missing GEMINI_API_KEY');
    throw new Error('GEMINI_API_KEY is not set in environment variables.');
  }

  const ai = new GoogleGenAI({ apiKey: GEMINI_API_KEY, vertexai: false });

  try {
    console.log(`[geminiTextCompletion] Sending request to Gemini API`);
    const response = await ai.models.generateContent({
      model: model,
      contents: fileContent,
      config: {
        systemInstruction: SYSTEM_PROMPT
      }
    });

    if (!response.text) {
      console.error(
        '[geminiTextCompletion] No text response received from Gemini'
      );
      throw new Error('[Gemini] No text response received from Gemini');
    }

    console.log(
      `[geminiTextCompletion] Successfully received response from Gemini`
    );
    return response.text;
  } catch (error) {
    console.error(`[geminiTextCompletion] Error:`, error);
    throw error;
  }
}

async function geminiJSONCompletion(
  fileContent: string,
  model: string = DEFAULT_MODEL
): Promise<string> {
  console.log(`[geminiJSONCompletion] Starting with model: ${model}`);
  const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
  if (!GEMINI_API_KEY) {
    console.error('[geminiJSONCompletion] Missing GEMINI_API_KEY');
    throw new Error('GEMINI_API_KEY is not set in environment variables.');
  }

  const ai = new GoogleGenAI({ apiKey: GEMINI_API_KEY, vertexai: false });

  try {
    console.log(`[geminiJSONCompletion] Sending request to Gemini API`);
    const response = await ai.models.generateContent({
      model: model,
      contents: [
        createUserContent([SYSTEM_PROMPT, createPartFromText(fileContent)])
      ],
      config: {
        responseMimeType: 'application/json',
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            title: { type: Type.STRING },
            challenge: { type: Type.STRING },
            approach: { type: Type.STRING },
            solution: { type: Type.STRING },
            outcomes: { type: Type.STRING },
            summary: { type: Type.STRING },
            key_points: {
              type: Type.ARRAY,
              items: { type: Type.STRING }
            }
          },
          propertyOrdering: [
            'title',
            'challenge',
            'approach',
            'solution',
            'outcomes',
            'summary',
            'key_points'
          ]
        }
      }
    });

    if (!response.text) {
      console.error(
        '[geminiJSONCompletion] No text response received from Gemini'
      );
      throw new Error('No text response received from Gemini');
    }

    console.log(
      `[geminiJSONCompletion] Successfully received response from Gemini`
    );
    return response.text;
  } catch (error) {
    console.error(`[geminiJSONCompletion] Error:`, error);
    throw error;
  }
}

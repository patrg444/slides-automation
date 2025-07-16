'use server';

import {
  CaseStudy,
  CaseStudyData,
  CaseStudyFile,
  CaseStudyImage,
  CaseStudySummary,
  CaseStudyWithFiles
} from '@/types';
import { db } from '@/db';
import {
  caseStudies,
  caseStudyFiles,
  caseStudyImages,
  caseStudySummaries
} from '@/db/schema';
import { auth } from '@clerk/nextjs/server';
import { desc, eq, inArray } from 'drizzle-orm';

export async function getAllCaseStudies(): Promise<CaseStudy[]> {
  const { userId } = await auth();
  if (!userId) throw new Error('User not authenticated');

  return db
    .select()
    .from(caseStudies)
    .where(eq(caseStudies.user_id, userId))
    .orderBy(desc(caseStudies.created_at))
    .then((result) => {
      return result;
    });
}

export async function getCaseStudyById(
  id: string
): Promise<CaseStudyWithFiles> {
  // Step 1: Fetch the case study
  const caseStudy = await db
    .select()
    .from(caseStudies)
    .where(eq(caseStudies.id, id))
    .then(([result]) => result);

  if (!caseStudy) {
    throw new Error('Case study not found');
  }

  // Step 2: Fetch all files for the case study
  const files = await db
    .select()
    .from(caseStudyFiles)
    .where(eq(caseStudyFiles.case_study_id, id));

  const summaries = await db
    .select()
    .from(caseStudySummaries)
    .where(eq(caseStudySummaries.case_study_id, id));

  if (files.length === 0) {
    return {
      ...caseStudy,
      files: [],
      summaries: []
    };
  }

  // Step 3: Fetch all images in *one query* for all file IDs
  const fileIds = files.map((file) => file.id);
  const images = await db
    .select()
    .from(caseStudyImages)
    .where(inArray(caseStudyImages.file_id, fileIds));

  // Step 4: Group images by file_id for quick lookup
  const imageMap = new Map<string, CaseStudyImage[]>();
  for (const image of images) {
    if (!imageMap.has(image.file_id)) {
      imageMap.set(image.file_id, []);
    }
    imageMap.get(image.file_id)!.push(image);
  }

  // Step 5: Attach images to corresponding files
  const filesWithImages = files.map((file) => ({
    ...file,
    metadata: file.metadata as Record<string, any> | null,
    images: imageMap.get(file.id) || []
  }));

  // Step 6: Return final nested object
  return {
    ...caseStudy,
    files: filesWithImages,
    summaries
  };
}

export async function saveCaseStudy(id: string, content: CaseStudyData) {
  const { userId } = await auth();
  if (!userId) throw new Error('User not authenticated');

  try {
    await db
      .update(caseStudies)
      .set({ description: content.summary })
      .where(eq(caseStudies.id, id));
    return true;
  } catch (error) {
    throw new Error('Failed to save case study');
  }
}

export async function deleteCaseStudy(id: string) {
  const { userId } = await auth();
  if (!userId) throw new Error('User not authenticated');

  try {
    await db.delete(caseStudies).where(eq(caseStudies.id, id));
    return true;
  } catch (error) {
    throw new Error('Failed to delete case study');
  }
}

export async function getCaseStudySummary(
  id: string
): Promise<CaseStudySummary> {
  const { userId } = await auth();
  if (!userId) throw new Error('User not authenticated');

  const caseStudy = await db
    .select()
    .from(caseStudySummaries)
    .where(eq(caseStudySummaries.case_study_id, id))
    .then(([result]) => result);

  if (!caseStudy) {
    throw new Error('Case study summary not found');
  }

  return caseStudy;
}

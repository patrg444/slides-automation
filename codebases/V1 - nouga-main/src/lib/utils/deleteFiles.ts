import { createSupabaseClient } from '@/lib/supabaseClient';

/**
 * Deletes files from a Supabase storage bucket.
 * @param filePaths Array of file paths (including folder if any, e.g. 'folder/file.png')
 * @param bucketName Name of the bucket (default: 'files')
 * @returns Promise<void>
 */
export const deleteFiles = async (
  sessionToken: string,
  filePaths: string[],
  bucketName: string = 'files'
): Promise<void> => {
  const supabaseClient = createSupabaseClient(sessionToken);
  const { error } = await supabaseClient.storage
    .from(bucketName)
    .remove(filePaths);

  if (error) {
    throw new Error(`Failed to delete files: ${error.message}`);
  }
};

// utils/uploadFiles.ts
import { createSupabaseClient } from '@/lib/supabaseClient';

export const uploadFile = async (
  sessionToken: string,
  file: File,
  filePath: string,
  bucketName: string = 'files'
): Promise<string> => {
  const supabaseClient = createSupabaseClient(sessionToken);

  const { error } = await supabaseClient.storage
    .from(bucketName)
    .upload(filePath, file, {
      cacheControl: '3600',
      upsert: false
    });

  if (error) {
    throw new Error(`Failed to upload ${file.name}: ${error.message}`);
  }

  const { data: publicUrlData } = supabaseClient.storage
    .from(bucketName)
    .getPublicUrl(filePath);

  return publicUrlData.publicUrl;
};

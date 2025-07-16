export async function downloadFileFromUrl(
  url: string
): Promise<{ blob: Blob; type: string; name: string }> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(
        `Failed to download file from ${url}: ${response.statusText}`
      );
    }

    const contentType =
      response.headers.get('content-type') || 'application/octet-stream';
    let name = url.split('/').pop() || 'file';

    try {
      const blob = await response.blob();
      return { blob, type: contentType, name };
    } catch (blobError) {
      throw new Error(
        `Failed to convert response to blob: ${
          blobError instanceof Error ? blobError.message : 'Unknown error'
        }`
      );
    }
  } catch (error) {
    throw new Error(
      `Error downloading file: ${
        error instanceof Error ? error.message : 'Unknown error'
      }`
    );
  }
}

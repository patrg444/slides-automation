import * as pdfjsLib from 'pdfjs-dist';
import type { TextItem } from 'pdfjs-dist/types/src/display/api';

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url
).href;

/**
 * Extracts text content from all PDF files in the provided array.
 * @param files Array of File objects (from input[type="file"])
 * @returns Promise resolving to an array of extracted text strings (one per PDF file)
 */
export async function processFiles(files: File[]): Promise<string[]> {
  const pdfFiles = files.filter((file) => file.type === 'application/pdf');

  const results = await Promise.all(
    pdfFiles.map(async (file) => {
      const arrayBuffer = await file.arrayBuffer();
      const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;

      const pageTexts = await Promise.all(
        Array.from({ length: pdf.numPages }, async (_, i) => {
          const page = await pdf.getPage(i + 1);
          const content = await page.getTextContent();
          return (content.items as TextItem[])
            .map((item) => item.str)
            .join(' ');
        })
      );

      return pageTexts.join(' ');
    })
  );

  return results;
}

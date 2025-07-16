'use client';

import { Button } from '@/components/ui/button';
import {
  FileUpload,
  FileUploadDropzone,
  FileUploadItem,
  FileUploadItemDelete,
  FileUploadItemMetadata,
  FileUploadItemPreview,
  FileUploadList,
  FileUploadTrigger
} from '@/components/ui/file-upload';
import { Upload, X } from 'lucide-react';
import { useCallback, useState } from 'react';
import { toast } from 'sonner';
import { FileWithStatus } from '@/types';
import { uploadFile } from '@/lib/utils/uploadFiles';
import { deleteFiles } from '@/lib/utils/deleteFiles';
import { useSession } from '@clerk/nextjs';
import SpinnerCircle from '../ui/spinner';

type FileUploadInputProps = {
  uploadedFiles: FileWithStatus[];
  setUploadedFiles: React.Dispatch<React.SetStateAction<FileWithStatus[]>>;
};

export function FileUploadInput({
  uploadedFiles,
  setUploadedFiles
}: FileUploadInputProps) {
  const [files, setFiles] = useState<File[]>([]);
  const { session } = useSession();

  const onUpload = (files: File[]) => {
    files.forEach(async (file) => {
      const fileWithStatus: FileWithStatus = {
        name: file.name,
        filePath: '',
        content: file,
        status: 'uploading',
        url: undefined,
        error: undefined
      };

      // Add file to uploadedFiles as uploading
      setUploadedFiles((prev) => [...prev, fileWithStatus]);

      try {
        const token = await session?.getToken();
        const userId = session?.user.id;
        if (!token || !userId) {
          throw new Error('No token or user id found');
        }

        const filePath = `${userId}/files/${file.name}`;
        const url = await uploadFile(token, file, filePath);

        // Update file status to success and set URL
        setUploadedFiles((prev) =>
          prev.map((f) =>
            f.name === file.name && f.status === 'uploading'
              ? { ...f, status: 'success', url, filePath }
              : f
          )
        );
      } catch (error) {
        // Update file status to error and set error message
        setUploadedFiles((prev) =>
          prev.map((f) =>
            f.name === file.name && f.status === 'uploading'
              ? {
                  ...f,
                  status: 'error',
                  error:
                    error instanceof Error ? error.message : 'Unknown error'
                }
              : f
          )
        );
      }
    });
  };

  const onDelete = async (file: FileWithStatus) => {
    const token = await session?.getToken();
    if (!token) {
      toast.error('No token found');
      return;
    }
    try {
      setUploadedFiles((prev) => prev.filter((f) => f.name !== file.name));
      await deleteFiles(token, [file.filePath]);
      toast.success('File deleted successfully');
    } catch (error) {
      toast.error('Failed to delete file');
    }
  };

  const onFileValidate = useCallback(
    (file: File): string | null => {
      // Validate max files
      if (files.length >= 10) {
        return 'You can only upload up to 10 files';
      }

      // Check for duplicates in uploadedFiles
      if (
        uploadedFiles.some(
          (f) => f.name === file.name && f.content.size === file.size
        )
      ) {
        return 'This file has already been selected';
      }

      // Validate file size (max 100MB)
      const MAX_SIZE = 100 * 1024 * 1024; // 100MB
      if (file.size > MAX_SIZE) {
        return `File size must be less than ${MAX_SIZE / (1024 * 1024)}MB`;
      }

      // Validate file type (only images, PDF, and Markdown (.md) files)
      if (
        !(
          file.type.startsWith('image/') ||
          file.type === 'application/pdf' ||
          file.name.toLowerCase().endsWith('.md')
        )
      ) {
        return 'Only image, PDF, and Markdown (.md) files are allowed';
      }

      return null;
    },
    [files, uploadedFiles]
  );

  const onFileReject = useCallback((file: File, message: string) => {
    toast(message, {
      description: `"${file.name.length > 20 ? `${file.name.slice(0, 20)}...` : file.name}" has been rejected`
    });
  }, []);

  return (
    <FileUpload
      value={files}
      onValueChange={setFiles}
      onFileValidate={onFileValidate}
      onFileReject={onFileReject}
      onUpload={onUpload}
      maxFiles={10}
      className='w-full'
      multiple
    >
      <FileUploadDropzone>
        <div className='flex flex-col items-center gap-1'>
          <div className='flex items-center justify-center rounded-full border p-2.5'>
            <Upload className='text-muted-foreground size-6' />
          </div>
          <p className='text-sm font-medium'>Drag & drop files here</p>
          <p className='text-muted-foreground text-xs'>
            Or click to browse (max 10 files, each file must be less than 100MB)
          </p>
        </div>
        <FileUploadTrigger asChild>
          <Button variant='outline' size='sm' className='mt-2 w-fit'>
            Browse files
          </Button>
        </FileUploadTrigger>
      </FileUploadDropzone>
      <FileUploadList>
        {uploadedFiles.map((file) => (
          <FileUploadItem
            key={file.name}
            value={file.content}
            className={
              file.status === 'uploading'
                ? 'pointer-events-none opacity-50'
                : ''
            }
          >
            <FileUploadItemPreview />
            <FileUploadItemMetadata />
            {file.status === 'uploading' && <SpinnerCircle />}
            <FileUploadItemDelete asChild>
              <Button
                variant='ghost'
                size='icon'
                className='size-7'
                disabled={file.status === 'uploading'}
                onClick={() => onDelete(file)}
              >
                <X />
              </Button>
            </FileUploadItemDelete>
          </FileUploadItem>
        ))}
      </FileUploadList>
    </FileUpload>
  );
}

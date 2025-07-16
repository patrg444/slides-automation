'use client';

import { Heading } from '@/components/ui/heading';
import React, { useEffect, useRef, useState } from 'react';
import { FileText, Loader2, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useRouter, useParams } from 'next/navigation';
import PageContainer from '@/components/layout/page-container';
import { getCaseStudyById } from '@/actions/case-study';
import { CaseStudyFile, CaseStudyWithFiles } from '@/types';
import { toast } from 'sonner';
import ReactMarkdown from 'react-markdown';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle
} from '@/components/ui/dialog';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import { createOnePager } from '@/actions/create-one-pager';
import Image from 'next/image';

const CaseStudyPage = () => {
  const { id } = useParams();
  const router = useRouter();
  const caseStudyId = id as string;
  const [loadingState, setLoadingState] = useState<{
    isLoading: boolean;
    type?: 'creating' | 'processing' | 'loading';
  }>({ isLoading: true });
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const [caseStudy, setCaseStudy] = useState<CaseStudyWithFiles | null>(null);
  const [selectedMarkdown, setSelectedMarkdown] = useState<{
    content: string;
    filename: string;
  } | null>(null);
  const [selectedImage, setSelectedImage] = useState<{
    url: string;
    filename: string;
  } | null>(null);
  const [selectedSummary, setSelectedSummary] = useState<{
    content: string;
    filename: string;
  } | null>(null);

  const handleCreateOnePager = async () => {
    if (!caseStudy?.files?.[0]?.markdown) {
      toast.error('No content available to create one pager');
      return;
    }
    setLoadingState({ isLoading: true, type: 'creating' });
    try {
      const caseStudySummary = await createOnePager(
        caseStudy.files[0].markdown,
        caseStudyId
      );
      toast.success('One pager created successfully');
      setSelectedSummary({
        content: caseStudySummary.summary,
        filename: `Summary ${caseStudySummary.id}`
      });
      setCaseStudy((prev) => {
        if (!prev) return null;
        return {
          ...prev,
          summaries: [...prev.summaries, caseStudySummary]
        };
      });
    } catch (error) {
      toast.error('Failed to create one pager');
    } finally {
      setLoadingState({ isLoading: false });
    }
  };

  const handleCreateProposalSlides = async () => {
    if (!caseStudy?.files?.[0]?.markdown) {
      toast.error('No content available to create proposal slides');
      return;
    }
    setLoadingState({ isLoading: true, type: 'creating' });

    try {
      await new Promise((resolve) => setTimeout(resolve, 3000));
      toast.success('Proposal slides created successfully');
    } catch (error) {
      toast.error('Failed to create proposal slides');
    } finally {
      setLoadingState({ isLoading: false });
    }
  };

  const hasProcessingFiles = (files: CaseStudyFile[]) =>
    files.some((file) => file.status === 'processing');

  const fetchCaseStudy = async () => {
    try {
      const data = await getCaseStudyById(caseStudyId);
      setCaseStudy(data);

      const stillProcessing = hasProcessingFiles(data.files);
      setLoadingState({
        isLoading: stillProcessing,
        type: stillProcessing ? 'processing' : 'loading'
      });

      if (!stillProcessing && intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    } catch (error) {
      toast.error('Failed to fetch case study', {
        description: 'Please try again'
      });
      router.push('/dashboard/case-studies');
    }
  };

  useEffect(() => {
    fetchCaseStudy().then(() => {
      intervalRef.current = setInterval(fetchCaseStudy, 1000);
    });

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [caseStudyId]);

  if (loadingState.isLoading) {
    const files = caseStudy?.files ?? [];
    const processingCount = files.filter(
      (f) => f.status === 'processing'
    ).length;
    const message =
      loadingState.type === 'creating'
        ? 'Generating your one pager document...'
        : loadingState.type === 'processing'
          ? `Processing ${processingCount} of ${files.length} files...`
          : 'Loading your case study details...';

    return (
      <PageContainer>
        <div className='absolute inset-0 flex flex-col items-center justify-center bg-white/60'>
          <Loader2 className='animate-spin text-gray-400' size={48} />
          <p className='mt-4 text-gray-600'>{message}</p>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <div className='flex min-h-0 flex-1 flex-col space-y-8 px-4 sm:px-6 lg:px-8'>
        <div className='flex items-center justify-between'>
          <Heading title={caseStudy?.title || ''} description='' />
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant='outline' className='font-medium'>
                <Plus className='mr-2 h-4 w-4' />
                Generate
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={handleCreateOnePager}>
                Create one pager
              </DropdownMenuItem>
              <DropdownMenuItem onClick={handleCreateProposalSlides}>
                Create proposal slides
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <div className='mb-8 space-y-6'>
          <div>
            <h3 className='text-xl font-bold tracking-tight'>Source files</h3>
            <p className='text-sm text-gray-500'>
              {caseStudy?.files.length} files
            </p>
          </div>
          <div className='flex w-full max-w-md flex-row gap-8'>
            {caseStudy?.files?.map((file: CaseStudyFile, idx: number) => (
              <div
                key={file.file_url + idx}
                className='flex cursor-pointer items-center gap-6 rounded-xl border border-gray-200 bg-white p-6'
                onClick={() => window.open(file.file_url, '_blank')}
              >
                <div className='flex h-16 w-16 items-center justify-center rounded-lg border border-gray-200 bg-gray-50'>
                  <FileText className='h-8 w-8 text-gray-400' />
                </div>
                <div className='truncate text-lg font-semibold text-gray-900'>
                  {file.file_url.split('/').pop()}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Summary Section */}
        <div className='mb-8 space-y-6'>
          <div>
            <h3 className='text-xl font-bold tracking-tight'>One Pager</h3>
            <p className='text-sm text-gray-500'>
              Summaries generated from your case study files
            </p>
          </div>
          <div className='flex w-full max-w-md flex-row gap-8'>
            {caseStudy?.summaries.map((summary, idx) => (
              <div
                key={summary.id}
                className='flex cursor-pointer items-center gap-6 rounded-xl border border-gray-200 bg-white p-6'
                onClick={() =>
                  router.push(
                    `/dashboard/case-studies/${caseStudyId}/summary/${summary.id}`
                  )
                }
              >
                <div className='flex h-16 w-16 items-center justify-center rounded-lg border border-gray-200 bg-gray-50'>
                  <FileText className='h-8 w-8 text-gray-400' />
                </div>
                <div className='truncate text-lg font-semibold text-gray-900'>
                  Summary {idx + 1}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Markdown Content Section */}
        <div className='mb-8 space-y-6'>
          <div>
            <h3 className='text-xl font-bold tracking-tight'>
              [Debug only] Extracted content
            </h3>
            <p className='text-sm text-gray-500'>
              Extracted content from your case study files
            </p>
          </div>
          <div className='flex w-full max-w-md flex-row gap-8'>
            {caseStudy?.files.map((file: CaseStudyFile, idx: number) => (
              <div
                key={file.id}
                className='flex cursor-pointer items-center gap-6 rounded-xl border border-gray-200 bg-white p-6'
                onClick={() =>
                  setSelectedMarkdown({
                    content: file.markdown || '',
                    filename: file.file_url.split('/').pop() || ''
                  })
                }
              >
                <div className='flex h-16 w-16 items-center justify-center rounded-lg border border-gray-200 bg-gray-50'>
                  <FileText className='h-8 w-8 text-gray-400' />
                </div>
                <div className='truncate text-lg font-semibold text-gray-900'>
                  {file.file_url.split('/').pop()}
                </div>
              </div>
            ))}
          </div>
        </div>

        <Dialog
          open={!!selectedMarkdown}
          onOpenChange={() => setSelectedMarkdown(null)}
        >
          <DialogContent className='max-h-[80vh] max-w-4xl overflow-y-auto'>
            <DialogHeader>
              <DialogTitle>{selectedMarkdown?.filename}</DialogTitle>
            </DialogHeader>
            <div className='prose prose-sm prose-p:my-4 max-w-none'>
              <ReactMarkdown>{selectedMarkdown?.content || ''}</ReactMarkdown>
            </div>
          </DialogContent>
        </Dialog>

        {/* Images Section */}
        <div className='mb-8 space-y-6'>
          <div>
            <h3 className='text-xl font-bold tracking-tight'>
              [Debug only] Extracted images
            </h3>
            <p className='text-sm text-gray-500'>
              Images extracted from your case study files
            </p>
          </div>
          <div className='grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6'>
            {caseStudy?.files.map((file) =>
              file.images.map((image, idx) => (
                <div
                  key={image.id}
                  className='group relative h-48 w-48 cursor-pointer overflow-hidden rounded-lg border border-gray-200 bg-white'
                  onClick={() =>
                    setSelectedImage({
                      url: image.image_url,
                      filename: `${file.file_url.split('/').pop() || 'File'} - Image ${idx + 1}`
                    })
                  }
                >
                  <Image
                    src={image.image_url}
                    alt={`Image ${idx + 1} from ${file.file_url.split('/').pop()}`}
                    width={192}
                    height={192}
                    className='h-full w-full object-scale-down transition-transform duration-300 group-hover:scale-105'
                  />
                  <div className='absolute inset-0 bg-black/40 opacity-0 transition-opacity duration-300 group-hover:opacity-100' />
                </div>
              ))
            )}
          </div>
        </div>

        <Dialog
          open={!!selectedImage}
          onOpenChange={() => setSelectedImage(null)}
        >
          <DialogContent className='max-h-[90vh] max-w-[90vw] overflow-hidden p-0'>
            <DialogHeader className='px-6 py-4'>
              <DialogTitle>{selectedImage?.filename}</DialogTitle>
            </DialogHeader>
            <div className='relative flex max-h-[calc(90vh-80px)] items-center justify-center overflow-auto'>
              <Image
                src={selectedImage?.url || ''}
                alt={selectedImage?.filename || ''}
                width={800}
                height={800}
                className='max-h-[calc(90vh-80px)] w-auto max-w-full object-contain'
              />
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </PageContainer>
  );
};

export default CaseStudyPage;

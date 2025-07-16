'use client';

import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { deleteCaseStudy, getCaseStudyById } from '@/actions/case-study';
import { CaseStudyWithFiles } from '@/types';
import PageContainer from '@/components/layout/page-container';
import { Loader2 } from 'lucide-react';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogFooter
} from '@/components/ui/alert-dialog';
import {
  AlertDialogDescription,
  AlertDialogHeader,
  AlertDialogTitle
} from '@/components/ui/alert-dialog';
import { Button, buttonVariants } from '@/components/ui/button';
import { MinimalTiptapEditor } from '@/components/minimal-tiptap';
import { AlertDialogTrigger } from '@/components/ui/alert-dialog';
import { AlertDialogContent } from '@/components/ui/alert-dialog';
import { Content } from '@tiptap/react';
import { Icons } from '@/components/icons';
import Image from 'next/image';

const SummaryPage = () => {
  const params = useParams();
  const caseStudyId = String(params.id ?? '');
  const summaryId = String(params.summaryId ?? '');

  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [caseStudy, setCaseStudy] = useState<CaseStudyWithFiles | null>(null);
  const [editorValue, setEditorValue] = useState<Content>('');
  const [showImagesPanel, setShowImagesPanel] = useState(true);

  const handleSave = async () => {
    if (!editorValue) {
      router.push(`/dashboard/case-studies/${caseStudyId}`);
      return;
    }

    // await saveCaseStudy(caseStudyId, editorValue);
    router.push(`/dashboard/case-studies/${caseStudyId}`);
  };

  const handleDelete = async () => {
    setLoading(true);
    try {
      await deleteCaseStudy(caseStudyId);
      router.push('/dashboard/case-studies');
    } catch (error) {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchCaseStudy = async () => {
      setLoading(true);
      try {
        const caseStudy: CaseStudyWithFiles = await getCaseStudyById(
          caseStudyId as string
        );
        setCaseStudy(caseStudy || null);
        setEditorValue(
          caseStudy.summaries.find((s) => s.id === summaryId)?.summary || ''
        );
      } catch (e) {
        setCaseStudy(null);
      } finally {
        setLoading(false);
      }
    };
    fetchCaseStudy();
  }, [caseStudyId, summaryId]);

  if (loading) {
    return (
      <PageContainer>
        <div className='fixed inset-0 z-50 flex min-h-screen flex-col items-center justify-center bg-white/60'>
          <Loader2 className='animate-spin text-gray-400' size={48} />
          <p className='mt-4 text-gray-600'>Loading one pager...</p>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <div className='flex min-h-0 flex-1 flex-col space-y-8 px-4 sm:px-6 lg:flex-row lg:space-y-0 lg:space-x-8 lg:px-8'>
        {/* Main Content */}
        <div className='flex min-h-0 w-full flex-1 flex-col rounded-none bg-white p-0 shadow-none'>
          <div className='mb-6 flex items-center justify-between pt-4'>
            <h2 className='text-left text-xl font-bold'>
              Edit Case Study Summary
            </h2>
            <div className='flex gap-2'>
              <Button
                className='bg-purple-600 text-white hover:bg-purple-700'
                onClick={handleSave}
              >
                Save
              </Button>
            </div>
          </div>
          <div className='h-full min-h-0 flex-1 pb-4'>
            <MinimalTiptapEditor
              value={editorValue}
              onChange={setEditorValue}
              output='html'
              className='h-full w-full overflow-y-auto'
              editorContentClassName='p-5'
              placeholder='Enter your description...'
              autofocus={true}
              editable={true}
              editorClassName='focus:outline-hidden'
              immediatelyRender={false}
            />
          </div>
          <div className='mt-8 flex justify-end'>
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button
                  variant='destructive'
                  className='bg-red-600 text-white hover:bg-red-700'
                  disabled={loading}
                >
                  Delete
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete
                    your case study and remove your data from our servers.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction
                    onClick={handleDelete}
                    className={buttonVariants({ variant: 'destructive' })}
                  >
                    Delete
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </div>
        {/* Sidebar */}
        <div className='mt-2 mb-2 ml-6 hidden h-[90vh] w-16 flex-col items-center rounded-2xl border border-gray-100 bg-white px-2 py-4 shadow-sm lg:flex'>
          <button
            className={`rounded p-2 transition-colors ${showImagesPanel ? 'bg-gray-100' : 'hover:bg-gray-100'}`}
            aria-label='Images'
            onClick={() => setShowImagesPanel((v) => !v)}
          >
            <Icons.media className='h-7 w-7 text-gray-400' />
          </button>
        </div>
        {/* Right Panel: Images */}
        {showImagesPanel &&
          caseStudy &&
          caseStudy.files &&
          caseStudy.files.some((f) => f.images && f.images.length > 0) && (
            <div className='relative hidden h-[90vh] w-80 max-w-xs flex-col overflow-y-auto rounded-2xl border border-gray-200 bg-white pl-6 shadow-sm lg:flex'>
              <button
                className='absolute top-3 right-3 z-10 rounded-full p-1 transition-colors hover:bg-gray-100'
                aria-label='Close Images Panel'
                onClick={() => setShowImagesPanel(false)}
              >
                <Icons.close className='h-5 w-5 text-gray-400' />
              </button>
              <h3 className='mt-2 mb-4 text-lg font-semibold'>
                Case Study Images
              </h3>
              <div className='flex flex-col gap-4'>
                {caseStudy.files
                  .flatMap((file) => file.images || [])
                  .map((image) => (
                    <div key={image.id} className='flex flex-col items-center'>
                      <div className='w-full'>
                        <div
                          className='bg-card flex items-center justify-center overflow-hidden rounded-xl border shadow-sm'
                          style={{ width: 320, height: 160 }}
                        >
                          <Image
                            src={image.image_url}
                            alt={`Case Study Image ${image.id}`}
                            width={320}
                            height={160}
                            className='max-h-full max-w-full bg-gray-100 object-contain'
                            style={{
                              width: 'auto',
                              height: 'auto',
                              maxWidth: '100%',
                              maxHeight: '100%',
                              objectFit: 'contain'
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}
      </div>
    </PageContainer>
  );
};

export default SummaryPage;

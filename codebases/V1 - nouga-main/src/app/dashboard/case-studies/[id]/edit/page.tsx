'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Heading } from '@/components/ui/heading';
import { Button, buttonVariants } from '@/components/ui/button';

import { IconSparkles } from '@tabler/icons-react';
import { MinimalTiptapEditor } from '@/components/minimal-tiptap';
import GenerateDialog from '@/components/case-studies/generate-dialog';
import { DialogTrigger } from '@/components/ui/dialog';
import { Dialog } from '@/components/ui/dialog';
import useCaseStudyStore from '@/store/useCaseStudyStore';
import { Content } from '@tiptap/react';
import PageContainer from '@/components/layout/page-container';
import { CaseStudy, CaseStudyData } from '@/types';
import {
  getCaseStudyById,
  saveCaseStudy,
  deleteCaseStudy
} from '@/actions/case-study';
import { Loader2 } from 'lucide-react';
import {
  AlertDialog,
  AlertDialogTrigger,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogCancel,
  AlertDialogAction
} from '@/components/ui/alert-dialog';
import { toast } from 'sonner';

// Todo: load the case study summary instead of the case study

function caseStudyToContentString(caseStudy: CaseStudy) {
  //   if (!caseStudy.summary) {
  //     return '';
  //   }

  //   const data = caseStudy.summary;

  //   return `
  // **Title:** ${data.title}

  // **Challenge:** ${data.challenge}

  // **Approach:** ${data.approach}

  // **Solution:** ${data.solution}

  // **Outcomes:** ${data.outcomes}

  // **Summary:** ${data.summary}

  // **Key Points:**
  // ${data.key_points.map((pt: string) => `- ${pt}`).join('\n')}
  //   `;

  return 'todo: fix this';
}

const EditCaseStudyPage = () => {
  const params = useParams();
  const caseStudyId = params.id as string;
  const router = useRouter();
  const [editorValue, setEditorValue] = useState<Content>('');
  const [loading, setLoading] = useState(true);

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
    setLoading(true);
    getCaseStudyById(caseStudyId)
      .then((caseStudy) => {
        const contentString = caseStudy
          ? caseStudyToContentString(caseStudy)
          : '';

        setEditorValue(contentString);
        setLoading(false);
      })
      .catch((error) => {
        toast.error('Failed to load case study. Please try again.', {
          description: error.message
        });
        setLoading(false);
      });
  }, [caseStudyId]);

  return (
    <PageContainer>
      {loading && (
        <div className='fixed inset-0 z-50 flex items-center justify-center bg-white/60'>
          <Loader2 className='animate-spin text-gray-400' size={48} />
        </div>
      )}

      <div className='flex min-h-0 flex-1 flex-col space-y-8 px-4 sm:px-6 lg:px-8'>
        <div className='flex items-center justify-between'>
          <Heading title={`Edit Case Study`} description='' />
        </div>
        <div className='flex min-h-0 w-full flex-1 flex-col rounded-none bg-white p-0 shadow-none'>
          <div className='mb-6 flex items-center justify-between pt-4'>
            <h2 className='text-left text-2xl font-bold'>
              Edit Case Study Form
            </h2>
            <div className='flex gap-2'>
              <Dialog>
                <DialogTrigger asChild>
                  <Button variant='outline' className='font-medium'>
                    <IconSparkles className='mr-2 size-4' />
                    Generate other formats
                  </Button>
                </DialogTrigger>
                <GenerateDialog />
              </Dialog>
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
      </div>
    </PageContainer>
  );
};

export default EditCaseStudyPage;

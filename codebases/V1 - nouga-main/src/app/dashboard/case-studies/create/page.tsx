'use client';

import React from 'react';
import { Heading } from '@/components/ui/heading';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import * as z from 'zod';
import { useRouter } from 'next/navigation';
import { FileUploadInput } from '@/components/case-studies/file-upload-input';
import SpinnerCircle from '@/components/ui/spinner';
import PageContainer from '@/components/layout/page-container';
import { createCaseStudy } from '@/actions/create-case-study';
import { toast } from 'sonner';
import { FileWithStatus } from '@/types';

const formSchema = z.object({
  projectName: z.string().min(1, { message: 'Project name is required.' }),
  clientName: z.string().optional(),
  industry: z.string().optional()
});

const Page = () => {
  const router = useRouter();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      projectName: '',
      clientName: '',
      industry: ''
    }
  });
  const [loading, setLoading] = React.useState(false);
  const [uploadedFiles, setUploadedFiles] = React.useState<FileWithStatus[]>(
    []
  );

  const handleGenerate = async (values: z.infer<typeof formSchema>) => {
    setLoading(true);
    try {
      const projectName = values.projectName;
      const clientName = values.clientName || null;
      const industry = values.industry || null;
      const fileUrls = uploadedFiles
        .map((file) => file.url)
        .filter((url) => url !== undefined);

      const caseStudy = await createCaseStudy({
        title: projectName,
        client: clientName,
        industry: industry,
        fileUrls: fileUrls
      });

      router.push(`/dashboard/case-studies/${caseStudy.id}`);
    } catch (error) {
      setLoading(false);
      toast.error('Failed to generate case study. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className='bg-opacity-20 fixed inset-0 z-50 flex items-center justify-center bg-white'>
        <SpinnerCircle />
        <span className='ml-4 text-xl font-semibold text-purple-600'>
          Generating case study, please wait...
        </span>
      </div>
    );
  }

  return (
    <PageContainer>
      <div className='h-full w-full space-y-8 px-4 sm:px-6 lg:px-8'>
        <Heading title='Create Case Study' description='' />
        <div className='w-full rounded-none bg-white p-0 shadow-none'>
          <div className='mb-12'>
            <h3 className='text-xl font-semibold'>Select files</h3>
            <p className='pb-4'>
              Upload or select project files from your file drive.
            </p>
            <FileUploadInput
              uploadedFiles={uploadedFiles}
              setUploadedFiles={setUploadedFiles}
            />
          </div>
          <div className='pb-4'>
            <h3 className='text-xl font-semibold'>Case Study Information</h3>
            <p className='pb-4'>Enter information about your case study.</p>
            <Form {...form}>
              <form
                onSubmit={form.handleSubmit(handleGenerate)}
                className='space-y-6'
              >
                <FormField
                  control={form.control}
                  name='projectName'
                  render={({ field }) => (
                    <FormItem>
                      <div className='flex items-center gap-8'>
                        <FormLabel className='w-48 whitespace-nowrap sm:w-56 lg:w-72'>
                          Project name
                        </FormLabel>
                        <FormControl className='max-w-[512px] flex-1'>
                          <Input placeholder='Enter project name' {...field} />
                        </FormControl>
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <hr className='my-6 border-gray-200' />
                <FormField
                  control={form.control}
                  name='clientName'
                  render={({ field }) => (
                    <FormItem>
                      <div className='flex items-center gap-8'>
                        <FormLabel className='w-48 whitespace-nowrap sm:w-56 lg:w-72'>
                          Client name
                        </FormLabel>
                        <FormControl className='max-w-[512px] flex-1'>
                          <Input placeholder='Enter client name' {...field} />
                        </FormControl>
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <hr className='my-6 border-gray-200' />
                <FormField
                  control={form.control}
                  name='industry'
                  render={({ field }) => (
                    <FormItem>
                      <div className='flex items-center gap-8'>
                        <FormLabel className='w-48 whitespace-nowrap sm:w-56 lg:w-72'>
                          Industry
                        </FormLabel>
                        <FormControl className='max-w-[512px] flex-1'>
                          <Input placeholder='Enter industry' {...field} />
                        </FormControl>
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <hr className='my-6 border-gray-200' />
                <div className='flex justify-end gap-2'>
                  <Button
                    type='button'
                    variant='outline'
                    onClick={() => router.back()}
                  >
                    Cancel
                  </Button>
                  <Button
                    type='submit'
                    className='bg-[#7F56D9] text-white'
                    disabled={loading}
                  >
                    Generate Case Study
                  </Button>
                </div>
              </form>
            </Form>
          </div>
        </div>
      </div>
    </PageContainer>
  );
};

export default Page;

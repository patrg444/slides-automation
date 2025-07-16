import { CaseStudyCard } from '@/components/case-studies/case-study-card';
import { Heading } from '@/components/ui/heading';
import Link from 'next/link';
import { IconPlus } from '@tabler/icons-react';
import PageContainer from '@/components/layout/page-container';
import { getAllCaseStudies } from '@/actions/case-study';

export default async function CaseStudiesPage() {
  const caseStudies = await getAllCaseStudies();
  const isEmpty = !caseStudies || caseStudies.length === 0;

  return (
    <PageContainer>
      <div className='h-full w-full space-y-8 p-4 sm:p-6 lg:p-8'>
        <div className='flex items-center justify-between'>
          <Heading
            title='Case Studies'
            description='Explore how our customers succeed with our solutions.'
          />
          {!isEmpty && (
            <Link href='/dashboard/case-studies/create'>
              <button className='hover:bg-secondary-dark flex items-center gap-2 rounded-md bg-black px-4 py-2 font-bold text-white shadow transition-all duration-200 hover:scale-105 hover:shadow-lg'>
                <IconPlus size={24} />
                Create New
              </button>
            </Link>
          )}
        </div>
        {isEmpty ? (
          <div className='flex flex-col items-center justify-center'>
            <div className='mb-4 text-2xl font-semibold text-gray-500'>
              No case studies yet
            </div>
            <Link href='/dashboard/case-studies/create'>
              <button className='hover:bg-secondary-dark flex items-center gap-2 rounded-md bg-black px-6 py-2 font-bold text-white shadow transition-all duration-200 hover:scale-105 hover:shadow-lg'>
                <IconPlus size={20} />
                Create your first case study
              </button>
            </Link>
          </div>
        ) : (
          <div className='grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4'>
            {caseStudies.map((study, index) => (
              <CaseStudyCard key={study.id} caseStudy={study} index={index} />
            ))}
          </div>
        )}
      </div>
    </PageContainer>
  );
}

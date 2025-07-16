'use client';

import * as React from 'react';
import { CaseStudy } from '@/types';
import Link from 'next/link';
import {
  Card,
  CardContent,
  CardTitle,
  CardDescription,
  CardHeader
} from '@/components/ui/card';
import Image from 'next/image';
import { motion } from 'framer-motion';

interface CaseStudyCardProps {
  caseStudy: CaseStudy;
  index: number;
}

export const CaseStudyCard: React.FC<CaseStudyCardProps> = ({
  caseStudy,
  index
}) => {
  const imageUrl =
    'https://images.unsplash.com/photo-1519125323398-675f0ddb6308';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
    >
      <Link
        href={`/dashboard/case-studies/${caseStudy.id}`}
        className='block focus:outline-none'
        tabIndex={0}
      >
        <Card className='max-w-md cursor-pointer overflow-hidden pt-0 transition-shadow hover:shadow-lg'>
          <CardHeader className='relative h-56 overflow-hidden rounded-t-xl bg-gray-100'>
            <Image
              src={imageUrl}
              alt={caseStudy.title}
              fill
              className='h-full w-full object-cover object-top'
            />
          </CardHeader>
          <CardContent className='p-x-4'>
            <div className='mb-1 text-sm font-medium text-violet-600'>
              {caseStudy.client} {caseStudy.industry}
            </div>
            <div className='mb-2 flex items-center gap-1'>
              <CardTitle className='m-0 flex-1 p-0 text-lg font-bold'>
                {caseStudy.title}
              </CardTitle>
            </div>
            <CardDescription className='mb-4 line-clamp-2 text-sm text-gray-600'>
              {caseStudy.description}
            </CardDescription>
            {/* <div className='flex flex-wrap gap-2'>
              {caseStudy.tags.map((tag) => (
                <span
                  key={tag}
                  className={
                    'rounded-full px-3 py-1 text-xs font-medium ' +
                    (tag === 'Design'
                      ? 'bg-violet-100 text-violet-700'
                      : tag === 'Research'
                        ? 'bg-blue-100 text-blue-700'
                        : tag === 'Presentation'
                          ? 'bg-pink-100 text-pink-700'
                          : 'bg-gray-100 text-gray-700')
                  }
                >
                  {tag}
                </span>
              ))}
            </div> */}
          </CardContent>
        </Card>
      </Link>
    </motion.div>
  );
};

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { CaseStudy } from '@/types';

interface CaseStudyStore {
  caseStudy: CaseStudy | null;
  setCaseStudy: (caseStudy: CaseStudy) => void;
}

const useCaseStudyStore = create<CaseStudyStore>()(
  persist<CaseStudyStore>(
    (set) => ({
      caseStudy: null,
      setCaseStudy: (caseStudy: CaseStudy) => set({ caseStudy })
    }),
    {
      name: 'case-study-store'
    }
  )
);

export default useCaseStudyStore;

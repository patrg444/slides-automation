import { Icons } from '@/components/icons';

export interface NavItem {
  title: string;
  url: string;
  disabled?: boolean;
  external?: boolean;
  shortcut?: [string, string];
  icon?: keyof typeof Icons;
  label?: string;
  description?: string;
  isActive?: boolean;
  items?: NavItem[];
}

export interface NavItemWithChildren extends NavItem {
  items: NavItemWithChildren[];
}

export interface NavItemWithOptionalChildren extends NavItem {
  items?: NavItemWithChildren[];
}

export interface FooterItem {
  title: string;
  items: {
    title: string;
    href: string;
    external?: boolean;
  }[];
}

export type MainNavItem = NavItemWithOptionalChildren;

export type SidebarNavItem = NavItemWithChildren;

export type CaseStudy = {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  client: string | null;
  industry: string | null;
  created_at: Date;
  updated_at: Date;
};

export type CaseStudyFile = {
  id: string;
  case_study_id: string;
  request_id: string;
  file_url: string;
  markdown: string | null;
  metadata: Record<string, any> | null;
  created_at: Date;
  updated_at: Date;
  status: 'processing' | 'complete';
  error: string | null;
};

export type CaseStudyImage = {
  id: string;
  file_id: string;
  image_url: string;
  created_at: Date;
  updated_at: Date;
};

export type CaseStudySummary = {
  id: string;
  case_study_id: string;
  summary: string;
  created_at: Date;
  updated_at: Date;
};

export type CaseStudyData = {
  title: string;
  challenge: string;
  approach: string;
  solution: string;
  outcomes: string;
  summary: string;
  key_points: string[];
};

export type FileWithStatus = {
  name: string;
  filePath: string;
  content: File;
  status: 'idle' | 'uploading' | 'success' | 'error';
  url?: string;
  error?: string;
};

export type CaseStudyWithFiles = CaseStudy & {
  files: (CaseStudyFile & {
    images: CaseStudyImage[];
  })[];
  summaries: CaseStudySummary[];
};

import { jsonb, pgTable, text, timestamp, uuid } from 'drizzle-orm/pg-core';

// Custom type for case study file status
export const caseStudyFileStatus = ['processing', 'complete'] as const;

// Users table
export const users = pgTable('users', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  created_at: timestamp('created_at', { withTimezone: true })
    .notNull()
    .defaultNow(),
  updated_at: timestamp('updated_at', { withTimezone: true })
    .notNull()
    .defaultNow()
    .$onUpdateFn(() => new Date())
});

// Case Studies table
export const caseStudies = pgTable('case_studies', {
  id: uuid('id').primaryKey().defaultRandom(),
  user_id: text('user_id')
    .references(() => users.id, { onDelete: 'cascade' })
    .notNull(),
  title: text('title').notNull(),
  description: text('description'),
  client: text('client'),
  industry: text('industry'),
  created_at: timestamp('created_at', { withTimezone: true })
    .notNull()
    .defaultNow(),
  updated_at: timestamp('updated_at', { withTimezone: true })
    .notNull()
    .defaultNow()
    .$onUpdateFn(() => new Date())
});

export const caseStudyFiles = pgTable('case_study_files', {
  id: uuid('id').primaryKey().defaultRandom(),
  case_study_id: uuid('case_study_id')
    .references(() => caseStudies.id, { onDelete: 'cascade' })
    .notNull(),
  request_id: text('request_id').notNull(),
  file_url: text('file_url').notNull(),
  markdown: text('markdown'),
  metadata: jsonb('metadata'),
  created_at: timestamp('created_at', { withTimezone: true })
    .notNull()
    .defaultNow(),
  updated_at: timestamp('updated_at', { withTimezone: true })
    .notNull()
    .defaultNow()
    .$onUpdateFn(() => new Date()),
  status: text('status', { enum: caseStudyFileStatus })
    .notNull()
    .default('processing'),
  error: text('error')
});

export const caseStudyImages = pgTable('case_study_images', {
  id: uuid('id').primaryKey().defaultRandom(),
  file_id: uuid('file_id')
    .references(() => caseStudyFiles.id)
    .notNull(),
  created_at: timestamp('created_at', { withTimezone: true })
    .notNull()
    .defaultNow(),
  updated_at: timestamp('updated_at', { withTimezone: true })
    .notNull()
    .defaultNow()
    .$onUpdateFn(() => new Date()),
  image_url: text('image_url').notNull()
});

export const caseStudySummaries = pgTable('case_study_summaries', {
  id: uuid('id').primaryKey().defaultRandom(),
  case_study_id: uuid('case_study_id')
    .references(() => caseStudies.id, { onDelete: 'cascade' })
    .notNull(),
  summary: text('summary').notNull(),
  created_at: timestamp('created_at', { withTimezone: true })
    .notNull()
    .defaultNow(),
  updated_at: timestamp('updated_at', { withTimezone: true })
    .notNull()
    .defaultNow()
    .$onUpdateFn(() => new Date())
});

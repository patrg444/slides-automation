ALTER TABLE "case_study_files" ADD COLUMN "request_id" text NOT NULL;--> statement-breakpoint
ALTER TABLE "case_study_files" ADD COLUMN "status" text DEFAULT 'processing' NOT NULL;--> statement-breakpoint
ALTER TABLE "case_study_files" ADD COLUMN "error" text;
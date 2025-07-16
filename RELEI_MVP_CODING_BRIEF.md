# Relei Pilot MVP - Coding Brief

## Project Overview
**Client**: Samantha Lim  
**Deadline**: July 31, 2025 (Milestone 1)  
**Current Codebase**: V1 (nouga-main) - This is the production codebase  
**Payment**: $1,500 for Milestone 1 completion  

## Key Documents
1. **Relei Pilot Product Brief** - Main requirements document
2. **Freelance Agreement** - Defines deliverables and milestones
3. **Figma Prototype** - Visual design reference
4. **V1 Codebase** - Production codebase (Next.js/PostgreSQL)
5. **V2 Codebase** - Alternative implementation (FastAPI/MongoDB) - NOT for production

## Core MVP Features to Implement

### 1. Case Study Slide Generation (Priority: CRITICAL)
**Current State**: Text output only (markdown format)  
**Required**: Transform to slide-based format supporting:
- HTML display
- PPTX export
- Google Slides export

**Implementation Notes**:
- Use existing AI extraction outputs from `create-one-pager.ts` and `create-case-study.ts`
- Map text sections (Challenge, Approach, Solution, Outcomes, Summary) to slide layouts
- Reference Figma prototype for visual design

### 2. Image Selector (Priority: HIGH)
**Current State**: Images extracted via Marker API but no selection UI  
**Required**: 
- UI to display extracted images
- Allow users to assign images to specific case study sections
- Integration with slide generation

### 3. Basic Editor (Priority: HIGH)
**Current State**: Tiptap dependencies present but editor not implemented  
**Required**:
- Text editing for AI-generated content
- Image swap functionality
- Slide reordering capability
- Save/update functionality

### 4. Reusable Asset Library (Priority: MEDIUM)
**Current State**: Basic library mentioned but not clearly implemented  
**Required**:
- Extend to store logos, graphics, boilerplate text
- Searchable interface
- Easy insertion into case studies

### 5. Template Application (Priority: MEDIUM)
**Current State**: Not implemented  
**Required**:
- Template system for branding (cover slides, fonts, colors, logos)
- Database storage for template configurations
- Dynamic application during slide generation

### 6. Export/Download (Priority: CRITICAL)
**Current State**: Not implemented  
**Required**:
- PPTX export functionality
- Google Slides export functionality
- Download management

## Existing Components to Leverage

### Authentication & User Management
- **Clerk** - Already integrated (`middleware.ts`)
- User context available via Clerk hooks

### File Processing & AI
- **File Upload**: Functional in `create-case-study.ts`
- **Marker API**: Extracts images and text from uploaded files
- **Gemini Flash**: Generates text summaries (`create-one-pager.ts`)
- **OpenAI**: Available but usage unclear

### Database & Storage
- **PostgreSQL** via Drizzle ORM (NOT MongoDB as mentioned in handover)
- **Supabase** for database and file storage
- Schema defined in `schema.ts`

### Frontend Stack
- **Next.js 15** with App Router
- **React** with TypeScript
- **Shadcn UI** components
- **Tailwind CSS** for styling

### Deployment
- **Vercel** - Scripts and config already set up
- Environment variables managed via `.env`

## Critical Discrepancies RESOLVED

### 1. Backend Architecture - RESOLVED
**V1 (Production)**: Next.js 15 full-stack with server actions  
**V2 (Alternative)**: Python/FastAPI + React/Vite (separate backend/frontend)  
**Decision**: Use V1's Next.js architecture - it's the production codebase

### 2. Database System - RESOLVED
**V1 (Production)**: PostgreSQL with Drizzle ORM + Supabase  
**V2 (Alternative)**: MongoDB  
**Decision**: Use V1's PostgreSQL setup - it's already in production

### 3. Why Two Codebases Exist
- **V1**: Complete production application with full features
- **V2**: Experimental implementation focusing on advanced document processing (AWS Textract)
- **V2 Features to Consider**: Enhanced PDF/PPTX processing capabilities that could be ported to V1

### 4. Remaining Clarifications Needed
- **Blop API**: Not found in either codebase - likely deprecated
- **Access Rights**: Still need Clerk and Supabase credentials from Samantha

## Technical Implementation Roadmap

### Phase 1: Foundation (Days 1-3)
1. Set up development environment with V1 codebase
2. Verify all API keys and service access
3. Review existing code structure and data flow
4. Create basic slide data model extending current schema

### Phase 2: Core Features (Days 4-10)
1. Implement HTML slide generation from existing AI outputs
2. Build image selector UI and backend logic
3. Create basic editor with Tiptap integration
4. Develop template system structure

### Phase 3: Export & Polish (Days 11-14)
1. Integrate PPTX export library (e.g., PptxGenJS)
2. Implement Google Slides API integration
3. Extend asset library functionality
4. Testing and bug fixes

### Phase 4: Deployment (Days 15-16)
1. Deploy to Vercel staging
2. Final testing and adjustments
3. Production deployment

## Key Files to Review in V1 Codebase

### Server Actions
- `app/actions/create-case-study.ts` - File processing logic
- `app/actions/create-one-pager.ts` - AI text generation
- `app/actions/case-study.ts` - CRUD operations

### Database
- `db/schema.ts` - Current data models
- `db/index.ts` - Database connection
- Migration files in `db/migrations/`

### UI Components
- Check `components/` directory for existing UI patterns
- `app/dashboard/` for current dashboard implementation

### Configuration
- `next.config.js` - Next.js configuration
- `tailwind.config.ts` - Styling configuration
- `.env` - Environment variables (create from `.env.example` if exists)

## Development Guidelines

1. **Build on V1**: Do NOT start from scratch. Extend the existing codebase.
2. **Follow Patterns**: Match existing code style and patterns in V1.
3. **Use Existing Libraries**: Leverage already installed dependencies.
4. **Figma Reference**: Use the prototype for all UI/UX decisions.
5. **Test Continuously**: Ensure existing functionality remains intact.

## V2 Features Worth Considering

While V1 is the production codebase, V2 has some advanced document processing features that could enhance the MVP:

### Document Processing (from V2)
- **AWS Textract Integration**: More sophisticated text extraction from PDFs
- **PPTX Processing**: Direct PowerPoint file handling with `python-pptx`
- **Image Extraction**: Better handling of embedded images in documents

### Implementation Approach
- Port specific V2 features as Next.js server actions in V1
- Use V2's document processing logic as reference
- Maintain V1's architecture while adding V2's capabilities

## Immediate Next Steps

1. **Get Access**: Ensure you have all necessary credentials:
   - Supabase project access
   - Clerk dashboard access
   - API keys (Marker, Gemini, OpenAI)
   - Figma file access

2. **Environment Setup**:
   ```bash
   cd /Users/patrickgloria/google-slides-relei
   # Review V1 codebase structure
   # Set up .env with provided credentials
   # Install dependencies
   # Run development server
   ```

3. **First Code Tasks**:
   - Create slide generation proof of concept
   - Extend database schema for slide data
   - Build basic editor component

## Questions for Samantha Before Deep Implementation

1. Is there a Python/FastAPI backend, or is Next.js the complete backend?
2. Confirm PostgreSQL/Supabase is the correct database (not MongoDB)?
3. Is Blop API integration required for MVP?
4. Do you have specific PPTX/Google Slides templates to follow?
5. Any specific branding guidelines beyond Figma?

---

**Note**: This brief consolidates all information from the Relei Pilot Product Brief, Freelance Agreement, and V1 codebase analysis. The V1 codebase is confirmed as the current running version to build upon.
# Google Slides Integration Guide for Relei MVP

## Overview
The Relei MVP requires exporting case studies to Google Slides format. This guide outlines the integration approach using the existing Google Slides API code in the project.

## Existing Google Slides Code

### Available Scripts
- `google_slides_enhanced.py` - Enhanced API wrapper
- `google_slides_enhanced_v2.py` - Version 2 improvements
- `presentation_manager.py` - Presentation management utilities
- `export_manager.py` - Export functionality
- `test_google_slides.py` - Basic API operations examples

### Key Capabilities from Existing Code
1. Create presentations
2. Add slides with various layouts
3. Insert and format text
4. Create tables
5. Add shapes and images
6. Apply consistent styling

## Integration Strategy

### 1. Connect Next.js to Python Scripts
Since the V1 codebase is Next.js but Google Slides scripts are in Python, consider:

**Option A: API Endpoint**
- Create a Python FastAPI microservice using existing scripts
- Call from Next.js server actions

**Option B: Direct Integration**
- Use Google Slides API directly from Node.js
- Port key Python functionality to TypeScript

**Option C: Hybrid Approach**
- Use Python scripts for complex operations
- Simple operations directly in Node.js

### 2. Data Flow for Case Study Export

```
Case Study Data (PostgreSQL)
    ↓
Format for Slides (Next.js)
    ↓
Generate Slides Structure
    ↓
Call Google Slides API
    ↓
Return Presentation URL
```

### 3. Slide Structure Mapping

Map case study sections to slides:

```javascript
const slideMapping = {
  coverSlide: {
    layout: 'TITLE',
    content: {
      title: caseStudy.title,
      subtitle: caseStudy.client
    }
  },
  challengeSlide: {
    layout: 'TITLE_AND_BODY',
    content: {
      title: 'Challenge',
      body: caseStudy.challenge
    }
  },
  solutionSlide: {
    layout: 'TITLE_AND_TWO_COLUMNS',
    content: {
      title: 'Solution',
      column1: caseStudy.approach,
      column2: caseStudy.solution
    }
  },
  outcomesSlide: {
    layout: 'TITLE_AND_BODY',
    content: {
      title: 'Outcomes',
      body: caseStudy.outcomes,
      bullets: caseStudy.keyPoints
    }
  }
};
```

### 4. Authentication Setup

The project already has:
- `credentials.json` - OAuth2 credentials
- `token.json` - Stored auth token

Ensure these work with the Google account that will own the presentations.

### 5. Template Application

Use the existing Python code's formatting capabilities:
- Custom colors from brand palette
- Consistent fonts
- Logo placement
- Background colors/images

## Implementation Steps

### Step 1: Test Existing Scripts
```bash
cd /Users/patrickgloria/google-slides-relei
python test_google_slides.py
```

### Step 2: Create Export Service
```typescript
// app/services/googleSlidesExport.ts
export async function exportToGoogleSlides(caseStudyId: string) {
  // 1. Fetch case study data
  // 2. Format for slides
  // 3. Call Google Slides API
  // 4. Return presentation URL
}
```

### Step 3: Add to Export Options
```typescript
// In your export component
const handleGoogleSlidesExport = async () => {
  const presentationUrl = await exportToGoogleSlides(caseStudyId);
  // Open in new tab or show success message
};
```

## Google Slides API Key Methods

From the existing code, these are the key methods to use:

1. **Create Presentation**
   ```python
   presentation_id = api.create_presentation(title)
   ```

2. **Add Slides**
   ```python
   slide_id = api.add_slide(presentation_id, layout_type)
   ```

3. **Add Formatted Text**
   ```python
   api.add_formatted_text(presentation_id, slide_id, text, 
                         font_size=24, bold=True, color={...})
   ```

4. **Add Images**
   ```python
   api.add_image(presentation_id, slide_id, image_url, 
                x=100, y=100, width=400, height=300)
   ```

5. **Create Tables**
   ```python
   table_id = api.create_table(presentation_id, slide_id, 
                              rows=3, columns=2)
   ```

## Important Considerations

1. **API Quotas**: Google Slides API has usage limits
2. **Image URLs**: Must be publicly accessible for Google to fetch
3. **Permissions**: Generated presentations will be owned by the authenticated account
4. **Styling**: Use batchUpdate for efficiency when applying multiple formats

## Next Steps for Integration

1. Decide on integration approach (Python microservice vs Node.js port)
2. Create proof of concept with a simple case study
3. Implement full mapping of case study data to slides
4. Add template/branding system
5. Handle errors and provide user feedback

## Resources

- [Google Slides API Docs](https://developers.google.com/slides)
- [API Reference](https://developers.google.com/slides/api/reference/rest)
- [Python Client Library](https://github.com/googleapis/google-api-python-client)
- [Node.js Client Library](https://github.com/googleapis/google-api-nodejs-client)
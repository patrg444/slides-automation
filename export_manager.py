#!/usr/bin/env python3
"""
Export Manager - Export Google Slides to various formats
"""

import os
import requests
from typing import Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io


class ExportManager:
    """Handle exporting presentations to different formats"""
    
    def __init__(self, credentials: Credentials):
        self.creds = credentials
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.slides_service = build('slides', 'v1', credentials=self.creds)
    
    def export_as_pdf(self, presentation_id: str, output_path: str) -> bool:
        """Export presentation as PDF"""
        try:
            # Export using Drive API
            request = self.drive_service.files().export_media(
                fileId=presentation_id,
                mimeType='application/pdf'
            )
            
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%")
            
            # Save to file
            fh.seek(0)
            with open(output_path, 'wb') as f:
                f.write(fh.read())
            
            print(f"✅ Exported to PDF: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting PDF: {e}")
            return False
    
    def export_as_pptx(self, presentation_id: str, output_path: str) -> bool:
        """Export presentation as PowerPoint"""
        try:
            # Export using Drive API
            request = self.drive_service.files().export_media(
                fileId=presentation_id,
                mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation'
            )
            
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%")
            
            # Save to file
            fh.seek(0)
            with open(output_path, 'wb') as f:
                f.write(fh.read())
            
            print(f"✅ Exported to PPTX: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting PPTX: {e}")
            return False
    
    def export_as_images(self, presentation_id: str, output_dir: str, format: str = 'png') -> bool:
        """Export presentation slides as images"""
        try:
            # Get presentation details
            presentation = self.slides_service.presentations().get(
                presentationId=presentation_id
            ).execute()
            
            slides = presentation.get('slides', [])
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Export each slide
            for i, slide in enumerate(slides):
                slide_id = slide.get('objectId')
                
                # Get slide thumbnail
                response = self.slides_service.presentations().pages().getThumbnail(
                    presentationId=presentation_id,
                    pageObjectId=slide_id,
                    thumbnailProperties_thumbnailSize='LARGE'
                ).execute()
                
                content_url = response.get('contentUrl')
                
                if content_url:
                    # Download image
                    img_response = requests.get(content_url)
                    
                    # Save image
                    output_path = os.path.join(output_dir, f'slide_{i+1}.{format}')
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    
                    print(f"✅ Exported slide {i+1} as image")
            
            return True
            
        except Exception as e:
            print(f"❌ Error exporting images: {e}")
            return False
    
    def generate_html_preview(self, presentation_id: str, output_path: str) -> bool:
        """Generate HTML preview of presentation"""
        try:
            # Get presentation details
            presentation = self.slides_service.presentations().get(
                presentationId=presentation_id
            ).execute()
            
            title = presentation.get('title', 'Presentation')
            slides = presentation.get('slides', [])
            
            # Generate HTML
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        .slide {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin: 20px 0;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .slide-number {{
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }}
        .slide-content {{
            min-height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #fafafa;
            border-radius: 4px;
            padding: 20px;
        }}
        .element {{
            margin: 10px 0;
        }}
        .text-element {{
            color: #333;
            line-height: 1.6;
        }}
        .navigation {{
            text-align: center;
            margin: 30px 0;
        }}
        .nav-button {{
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 4px;
            cursor: pointer;
        }}
        .nav-button:hover {{
            background: #0056b3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="navigation">
            <button class="nav-button" onclick="previousSlide()">Previous</button>
            <span id="slideInfo">Slide 1 of {len(slides)}</span>
            <button class="nav-button" onclick="nextSlide()">Next</button>
        </div>
"""
            
            # Add slides
            for i, slide in enumerate(slides):
                display = 'block' if i == 0 else 'none'
                html_content += f"""
        <div class="slide" id="slide{i}" style="display: {display};">
            <div class="slide-number">Slide {i+1}</div>
            <div class="slide-content">
"""
                
                # Extract text content from slide
                elements = slide.get('pageElements', [])
                for element in elements:
                    if 'shape' in element:
                        shape = element['shape']
                        if shape.get('shapeType') == 'TEXT_BOX':
                            text_elements = shape.get('text', {}).get('textElements', [])
                            text = ''
                            for text_element in text_elements:
                                if 'textRun' in text_element:
                                    text += text_element['textRun'].get('content', '')
                            
                            if text.strip():
                                html_content += f'                <div class="element text-element">{text.strip()}</div>\n'
                
                html_content += """            </div>
        </div>
"""
            
            # Add JavaScript
            html_content += f"""
        <div class="navigation">
            <button class="nav-button" onclick="previousSlide()">Previous</button>
            <button class="nav-button" onclick="nextSlide()">Next</button>
        </div>
    </div>
    
    <script>
        let currentSlide = 0;
        const totalSlides = {len(slides)};
        
        function showSlide(n) {{
            const slides = document.querySelectorAll('.slide');
            if (n >= totalSlides) currentSlide = 0;
            if (n < 0) currentSlide = totalSlides - 1;
            
            slides.forEach(slide => slide.style.display = 'none');
            slides[currentSlide].style.display = 'block';
            
            document.getElementById('slideInfo').textContent = 
                `Slide ${{currentSlide + 1}} of ${{totalSlides}}`;
        }}
        
        function nextSlide() {{
            currentSlide++;
            showSlide(currentSlide);
        }}
        
        function previousSlide() {{
            currentSlide--;
            showSlide(currentSlide);
        }}
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight') nextSlide();
            if (e.key === 'ArrowLeft') previousSlide();
        }});
    </script>
</body>
</html>
"""
            
            # Save HTML file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ Generated HTML preview: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating HTML: {e}")
            return False
#!/usr/bin/env python3
"""
Enhanced Google Slides API Wrapper
Improved version with better error handling, unique IDs, and more features
"""

import os
import json
import uuid
import time
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from functools import wraps
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations']


def retry_on_error(max_retries=3, delay=1):
    """Decorator to retry API calls on failure"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except HttpError as e:
                    if attempt < max_retries - 1:
                        if e.resp.status in [429, 500, 503]:  # Rate limit or server errors
                            time.sleep(delay * (attempt + 1))
                            continue
                    raise
            return None
        return wrapper
    return decorator


class GoogleSlidesEnhanced:
    """Enhanced Google Slides API wrapper with improved features"""
    
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Handle authentication for Google Slides API"""
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("ERROR: credentials.json not found!")
                    print("Please follow the setup instructions in SETUP.md")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        
        self.service = build('slides', 'v1', credentials=self.creds)
        return True
    
    @staticmethod
    def generate_id(prefix='element'):
        """Generate a unique ID for elements"""
        return f"{prefix}_{uuid.uuid4().hex[:12]}"
    
    @retry_on_error()
    def create_presentation(self, title: str) -> Optional[str]:
        """Create a new presentation"""
        try:
            presentation = {
                'title': title
            }
            
            presentation = self.service.presentations().create(
                body=presentation).execute()
            
            presentation_id = presentation.get("presentationId")
            print(f'✅ Created presentation: {title}')
            print(f'   ID: {presentation_id}')
            return presentation_id
        
        except HttpError as error:
            print(f'❌ Error creating presentation: {error}')
            return None
    
    @retry_on_error()
    def add_slide(self, presentation_id: str, layout: str = 'BLANK', 
                  insertion_index: Optional[int] = None) -> Optional[str]:
        """Add a new slide to the presentation"""
        try:
            request = {
                'createSlide': {
                    'slideLayoutReference': {
                        'predefinedLayout': layout
                    }
                }
            }
            
            if insertion_index is not None:
                request['createSlide']['insertionIndex'] = insertion_index
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': [request]}
            ).execute()
            
            slide_id = response.get('replies')[0].get('createSlide').get('objectId')
            print(f'✅ Added {layout} slide (ID: {slide_id})')
            return slide_id
        
        except HttpError as error:
            print(f'❌ Error adding slide: {error}')
            return None
    
    @retry_on_error()
    def add_text_box(self, presentation_id: str, page_id: str, text: str,
                     x: int = 100, y: int = 100, width: int = 300, height: int = 50) -> Optional[str]:
        """Add a text box to a slide"""
        try:
            element_id = self.generate_id('textbox')
            
            requests = [
                {
                    'createShape': {
                        'objectId': element_id,
                        'shapeType': 'TEXT_BOX',
                        'elementProperties': {
                            'pageObjectId': page_id,
                            'size': {
                                'width': {'magnitude': width, 'unit': 'PT'},
                                'height': {'magnitude': height, 'unit': 'PT'}
                            },
                            'transform': {
                                'scaleX': 1,
                                'scaleY': 1,
                                'translateX': x,
                                'translateY': y,
                                'unit': 'PT'
                            }
                        }
                    }
                },
                {
                    'insertText': {
                        'objectId': element_id,
                        'text': text,
                        'insertionIndex': 0
                    }
                }
            ]
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'✅ Added text box: "{text[:30]}..."' if len(text) > 30 else f'✅ Added text box: "{text}"')
            return element_id
        
        except HttpError as error:
            print(f'❌ Error adding text box: {error}')
            return None
    
    @retry_on_error()
    def add_formatted_text(self, presentation_id: str, page_id: str, text: str,
                          x: int = 100, y: int = 100, width: int = 300, height: int = 50,
                          font_size: int = 14, bold: bool = False, italic: bool = False,
                          font_family: str = 'Arial', color: Optional[Dict] = None,
                          alignment: str = 'LEFT') -> Optional[str]:
        """Add formatted text with advanced styling"""
        try:
            element_id = self.generate_id('formatted_text')
            
            requests = [
                {
                    'createShape': {
                        'objectId': element_id,
                        'shapeType': 'TEXT_BOX',
                        'elementProperties': {
                            'pageObjectId': page_id,
                            'size': {
                                'width': {'magnitude': width, 'unit': 'PT'},
                                'height': {'magnitude': height, 'unit': 'PT'}
                            },
                            'transform': {
                                'scaleX': 1,
                                'scaleY': 1,
                                'translateX': x,
                                'translateY': y,
                                'unit': 'PT'
                            }
                        }
                    }
                },
                {
                    'insertText': {
                        'objectId': element_id,
                        'text': text,
                        'insertionIndex': 0
                    }
                }
            ]
            
            # Text style
            style_update = {
                'updateTextStyle': {
                    'objectId': element_id,
                    'style': {
                        'fontSize': {'magnitude': font_size, 'unit': 'PT'},
                        'fontFamily': font_family,
                        'bold': bold,
                        'italic': italic
                    },
                    'textRange': {'type': 'ALL'},
                    'fields': 'fontSize,fontFamily,bold,italic'
                }
            }
            
            if color:
                style_update['updateTextStyle']['style']['foregroundColor'] = {
                    'opaqueColor': {'rgbColor': color}
                }
                style_update['updateTextStyle']['fields'] += ',foregroundColor'
            
            requests.append(style_update)
            
            # Paragraph style - map alignment values
            alignment_map = {
                'LEFT': 'START',
                'CENTER': 'CENTER',
                'RIGHT': 'END',
                'JUSTIFIED': 'JUSTIFIED'
            }
            
            if alignment in alignment_map:
                requests.append({
                    'updateParagraphStyle': {
                        'objectId': element_id,
                        'style': {
                            'alignment': alignment_map.get(alignment, 'START')
                        },
                        'textRange': {'type': 'ALL'},
                        'fields': 'alignment'
                    }
                })
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'✅ Added formatted text: "{text[:30]}..."' if len(text) > 30 else f'✅ Added formatted text: "{text}"')
            return element_id
        
        except HttpError as error:
            print(f'❌ Error adding formatted text: {error}')
            return None
    
    @retry_on_error()
    def create_table(self, presentation_id: str, page_id: str, rows: int = 3, columns: int = 3,
                     x: int = 50, y: int = 50, width: int = 400, height: int = 200) -> Optional[str]:
        """Create a table on a slide"""
        try:
            table_id = self.generate_id('table')
            
            requests = [{
                'createTable': {
                    'objectId': table_id,
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'width': {'magnitude': width, 'unit': 'PT'},
                            'height': {'magnitude': height, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': x,
                            'translateY': y,
                            'unit': 'PT'
                        }
                    },
                    'rows': rows,
                    'columns': columns
                }
            }]
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'✅ Created {rows}x{columns} table')
            return table_id
        
        except HttpError as error:
            print(f'❌ Error creating table: {error}')
            return None
    
    @retry_on_error()
    def fill_table(self, presentation_id: str, table_id: str, data: List[List[str]],
                   header_row: bool = True) -> bool:
        """Fill an entire table with data"""
        try:
            requests = []
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_text in enumerate(row_data):
                    request = {
                        'insertText': {
                            'objectId': table_id,
                            'cellLocation': {
                                'rowIndex': row_idx,
                                'columnIndex': col_idx
                            },
                            'text': cell_text,
                            'insertionIndex': 0
                        }
                    }
                    requests.append(request)
                    
                    # Format header row
                    if header_row and row_idx == 0:
                        requests.append({
                            'updateTableCellProperties': {
                                'objectId': table_id,
                                'tableRange': {
                                    'location': {
                                        'rowIndex': 0,
                                        'columnIndex': col_idx
                                    },
                                    'rowSpan': 1,
                                    'columnSpan': 1
                                },
                                'tableCellProperties': {
                                    'tableCellBackgroundFill': {
                                        'solidFill': {
                                            'color': {
                                                'rgbColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
                                            }
                                        }
                                    }
                                },
                                'fields': 'tableCellBackgroundFill'
                            }
                        })
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'✅ Filled table with {len(data)} rows of data')
            return True
        
        except HttpError as error:
            print(f'❌ Error filling table: {error}')
            return False
    
    @retry_on_error()
    def add_bullet_list(self, presentation_id: str, page_id: str, items: List[str],
                        x: int = 50, y: int = 50, width: int = 400, height: int = 200,
                        font_size: int = 12) -> Optional[str]:
        """Add a properly formatted bullet list"""
        try:
            element_id = self.generate_id('bullet_list')
            
            # Create text box
            requests = [{
                'createShape': {
                    'objectId': element_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'width': {'magnitude': width, 'unit': 'PT'},
                            'height': {'magnitude': height, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': x,
                            'translateY': y,
                            'unit': 'PT'
                        }
                    }
                }
            }]
            
            # Add all text with newlines
            text = '\n'.join(items)
            requests.append({
                'insertText': {
                    'objectId': element_id,
                    'text': text,
                    'insertionIndex': 0
                }
            })
            
            # Execute initial requests
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            # Apply bullet formatting in a separate request
            bullet_requests = []
            for i in range(len(items)):
                bullet_requests.append({
                    'createParagraphBullets': {
                        'objectId': element_id,
                        'textRange': {
                            'type': 'FIXED_RANGE',
                            'startIndex': sum(len(items[j]) + 1 for j in range(i)),
                            'endIndex': sum(len(items[j]) + 1 for j in range(i + 1)) - 1
                        },
                        'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                    }
                })
            
            # Set font size
            bullet_requests.append({
                'updateTextStyle': {
                    'objectId': element_id,
                    'style': {
                        'fontSize': {'magnitude': font_size, 'unit': 'PT'}
                    },
                    'textRange': {'type': 'ALL'},
                    'fields': 'fontSize'
                }
            })
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': bullet_requests}
            ).execute()
            
            print(f'✅ Added bullet list with {len(items)} items')
            return element_id
        
        except HttpError as error:
            print(f'❌ Error adding bullet list: {error}')
            return None
    
    @retry_on_error()
    def add_shape(self, presentation_id: str, page_id: str, shape_type: str = 'RECTANGLE',
                  x: int = 100, y: int = 100, width: int = 200, height: int = 100,
                  fill_color: Optional[Dict] = None, outline_color: Optional[Dict] = None,
                  outline_weight: int = 2) -> Optional[str]:
        """Add a shape with customizable properties"""
        try:
            shape_id = self.generate_id('shape')
            
            requests = [{
                'createShape': {
                    'objectId': shape_id,
                    'shapeType': shape_type,
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'width': {'magnitude': width, 'unit': 'PT'},
                            'height': {'magnitude': height, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': x,
                            'translateY': y,
                            'unit': 'PT'
                        }
                    }
                }
            }]
            
            # Shape properties
            shape_properties = {}
            fields = []
            
            if fill_color:
                shape_properties['shapeBackgroundFill'] = {
                    'solidFill': {
                        'color': {'rgbColor': fill_color}
                    }
                }
                fields.append('shapeBackgroundFill')
            
            if outline_color:
                shape_properties['outline'] = {
                    'weight': {'magnitude': outline_weight, 'unit': 'PT'},
                    'outlineFill': {
                        'solidFill': {
                            'color': {'rgbColor': outline_color}
                        }
                    }
                }
                fields.append('outline')
            
            if shape_properties:
                requests.append({
                    'updateShapeProperties': {
                        'objectId': shape_id,
                        'shapeProperties': shape_properties,
                        'fields': ','.join(fields)
                    }
                })
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'✅ Added {shape_type} shape')
            return shape_id
        
        except HttpError as error:
            print(f'❌ Error adding shape: {error}')
            return None
    
    @retry_on_error()
    def add_image(self, presentation_id: str, page_id: str, image_url: str,
                  x: int = 100, y: int = 100, width: int = 300, height: int = 200) -> Optional[str]:
        """Add an image from URL"""
        try:
            image_id = self.generate_id('image')
            
            requests = [{
                'createImage': {
                    'objectId': image_id,
                    'url': image_url,
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'width': {'magnitude': width, 'unit': 'PT'},
                            'height': {'magnitude': height, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': x,
                            'translateY': y,
                            'unit': 'PT'
                        }
                    }
                }
            }]
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'✅ Added image from URL')
            return image_id
        
        except HttpError as error:
            print(f'❌ Error adding image: {error}')
            return None
    
    @retry_on_error()
    def duplicate_slide(self, presentation_id: str, slide_id: str,
                       insertion_index: Optional[int] = None) -> Optional[str]:
        """Duplicate an existing slide"""
        try:
            request = {
                'duplicateObject': {
                    'objectId': slide_id
                }
            }
            
            if insertion_index is not None:
                request['duplicateObject']['insertionIndex'] = insertion_index
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': [request]}
            ).execute()
            
            new_slide_id = response.get('replies')[0].get('duplicateObject').get('objectId')
            print(f'✅ Duplicated slide (new ID: {new_slide_id})')
            return new_slide_id
        
        except HttpError as error:
            print(f'❌ Error duplicating slide: {error}')
            return None
    
    @retry_on_error()
    def update_slide_properties(self, presentation_id: str, page_id: str,
                               background_color: Optional[Dict] = None,
                               background_image_url: Optional[str] = None) -> bool:
        """Update slide properties"""
        try:
            page_properties = {}
            fields = []
            
            if background_color:
                page_properties['pageBackgroundFill'] = {
                    'solidFill': {
                        'color': {'rgbColor': background_color}
                    }
                }
                fields.append('pageBackgroundFill')
            
            if background_image_url:
                page_properties['pageBackgroundFill'] = {
                    'stretchedPictureFill': {
                        'contentUrl': background_image_url
                    }
                }
                fields.append('pageBackgroundFill')
            
            if not page_properties:
                return True
            
            requests = [{
                'updatePageProperties': {
                    'objectId': page_id,
                    'pageProperties': page_properties,
                    'fields': ','.join(fields)
                }
            }]
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print('✅ Updated slide properties')
            return True
        
        except HttpError as error:
            print(f'❌ Error updating slide properties: {error}')
            return False
    
    @retry_on_error()
    def get_presentation(self, presentation_id: str) -> Optional[Dict]:
        """Get presentation details"""
        try:
            presentation = self.service.presentations().get(
                presentationId=presentation_id
            ).execute()
            return presentation
        
        except HttpError as error:
            print(f'❌ Error getting presentation: {error}')
            return None
    
    def create_title_slide(self, presentation_id: str, title: str, subtitle: str = "") -> Optional[str]:
        """Create a title slide with formatted text"""
        slide_id = self.add_slide(presentation_id, 'TITLE')
        
        if slide_id:
            # Add title
            self.add_formatted_text(
                presentation_id, slide_id, title,
                x=50, y=150, width=600, height=100,
                font_size=48, bold=True, alignment='CENTER'
            )
            
            # Add subtitle if provided
            if subtitle:
                self.add_formatted_text(
                    presentation_id, slide_id, subtitle,
                    x=50, y=300, width=600, height=60,
                    font_size=24, alignment='CENTER',
                    color={'red': 0.5, 'green': 0.5, 'blue': 0.5}
                )
        
        return slide_id
    
    def create_content_slide(self, presentation_id: str, title: str, 
                            content: List[str], slide_type: str = 'bullets') -> Optional[str]:
        """Create a content slide with title and bullet points or paragraphs"""
        slide_id = self.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Add title
            self.add_formatted_text(
                presentation_id, slide_id, title,
                x=50, y=30, width=600, height=60,
                font_size=32, bold=True
            )
            
            # Add content
            if slide_type == 'bullets':
                self.add_bullet_list(
                    presentation_id, slide_id, content,
                    x=50, y=120, width=600, height=300,
                    font_size=18
                )
            else:
                # Add as paragraph text
                text = '\n\n'.join(content)
                self.add_formatted_text(
                    presentation_id, slide_id, text,
                    x=50, y=120, width=600, height=300,
                    font_size=16
                )
        
        return slide_id


def main():
    """Test the enhanced Google Slides API wrapper"""
    print("\n🚀 Enhanced Google Slides API Test")
    print("=" * 50)
    
    # Initialize API
    api = GoogleSlidesEnhanced()
    
    if not api.service:
        print("Failed to authenticate. Please check your credentials.")
        return
    
    # Create a new presentation
    print("\n📝 Creating presentation...")
    presentation_id = api.create_presentation(f'Enhanced API Demo - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    
    if not presentation_id:
        return
    
    # Create title slide
    print("\n📊 Creating slides...")
    api.create_title_slide(
        presentation_id,
        "Google Slides API Enhanced Demo",
        "Showcasing Advanced Features"
    )
    
    # Create content slide with bullets
    api.create_content_slide(
        presentation_id,
        "Key Features",
        [
            "Unique ID generation with UUID",
            "Retry logic for API resilience",
            "Enhanced error handling",
            "More formatting options",
            "Helper methods for common patterns"
        ]
    )
    
    # Create a slide with shapes
    shapes_slide = api.add_slide(presentation_id, 'BLANK')
    if shapes_slide:
        api.add_formatted_text(
            presentation_id, shapes_slide,
            "Shapes and Colors",
            x=50, y=30, width=600, height=60,
            font_size=32, bold=True
        )
        
        # Add various shapes
        api.add_shape(
            presentation_id, shapes_slide, 'RECTANGLE',
            x=50, y=120, width=150, height=100,
            fill_color={'red': 0.2, 'green': 0.6, 'blue': 0.9},
            outline_color={'red': 0.1, 'green': 0.3, 'blue': 0.6}
        )
        
        api.add_shape(
            presentation_id, shapes_slide, 'ELLIPSE',
            x=250, y=120, width=150, height=150,
            fill_color={'red': 0.9, 'green': 0.3, 'blue': 0.3},
            outline_color={'red': 0.6, 'green': 0.1, 'blue': 0.1}
        )
        
        api.add_shape(
            presentation_id, shapes_slide, 'TRIANGLE',
            x=450, y=120, width=150, height=150,
            fill_color={'red': 0.3, 'green': 0.9, 'blue': 0.3},
            outline_color={'red': 0.1, 'green': 0.6, 'blue': 0.1}
        )
    
    # Create a slide with a table
    table_slide = api.add_slide(presentation_id, 'BLANK')
    if table_slide:
        api.add_formatted_text(
            presentation_id, table_slide,
            "Sample Data Table",
            x=50, y=30, width=600, height=60,
            font_size=32, bold=True
        )
        
        table_id = api.create_table(
            presentation_id, table_slide,
            rows=4, columns=4,
            x=50, y=120, width=600, height=250
        )
        
        if table_id:
            data = [
                ['Quarter', 'Revenue', 'Expenses', 'Profit'],
                ['Q1 2024', '$125,000', '$80,000', '$45,000'],
                ['Q2 2024', '$150,000', '$90,000', '$60,000'],
                ['Q3 2024', '$175,000', '$95,000', '$80,000']
            ]
            api.fill_table(presentation_id, table_id, data, header_row=True)
    
    # Create a slide with gradient background
    gradient_slide = api.add_slide(presentation_id, 'BLANK')
    if gradient_slide:
        api.update_slide_properties(
            presentation_id, gradient_slide,
            background_color={'red': 0.95, 'green': 0.98, 'blue': 1.0}
        )
        
        api.add_formatted_text(
            presentation_id, gradient_slide,
            "Thank You!",
            x=50, y=200, width=600, height=100,
            font_size=48, bold=True, alignment='CENTER',
            color={'red': 0.2, 'green': 0.3, 'blue': 0.6}
        )
    
    # Print success message and URL
    print(f"\n✅ Enhanced presentation created successfully!")
    print(f"📎 View at: https://docs.google.com/presentation/d/{presentation_id}/edit")
    print("\n💡 Features demonstrated:")
    print("   - UUID-based unique IDs")
    print("   - Retry logic for API calls")
    print("   - Enhanced text formatting")
    print("   - Proper bullet list handling")
    print("   - Table creation with header formatting")
    print("   - Shape styling with fill and outline")
    print("   - Slide background customization")
    print("   - Helper methods for common patterns")


if __name__ == '__main__':
    main()
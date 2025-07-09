#!/usr/bin/env python3
"""
Enhanced Google Slides API Wrapper v2
Improved version with better layout, spacing, and professional styling
"""

import os
import json
import uuid
import time
import math
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

# Slide dimensions in PT (points)
SLIDE_WIDTH = 720
SLIDE_HEIGHT = 405

# Professional layout constants
LAYOUTS = {
    'standard': {
        'margin': 60,  # Increased margins for better spacing
        'title_top': 40,
        'title_height': 60,
        'content_top': 120,
        'content_spacing': 20,
        'footer_bottom': 380
    },
    'two_column': {
        'column_gap': 40,
        'column_width': 300
    },
    'table': {
        'cell_padding': 10,
        'header_height': 40,
        'row_height': 35
    }
}

# Professional color palette
THEME_COLORS = {
    'primary': {'red': 0.161, 'green': 0.314, 'blue': 0.612},  # Professional blue
    'secondary': {'red': 0.404, 'green': 0.404, 'blue': 0.404},  # Dark gray
    'accent': {'red': 0.918, 'green': 0.341, 'blue': 0.224},  # Coral red
    'success': {'red': 0.298, 'green': 0.686, 'blue': 0.314},  # Green
    'warning': {'red': 1.0, 'green': 0.757, 'blue': 0.027},  # Yellow
    'text_primary': {'red': 0.133, 'green': 0.133, 'blue': 0.133},  # Almost black
    'text_secondary': {'red': 0.459, 'green': 0.459, 'blue': 0.459},  # Medium gray
    'background': {'red': 1.0, 'green': 1.0, 'blue': 1.0},  # White
    'background_alt': {'red': 0.969, 'green': 0.969, 'blue': 0.969},  # Light gray
    'table_header': {'red': 0.925, 'green': 0.941, 'blue': 0.957},  # Very light blue
    'border': {'red': 0.878, 'green': 0.878, 'blue': 0.878}  # Light gray border
}

# Font sizes for consistency
FONT_SIZES = {
    'title': 40,
    'heading': 28,
    'subheading': 22,
    'body': 16,
    'caption': 14,
    'small': 12
}

# Scopes
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
                        if e.resp.status in [429, 500, 503]:
                            time.sleep(delay * (attempt + 1))
                            continue
                    raise
            return None
        return wrapper
    return decorator


class GoogleSlidesEnhancedV2:
    """Enhanced Google Slides API wrapper with improved layout and styling"""
    
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
    
    @staticmethod
    def calculate_text_height(text: str, font_size: int, width: int) -> int:
        """Calculate appropriate height for text box based on content"""
        avg_char_width = font_size * 0.6
        chars_per_line = width / avg_char_width
        lines = math.ceil(len(text) / chars_per_line)
        line_height = font_size * 1.4  # Better line spacing
        return int(max(lines * line_height + 20, font_size * 2.5))  # Add padding
    
    @staticmethod
    def get_centered_position(width: int, element_width: int, margin: int = 60) -> int:
        """Calculate centered X position within available width"""
        available_width = width - (2 * margin)
        return margin + (available_width - element_width) // 2
    
    @retry_on_error()
    def create_presentation(self, title: str) -> Optional[str]:
        """Create a new presentation"""
        try:
            presentation = {'title': title}
            presentation = self.service.presentations().create(body=presentation).execute()
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
                    'slideLayoutReference': {'predefinedLayout': layout}
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
    def add_text_box_smart(self, presentation_id: str, page_id: str, text: str,
                          position: str = 'left', margin_top: int = 0,
                          width_percent: float = 0.9, font_size: Optional[int] = None,
                          color: Optional[Dict] = None, bold: bool = False,
                          alignment: str = 'LEFT') -> Optional[str]:
        """Add text box with smart positioning and sizing"""
        try:
            element_id = self.generate_id('textbox')
            margin = LAYOUTS['standard']['margin']
            available_width = SLIDE_WIDTH - (2 * margin)
            width = int(available_width * width_percent)
            
            # Smart positioning
            if position == 'center':
                x = self.get_centered_position(SLIDE_WIDTH, width, margin)
            elif position == 'right':
                x = SLIDE_WIDTH - margin - width
            else:  # left
                x = margin
            
            y = margin_top if margin_top > 0 else LAYOUTS['standard']['content_top']
            
            # Auto-calculate height
            if font_size is None:
                font_size = FONT_SIZES['body']
            height = self.calculate_text_height(text, font_size, width)
            
            # Create text box
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
            
            # Text styling
            style = {
                'fontSize': {'magnitude': font_size, 'unit': 'PT'},
                'fontFamily': 'Arial',
                'bold': bold
            }
            
            if color:
                style['foregroundColor'] = {'opaqueColor': {'rgbColor': color}}
            else:
                style['foregroundColor'] = {'opaqueColor': {'rgbColor': THEME_COLORS['text_primary']}}
            
            requests.append({
                'updateTextStyle': {
                    'objectId': element_id,
                    'style': style,
                    'textRange': {'type': 'ALL'},
                    'fields': 'fontSize,fontFamily,bold,foregroundColor'
                }
            })
            
            # Paragraph alignment
            alignment_map = {
                'LEFT': 'START',
                'CENTER': 'CENTER',
                'RIGHT': 'END',
                'JUSTIFIED': 'JUSTIFIED'
            }
            
            requests.append({
                'updateParagraphStyle': {
                    'objectId': element_id,
                    'style': {
                        'alignment': alignment_map.get(alignment, 'START'),
                        'lineSpacing': 125  # 1.25 line spacing
                    },
                    'textRange': {'type': 'ALL'},
                    'fields': 'alignment,lineSpacing'
                }
            })
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'✅ Added text: "{text[:30]}..."' if len(text) > 30 else f'✅ Added text: "{text}"')
            return element_id
            
        except HttpError as error:
            print(f'❌ Error adding text: {error}')
            return None
    
    @retry_on_error()
    def add_title(self, presentation_id: str, page_id: str, title: str,
                  subtitle: Optional[str] = None) -> bool:
        """Add a properly formatted title and optional subtitle"""
        try:
            # Add title
            self.add_text_box_smart(
                presentation_id, page_id, title,
                position='center',
                margin_top=LAYOUTS['standard']['title_top'],
                width_percent=0.9,
                font_size=FONT_SIZES['title'],
                color=THEME_COLORS['primary'],
                bold=True,
                alignment='CENTER'
            )
            
            # Add subtitle if provided
            if subtitle:
                self.add_text_box_smart(
                    presentation_id, page_id, subtitle,
                    position='center',
                    margin_top=100,
                    width_percent=0.8,
                    font_size=FONT_SIZES['subheading'],
                    color=THEME_COLORS['secondary'],
                    alignment='CENTER'
                )
            
            return True
            
        except Exception as error:
            print(f'❌ Error adding title: {error}')
            return False
    
    @retry_on_error()
    def add_bullet_list_improved(self, presentation_id: str, page_id: str, items: List[str],
                                x: Optional[int] = None, y: Optional[int] = None,
                                width: Optional[int] = None, font_size: Optional[int] = None) -> Optional[str]:
        """Add bullet list with improved formatting"""
        try:
            element_id = self.generate_id('bullet_list')
            
            # Default positioning
            if x is None:
                x = LAYOUTS['standard']['margin']
            if y is None:
                y = LAYOUTS['standard']['content_top']
            if width is None:
                width = SLIDE_WIDTH - (2 * LAYOUTS['standard']['margin'])
            if font_size is None:
                font_size = FONT_SIZES['body']
            
            # Calculate height based on items
            height = len(items) * font_size * 2  # More spacing between items
            
            # Create single text with all items
            text = '\n'.join(items)
            
            # Create text box
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
            
            # Apply bullet formatting in separate request
            bullet_requests = []
            
            # Apply bullets to all text at once
            bullet_requests.append({
                'createParagraphBullets': {
                    'objectId': element_id,
                    'textRange': {'type': 'ALL'},
                    'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                }
            })
            
            # Style the text
            bullet_requests.append({
                'updateTextStyle': {
                    'objectId': element_id,
                    'style': {
                        'fontSize': {'magnitude': font_size, 'unit': 'PT'},
                        'fontFamily': 'Arial',
                        'foregroundColor': {'opaqueColor': {'rgbColor': THEME_COLORS['text_primary']}}
                    },
                    'textRange': {'type': 'ALL'},
                    'fields': 'fontSize,fontFamily,foregroundColor'
                }
            })
            
            # Set line spacing
            bullet_requests.append({
                'updateParagraphStyle': {
                    'objectId': element_id,
                    'style': {
                        'lineSpacing': 150,  # 1.5x line spacing
                        'spaceAbove': {'magnitude': 6, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 6, 'unit': 'PT'}
                    },
                    'textRange': {'type': 'ALL'},
                    'fields': 'lineSpacing,spaceAbove,spaceBelow'
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
    def create_styled_table(self, presentation_id: str, page_id: str, data: List[List[str]],
                           x: Optional[int] = None, y: Optional[int] = None,
                           width: Optional[int] = None) -> Optional[str]:
        """Create a professionally styled table"""
        try:
            table_id = self.generate_id('table')
            rows = len(data)
            cols = len(data[0]) if data else 0
            
            # Default positioning
            if x is None:
                x = LAYOUTS['standard']['margin']
            if y is None:
                y = LAYOUTS['standard']['content_top']
            if width is None:
                width = SLIDE_WIDTH - (2 * LAYOUTS['standard']['margin'])
            
            # Calculate height based on rows
            header_height = LAYOUTS['table']['header_height']
            row_height = LAYOUTS['table']['row_height']
            height = header_height + (rows - 1) * row_height
            
            # Create table
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
                    'columns': cols
                }
            }]
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            # Fill table with data and styling
            styling_requests = []
            
            # Fill cells
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_text in enumerate(row_data):
                    styling_requests.append({
                        'insertText': {
                            'objectId': table_id,
                            'cellLocation': {
                                'rowIndex': row_idx,
                                'columnIndex': col_idx
                            },
                            'text': cell_text,
                            'insertionIndex': 0
                        }
                    })
                    
                    # Style header row
                    if row_idx == 0:
                        styling_requests.append({
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
                                            'color': {'rgbColor': THEME_COLORS['table_header']}
                                        }
                                    }
                                },
                                'fields': 'tableCellBackgroundFill'
                            }
                        })
                        
                        # Bold header text
                        styling_requests.append({
                            'updateTextStyle': {
                                'objectId': table_id,
                                'cellLocation': {
                                    'rowIndex': 0,
                                    'columnIndex': col_idx
                                },
                                'style': {
                                    'bold': True,
                                    'fontSize': {'magnitude': FONT_SIZES['body'], 'unit': 'PT'}
                                },
                                'textRange': {'type': 'ALL'},
                                'fields': 'bold,fontSize'
                            }
                        })
            
            # Add borders to all cells
            for row in range(rows):
                for col in range(cols):
                    styling_requests.append({
                        'updateTableBorderProperties': {
                            'objectId': table_id,
                            'tableRange': {
                                'location': {
                                    'rowIndex': row,
                                    'columnIndex': col
                                },
                                'rowSpan': 1,
                                'columnSpan': 1
                            },
                            'borderPosition': 'ALL',
                            'tableBorderProperties': {
                                'tableBorderFill': {
                                    'solidFill': {
                                        'color': {'rgbColor': THEME_COLORS['border']}
                                    }
                                },
                                'weight': {'magnitude': 1, 'unit': 'PT'}
                            },
                            'fields': 'tableBorderFill,weight'
                        }
                    })
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': styling_requests}
            ).execute()
            
            print(f'✅ Created styled table ({rows}x{cols})')
            return table_id
            
        except HttpError as error:
            print(f'❌ Error creating table: {error}')
            return None
    
    @retry_on_error()
    def add_shape_styled(self, presentation_id: str, page_id: str, shape_type: str = 'RECTANGLE',
                        x: int = 100, y: int = 100, width: int = 200, height: int = 100,
                        fill_color: Optional[Dict] = None, add_shadow: bool = True) -> Optional[str]:
        """Add a shape with modern styling including shadow"""
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
            
            # Fill color
            if fill_color:
                shape_properties['shapeBackgroundFill'] = {
                    'solidFill': {'color': {'rgbColor': fill_color}}
                }
                fields.append('shapeBackgroundFill')
            
            # Add subtle shadow for depth
            if add_shadow:
                shape_properties['shadow'] = {
                    'type': 'OUTER',
                    'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}},
                    'alpha': 0.2,
                    'rotateWithShape': False,
                    'blurRadius': {'magnitude': 3, 'unit': 'PT'}
                }
                fields.append('shadow')
            
            # Subtle outline
            shape_properties['outline'] = {
                'weight': {'magnitude': 1, 'unit': 'PT'},
                'outlineFill': {
                    'solidFill': {
                        'color': {'rgbColor': THEME_COLORS['border']}
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
            
            print(f'✅ Added styled {shape_type} shape')
            return shape_id
            
        except HttpError as error:
            print(f'❌ Error adding shape: {error}')
            return None
    
    @retry_on_error()
    def add_two_column_layout(self, presentation_id: str, page_id: str,
                             left_content: List[str], right_content: List[str],
                             left_title: Optional[str] = None, right_title: Optional[str] = None) -> bool:
        """Create a professional two-column layout"""
        try:
            margin = LAYOUTS['standard']['margin']
            gap = LAYOUTS['two_column']['column_gap']
            column_width = LAYOUTS['two_column']['column_width']
            
            y_start = LAYOUTS['standard']['content_top']
            
            # Left column
            if left_title:
                self.add_text_box_smart(
                    presentation_id, page_id, left_title,
                    position='left',
                    margin_top=y_start,
                    width_percent=0.4,
                    font_size=FONT_SIZES['subheading'],
                    color=THEME_COLORS['primary'],
                    bold=True
                )
                y_start += 50
            
            self.add_bullet_list_improved(
                presentation_id, page_id, left_content,
                x=margin,
                y=y_start,
                width=column_width
            )
            
            # Divider
            self.add_shape_styled(
                presentation_id, page_id, 'RECTANGLE',
                x=margin + column_width + gap//2 - 1,
                y=LAYOUTS['standard']['content_top'],
                width=2,
                height=250,
                fill_color=THEME_COLORS['border'],
                add_shadow=False
            )
            
            # Right column
            y_start = LAYOUTS['standard']['content_top']
            if right_title:
                self.add_text_box_smart(
                    presentation_id, page_id, right_title,
                    position='left',
                    margin_top=y_start,
                    width_percent=0.4,
                    font_size=FONT_SIZES['subheading'],
                    color=THEME_COLORS['primary'],
                    bold=True
                )
                y_start += 50
            
            self.add_bullet_list_improved(
                presentation_id, page_id, right_content,
                x=margin + column_width + gap,
                y=y_start,
                width=column_width
            )
            
            return True
            
        except Exception as error:
            print(f'❌ Error creating two-column layout: {error}')
            return False
    
    @retry_on_error()
    def update_slide_background(self, presentation_id: str, page_id: str,
                               color: Optional[Dict] = None) -> bool:
        """Update slide background with professional styling"""
        try:
            if color is None:
                color = THEME_COLORS['background']
            
            requests = [{
                'updatePageProperties': {
                    'objectId': page_id,
                    'pageProperties': {
                        'pageBackgroundFill': {
                            'solidFill': {'color': {'rgbColor': color}}
                        }
                    },
                    'fields': 'pageBackgroundFill'
                }
            }]
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print('✅ Updated slide background')
            return True
            
        except HttpError as error:
            print(f'❌ Error updating background: {error}')
            return False


def create_professional_demo():
    """Create a professional demonstration presentation"""
    api = GoogleSlidesEnhancedV2()
    
    if not api.service:
        print("Failed to authenticate")
        return
    
    # Create presentation
    presentation_id = api.create_presentation(f'Professional Demo v2 - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    
    if not presentation_id:
        return
    
    # Slide 1: Title
    print("\n📊 Creating professional presentation...")
    slide1 = api.add_slide(presentation_id, 'BLANK')
    if slide1:
        api.update_slide_background(presentation_id, slide1, THEME_COLORS['background_alt'])
        api.add_title(
            presentation_id, slide1,
            "Enhanced Google Slides API v2",
            "Professional Layouts & Modern Styling"
        )
    
    # Slide 2: Features
    slide2 = api.add_slide(presentation_id, 'BLANK')
    if slide2:
        api.add_title(presentation_id, slide2, "Key Improvements")
        api.add_bullet_list_improved(
            presentation_id, slide2,
            [
                "Smart positioning with proper margins and spacing",
                "Auto-calculated text box heights",
                "Professional color palette with accessibility in mind",
                "Modern styling with subtle shadows and borders",
                "Improved table formatting with styled headers",
                "Consistent font sizes and line spacing"
            ]
        )
    
    # Slide 3: Two Column Comparison
    slide3 = api.add_slide(presentation_id, 'BLANK')
    if slide3:
        api.add_title(presentation_id, slide3, "Version Comparison")
        api.add_two_column_layout(
            presentation_id, slide3,
            left_content=[
                "Fixed positioning",
                "Basic colors",
                "No shadows",
                "Simple tables"
            ],
            right_content=[
                "Smart layouts",
                "Professional palette",
                "Modern effects",
                "Styled tables"
            ],
            left_title="Version 1",
            right_title="Version 2"
        )
    
    # Slide 4: Data Table
    slide4 = api.add_slide(presentation_id, 'BLANK')
    if slide4:
        api.add_title(presentation_id, slide4, "Performance Metrics")
        api.create_styled_table(
            presentation_id, slide4,
            [
                ['Feature', 'Before', 'After', 'Improvement'],
                ['Load Time', '2.5s', '1.8s', '28%'],
                ['Memory Usage', '45MB', '32MB', '29%'],
                ['API Calls', '15', '8', '47%'],
                ['Error Rate', '5%', '0.5%', '90%']
            ]
        )
    
    # Slide 5: Shapes Demo
    slide5 = api.add_slide(presentation_id, 'BLANK')
    if slide5:
        api.add_title(presentation_id, slide5, "Modern Shape Styling")
        
        # Add shapes with different colors
        y_pos = 150
        shapes = [
            ('RECTANGLE', THEME_COLORS['primary'], "Primary"),
            ('ELLIPSE', THEME_COLORS['accent'], "Accent"),
            ('TRIANGLE', THEME_COLORS['success'], "Success")
        ]
        
        for i, (shape_type, color, label) in enumerate(shapes):
            x_pos = 90 + i * 200
            api.add_shape_styled(
                presentation_id, slide5, shape_type,
                x=x_pos, y=y_pos, width=120, height=120,
                fill_color=color
            )
            # Position label below shape
            label_width = 120
            label_x = x_pos
            api.add_text_box_smart(
                presentation_id, slide5, label,
                position='left',
                margin_top=y_pos + 140,
                width_percent=0.15,
                font_size=FONT_SIZES['caption'],
                alignment='CENTER'
            )
    
    print(f"\n✅ Professional presentation created!")
    print(f"📎 View at: https://docs.google.com/presentation/d/{presentation_id}/edit")
    print("\n💡 Improvements demonstrated:")
    print("   - Professional margins and spacing")
    print("   - Auto-sized text boxes")
    print("   - Consistent color palette")
    print("   - Modern shadows and styling")
    print("   - Improved table formatting")
    print("   - Better two-column layouts")


if __name__ == '__main__':
    create_professional_demo()
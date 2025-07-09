#!/usr/bin/env python3
"""
Advanced Google Slides API Examples
Demonstrates more complex operations like formatting, images, tables, etc.
"""

import os
from test_google_slides import GoogleSlidesAPI
from datetime import datetime


class AdvancedSlidesExamples(GoogleSlidesAPI):
    def add_formatted_text(self, presentation_id, page_id, text, x=100, y=100, 
                          font_size=14, bold=False, italic=False, color=None):
        """Add formatted text to a slide"""
        try:
            element_id = f'formatted_text_{int(datetime.now().timestamp())}'
            
            requests = [
                {
                    'createShape': {
                        'objectId': element_id,
                        'shapeType': 'TEXT_BOX',
                        'elementProperties': {
                            'pageObjectId': page_id,
                            'size': {
                                'width': {'magnitude': 300, 'unit': 'PT'},
                                'height': {'magnitude': 50, 'unit': 'PT'}
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
            
            # Add text style updates
            style_updates = {
                'objectId': element_id,
                'style': {
                    'fontSize': {'magnitude': font_size, 'unit': 'PT'},
                    'bold': bold,
                    'italic': italic
                },
                'fields': 'fontSize,bold,italic'
            }
            
            if color:
                style_updates['style']['foregroundColor'] = {
                    'opaqueColor': {
                        'rgbColor': color
                    }
                }
                style_updates['fields'] += ',foregroundColor'
            
            requests.append({'updateTextStyle': style_updates})
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'Added formatted text: "{text}"')
            return element_id
        
        except Exception as error:
            print(f'An error occurred: {error}')
            return None
    
    def create_table(self, presentation_id, page_id, rows=3, columns=3, x=50, y=50):
        """Create a table on a slide"""
        try:
            table_id = f'table_{int(datetime.now().timestamp())}'
            
            requests = [{
                'createTable': {
                    'objectId': table_id,
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'width': {'magnitude': 400, 'unit': 'PT'},
                            'height': {'magnitude': 200, 'unit': 'PT'}
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
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'Created {rows}x{columns} table')
            return table_id
        
        except Exception as error:
            print(f'An error occurred: {error}')
            return None
    
    def fill_table_cell(self, presentation_id, table_id, row, column, text):
        """Fill a specific cell in a table"""
        try:
            requests = [{
                'insertText': {
                    'objectId': table_id,
                    'cellLocation': {
                        'rowIndex': row,
                        'columnIndex': column
                    },
                    'text': text,
                    'insertionIndex': 0
                }
            }]
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'Filled cell [{row},{column}] with "{text}"')
            return True
        
        except Exception as error:
            print(f'An error occurred: {error}')
            return False
    
    def add_bullet_list(self, presentation_id, page_id, items, x=50, y=50):
        """Add a bulleted list to a slide"""
        try:
            element_id = f'bullet_list_{int(datetime.now().timestamp())}'
            
            # Create text box
            requests = [{
                'createShape': {
                    'objectId': element_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'width': {'magnitude': 400, 'unit': 'PT'},
                            'height': {'magnitude': 200, 'unit': 'PT'}
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
            
            # Add text with line breaks
            text = '\\n'.join(items)
            requests.append({
                'insertText': {
                    'objectId': element_id,
                    'text': text,
                    'insertionIndex': 0
                }
            })
            
            # Apply bullet formatting
            start_index = 0
            for i, item in enumerate(items):
                end_index = start_index + len(item)
                
                requests.append({
                    'createParagraphBullets': {
                        'objectId': element_id,
                        'textRange': {
                            'startIndex': start_index,
                            'endIndex': end_index
                        },
                        'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                    }
                })
                
                start_index = end_index + 1  # +1 for newline
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'Added bullet list with {len(items)} items')
            return element_id
        
        except Exception as error:
            print(f'An error occurred: {error}')
            return None
    
    def add_shape(self, presentation_id, page_id, shape_type='RECTANGLE', 
                  x=100, y=100, width=200, height=100, color=None):
        """Add a shape to a slide"""
        try:
            shape_id = f'shape_{int(datetime.now().timestamp())}'
            
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
            
            # Add color if specified
            if color:
                requests.append({
                    'updateShapeProperties': {
                        'objectId': shape_id,
                        'shapeProperties': {
                            'shapeBackgroundFill': {
                                'solidFill': {
                                    'color': {
                                        'rgbColor': color
                                    }
                                }
                            }
                        },
                        'fields': 'shapeBackgroundFill'
                    }
                })
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'Added {shape_type} shape')
            return shape_id
        
        except Exception as error:
            print(f'An error occurred: {error}')
            return None
    
    def duplicate_slide(self, presentation_id, slide_id):
        """Duplicate an existing slide"""
        try:
            requests = [{
                'duplicateObject': {
                    'objectId': slide_id
                }
            }]
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            new_slide_id = response.get('replies')[0].get('duplicateObject').get('objectId')
            print(f'Duplicated slide. New slide ID: {new_slide_id}')
            return new_slide_id
        
        except Exception as error:
            print(f'An error occurred: {error}')
            return None
    
    def update_slide_properties(self, presentation_id, page_id, background_color=None):
        """Update slide properties like background color"""
        try:
            requests = []
            
            if background_color:
                requests.append({
                    'updatePageProperties': {
                        'objectId': page_id,
                        'pageProperties': {
                            'pageBackgroundFill': {
                                'solidFill': {
                                    'color': {
                                        'rgbColor': background_color
                                    }
                                }
                            }
                        },
                        'fields': 'pageBackgroundFill'
                    }
                })
            
            if requests:
                response = self.service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={'requests': requests}
                ).execute()
                
                print('Updated slide properties')
                return True
            
            return False
        
        except Exception as error:
            print(f'An error occurred: {error}')
            return False


def main():
    """Demonstrate advanced Google Slides API operations"""
    print("Advanced Google Slides API Examples")
    print("=" * 50)
    
    # Initialize API
    api = AdvancedSlidesExamples()
    
    if not api.service:
        print("Failed to authenticate. Please check your credentials.")
        return
    
    # Create a new presentation
    print("\\n1. Creating presentation...")
    presentation_id = api.create_presentation(f'Advanced API Test - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    
    if not presentation_id:
        print("Failed to create presentation")
        return
    
    # Add slides with different layouts
    print("\\n2. Adding slides...")
    slide1_id = api.add_slide(presentation_id, 'BLANK')
    slide2_id = api.add_slide(presentation_id, 'BLANK')
    slide3_id = api.add_slide(presentation_id, 'BLANK')
    
    # Slide 1: Formatted text and shapes
    if slide1_id:
        print("\\n3. Adding formatted content to Slide 1...")
        
        # Add title
        api.add_formatted_text(
            presentation_id, slide1_id, 
            "Formatted Text Examples", 
            x=50, y=30, font_size=24, bold=True,
            color={'red': 0.2, 'green': 0.4, 'blue': 0.8}
        )
        
        # Add colored shapes
        api.add_shape(
            presentation_id, slide1_id, 'RECTANGLE',
            x=50, y=100, width=100, height=50,
            color={'red': 0.9, 'green': 0.2, 'blue': 0.2}
        )
        
        api.add_shape(
            presentation_id, slide1_id, 'ELLIPSE',
            x=200, y=100, width=100, height=100,
            color={'red': 0.2, 'green': 0.9, 'blue': 0.2}
        )
        
        api.add_shape(
            presentation_id, slide1_id, 'TRIANGLE',
            x=350, y=100, width=100, height=100,
            color={'red': 0.2, 'green': 0.2, 'blue': 0.9}
        )
    
    # Slide 2: Table
    if slide2_id:
        print("\\n4. Adding table to Slide 2...")
        
        # Add title
        api.add_text_box(presentation_id, slide2_id, "Table Example", 50, 30, 400, 40)
        
        # Create and fill table
        table_id = api.create_table(presentation_id, slide2_id, rows=3, columns=4, x=50, y=100)
        if table_id:
            # Fill header row
            headers = ['Name', 'Department', 'Role', 'Status']
            for col, header in enumerate(headers):
                api.fill_table_cell(presentation_id, table_id, 0, col, header)
            
            # Fill data rows
            data = [
                ['John Doe', 'Engineering', 'Developer', 'Active'],
                ['Jane Smith', 'Marketing', 'Manager', 'Active']
            ]
            for row_idx, row_data in enumerate(data, 1):
                for col_idx, cell_data in enumerate(row_data):
                    api.fill_table_cell(presentation_id, table_id, row_idx, col_idx, cell_data)
    
    # Slide 3: Bullet list
    if slide3_id:
        print("\\n5. Adding bullet list to Slide 3...")
        
        # Change background color
        api.update_slide_properties(
            presentation_id, slide3_id,
            background_color={'red': 0.95, 'green': 0.95, 'blue': 0.95}
        )
        
        # Add title
        api.add_text_box(presentation_id, slide3_id, "Key Features", 50, 30, 400, 40)
        
        # Add bullet list
        items = [
            'Create presentations programmatically',
            'Add and format text, shapes, and tables',
            'Customize slide layouts and themes',
            'Batch update multiple elements',
            'Read and modify existing presentations'
        ]
        api.add_bullet_list(presentation_id, slide3_id, items, x=50, y=100)
    
    # Print presentation URL
    print(f"\\n✅ Advanced examples completed!")
    print(f"View your presentation at: https://docs.google.com/presentation/d/{presentation_id}/edit")


if __name__ == '__main__':
    main()
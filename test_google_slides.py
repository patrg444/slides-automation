#!/usr/bin/env python3
"""
Google Slides API Test Script
This script demonstrates various operations with the Google Slides API
"""

import os
import json
from datetime import datetime
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


class GoogleSlidesAPI:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Handle authentication for Google Slides API"""
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
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
            
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        
        self.service = build('slides', 'v1', credentials=self.creds)
        return True
    
    def create_presentation(self, title):
        """Create a new presentation"""
        try:
            presentation = {
                'title': title
            }
            
            presentation = self.service.presentations().create(
                body=presentation).execute()
            
            print(f'Created presentation with ID: {presentation.get("presentationId")}')
            return presentation.get('presentationId')
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
    def add_slide(self, presentation_id, layout='BLANK'):
        """Add a new slide to the presentation"""
        try:
            requests = [{
                'createSlide': {
                    'slideLayoutReference': {
                        'predefinedLayout': layout
                    }
                }
            }]
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            slide_id = response.get('replies')[0].get('createSlide').get('objectId')
            print(f'Added slide with ID: {slide_id}')
            return slide_id
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
    def add_text_box(self, presentation_id, page_id, text, x=100, y=100, width=300, height=50):
        """Add a text box to a slide"""
        try:
            element_id = f'textbox_{int(datetime.now().timestamp())}'
            pt350 = {
                'magnitude': 350,
                'unit': 'PT'
            }
            
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
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'Added text box: "{text}"')
            return element_id
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
    def update_text(self, presentation_id, object_id, new_text):
        """Update text in an existing text box"""
        try:
            requests = [
                {
                    'deleteText': {
                        'objectId': object_id,
                        'textRange': {
                            'type': 'ALL'
                        }
                    }
                },
                {
                    'insertText': {
                        'objectId': object_id,
                        'text': new_text,
                        'insertionIndex': 0
                    }
                }
            ]
            
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f'Updated text to: "{new_text}"')
            return True
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return False
    
    def get_presentation(self, presentation_id):
        """Get presentation details"""
        try:
            presentation = self.service.presentations().get(
                presentationId=presentation_id
            ).execute()
            
            return presentation
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
    def list_slides(self, presentation_id):
        """List all slides in a presentation"""
        presentation = self.get_presentation(presentation_id)
        
        if presentation:
            slides = presentation.get('slides', [])
            print(f'\\nPresentation has {len(slides)} slides:')
            
            for i, slide in enumerate(slides):
                print(f'  Slide {i+1}: {slide.get("objectId")}')
                
                # List elements on each slide
                elements = slide.get('pageElements', [])
                if elements:
                    print(f'    Elements: {len(elements)}')
                    for elem in elements:
                        if 'shape' in elem and elem['shape'].get('shapeType') == 'TEXT_BOX':
                            text_content = elem.get('shape', {}).get('text', {}).get('textElements', [])
                            if text_content:
                                text = ''.join([t.get('textRun', {}).get('content', '') 
                                              for t in text_content if 'textRun' in t])
                                print(f'      - Text box: "{text.strip()}"')
            
            return slides
        
        return []


def main():
    """Main function to demonstrate Google Slides API operations"""
    print("Google Slides API Test")
    print("=" * 50)
    
    # Initialize API
    api = GoogleSlidesAPI()
    
    if not api.service:
        print("Failed to authenticate. Please check your credentials.")
        return
    
    # Check for test presentation ID in environment
    test_presentation_id = os.getenv('TEST_PRESENTATION_ID')
    
    if test_presentation_id:
        print(f"\\nUsing existing presentation: {test_presentation_id}")
        presentation_id = test_presentation_id
    else:
        # Create a new presentation
        print("\\n1. Creating new presentation...")
        presentation_id = api.create_presentation(f'API Test - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        
        if not presentation_id:
            print("Failed to create presentation")
            return
    
    # Add slides
    print("\\n2. Adding slides...")
    slide1_id = api.add_slide(presentation_id, 'TITLE_AND_BODY')
    slide2_id = api.add_slide(presentation_id, 'BLANK')
    
    # Add text boxes
    print("\\n3. Adding text boxes...")
    if slide1_id:
        api.add_text_box(presentation_id, slide1_id, "Welcome to Google Slides API!", 100, 50, 400, 60)
        api.add_text_box(presentation_id, slide1_id, "This is a test presentation", 100, 150, 400, 40)
    
    if slide2_id:
        text_box_id = api.add_text_box(presentation_id, slide2_id, "Initial text", 50, 50, 300, 50)
        
        # Update text
        if text_box_id:
            print("\\n4. Updating text...")
            api.update_text(presentation_id, text_box_id, "Updated text via API!")
    
    # List slides and content
    print("\\n5. Listing presentation content...")
    api.list_slides(presentation_id)
    
    # Print presentation URL
    print(f"\\n✅ Test completed successfully!")
    print(f"View your presentation at: https://docs.google.com/presentation/d/{presentation_id}/edit")


if __name__ == '__main__':
    main()
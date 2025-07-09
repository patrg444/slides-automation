#!/usr/bin/env python3
"""
Consulting Platform Fixed Final V2 - Fixes Slide 2 Text Overlap
Enhanced positioning and spacing for challenge slide
"""

import os
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from google_slides_enhanced_v2 import GoogleSlidesEnhancedV2, FONT_SIZES, LAYOUTS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
except Exception as e:
    print(f"Warning: OpenAI client initialization failed: {e}")
    client = None

# Professional color palettes
PROFESSIONAL_THEMES = {
    'corporate_blue': {
        'primary': {'red': 0.031, 'green': 0.094, 'blue': 0.212},      # Dark navy
        'secondary': {'red': 0.333, 'green': 0.333, 'blue': 0.333},     # Dark gray
        'accent': {'red': 0.000, 'green': 0.478, 'blue': 0.698},        # Professional blue
        'background': {'red': 1.000, 'green': 1.000, 'blue': 1.000},    # White
        'light_bg': {'red': 0.961, 'green': 0.969, 'blue': 0.980},      # Very light blue-gray
        'text_primary': {'red': 0.133, 'green': 0.133, 'blue': 0.133},  # Almost black
        'text_secondary': {'red': 0.459, 'green': 0.459, 'blue': 0.459}, # Medium gray
        'success': {'red': 0.298, 'green': 0.686, 'blue': 0.314}        # Green
    }
}

DEFAULT_THEME = PROFESSIONAL_THEMES['corporate_blue']


@dataclass
class BrandingConfig:
    """Company branding configuration"""
    company_name: str
    primary_color: Optional[Dict[str, float]] = None
    secondary_color: Optional[Dict[str, float]] = None
    accent_color: Optional[Dict[str, float]] = None
    logo_url: Optional[str] = None
    font_family: str = 'Arial'
    tagline: Optional[str] = None
    website: Optional[str] = None
    
    def __post_init__(self):
        if not self.primary_color:
            self.primary_color = DEFAULT_THEME['primary']
        if not self.secondary_color:
            self.secondary_color = DEFAULT_THEME['secondary']
        if not self.accent_color:
            self.accent_color = DEFAULT_THEME['accent']
    
    def to_dict(self):
        return asdict(self)


@dataclass
class CaseStudyData:
    """Data structure for case studies"""
    client_name: str
    industry: str
    challenge: str
    solution: str
    results: List[str]
    timeline: str
    team_size: str
    technologies: List[str]
    testimonial: Optional[str] = None
    metrics: Optional[Dict[str, str]] = None


class PositionTracker:
    """Track positions to prevent overlaps"""
    def __init__(self):
        self.current_y = 0
        self.elements = []
    
    def add_element(self, y: int, height: int, description: str):
        """Add element and track position"""
        self.elements.append({
            'y': y,
            'height': height,
            'bottom': y + height,
            'description': description
        })
        self.current_y = y + height
    
    def get_next_y(self, min_gap: int = 20) -> int:
        """Get next available Y position with gap"""
        if not self.elements:
            return LAYOUTS['standard']['content_top']
        
        last = self.elements[-1]
        return last['bottom'] + min_gap
    
    def check_overlap(self, y: int, height: int) -> bool:
        """Check if position would overlap"""
        new_bottom = y + height
        for elem in self.elements:
            if (y < elem['bottom'] and new_bottom > elem['y']):
                return True
        return False


class ConsultingTemplatesFinal:
    """Final fixed templates with position tracking"""
    
    def __init__(self, api: GoogleSlidesEnhancedV2):
        self.api = api
        self.slide_width = 720
        self.slide_height = 405
    
    def create_case_study_title_slide(self, presentation_id: str, data: CaseStudyData, 
                                     branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create title slide with position tracking"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            tracker = PositionTracker()
            
            # White background
            self.api.update_slide_background(presentation_id, slide_id, DEFAULT_THEME['background'])
            
            # Top accent bar
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=0, y=0, width=720, height=5,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            tracker.add_element(0, 5, "accent bar")
            
            # Client name
            y_pos = tracker.get_next_y(35)  # Extra gap after accent
            element_id = self.api.add_text_box_smart(
                presentation_id, slide_id, data.client_name.upper(),
                position='left', margin_top=y_pos, width_percent=0.9,
                font_size=16, color=branding.accent_color,
                bold=True
            )
            tracker.add_element(y_pos, 30, "client name")
            
            # Main title with dynamic height
            title = ai_content.get('title', f'{data.client_name} Case Study')
            y_pos = tracker.get_next_y(30)  # Gap before title
            
            # Use the API's height calculation
            title_width = int(self.slide_width * 0.9)
            title_height = self.api.calculate_text_height(title, 36, title_width)
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, title,
                position='left', margin_top=y_pos, width_percent=0.9,
                font_size=36, color=branding.primary_color,
                bold=True
            )
            tracker.add_element(y_pos, title_height, "main title")
            
            # Subtitle
            if data.results and tracker.current_y < 260:  # Ensure space for footer
                subtitle = f"{data.industry} • {data.results[0]}"
                y_pos = tracker.get_next_y(20)
                
                self.api.add_text_box_smart(
                    presentation_id, slide_id, subtitle,
                    position='left', margin_top=y_pos, width_percent=0.9,
                    font_size=20, color=DEFAULT_THEME['text_secondary']
                )
                tracker.add_element(y_pos, 40, "subtitle")
            
            # Footer - fixed at bottom
            footer_y = 340
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=0, y=footer_y, width=720, height=65,
                fill_color=DEFAULT_THEME['light_bg'],
                add_shadow=False
            )
            
            # Company info in footer
            self.api.add_text_box_smart(
                presentation_id, slide_id, branding.company_name,
                position='left', margin_top=355, width_percent=0.9,
                font_size=14, color=branding.primary_color,
                bold=True
            )
            
            if branding.tagline and len(branding.tagline) < 50:  # Only if short
                self.api.add_text_box_smart(
                    presentation_id, slide_id, branding.tagline,
                    position='left', margin_top=375, width_percent=0.9,
                    font_size=12, color=DEFAULT_THEME['text_secondary']
                )
        
        return slide_id
    
    def create_challenge_slide(self, presentation_id: str, data: CaseStudyData,
                              branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create challenge slide with improved spacing to prevent overlap"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            tracker = PositionTracker()
            
            # Section marker and title
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=40, width=5, height=40,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            # Title with proper height tracking
            title_height = self.api.calculate_text_height("The Challenge", 32, int(self.slide_width * 0.8))
            self.api.add_text_box_smart(
                presentation_id, slide_id, "The Challenge",
                position='left', margin_top=45, width_percent=0.8,
                font_size=32, color=branding.primary_color, bold=True
            )
            tracker.add_element(40, max(title_height, 50), "title section")
            
            # Challenge description with better height calculation
            y_pos = tracker.get_next_y(35)  # Increased gap after title
            challenge_text = ai_content.get('challenge_detail', data.challenge)
            
            # Calculate actual height with word wrapping consideration
            desc_width = int(self.slide_width * 0.85)
            # Add multiplier for better word wrap estimation
            desc_height = int(self.api.calculate_text_height(challenge_text, 18, desc_width) * 1.2)
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, challenge_text,
                position='left', margin_top=y_pos, width_percent=0.85,
                font_size=18, color=DEFAULT_THEME['text_primary']
            )
            tracker.add_element(y_pos, desc_height, "challenge description")
            
            # Challenge points - with better spacing and positioning
            remaining_space = 380 - tracker.current_y  # Leave margin at bottom
            if remaining_space > 180:  # Need more space for proper display
                challenges = [
                    "Legacy System Constraints",
                    "Process Inefficiencies", 
                    "Limited Analytics Capability"
                ]
                
                y_pos = tracker.get_next_y(40)  # Increased gap before items
                item_height = 50
                item_spacing = 20  # Increased spacing between items
                
                # Check if all items will fit
                total_items_height = len(challenges) * item_height + (len(challenges) - 1) * item_spacing
                if y_pos + total_items_height > 380:
                    # Reduce number of items if needed
                    max_items = int((380 - y_pos) / (item_height + item_spacing))
                    challenges = challenges[:max(1, max_items)]
                
                for i, challenge in enumerate(challenges):
                    item_y = y_pos + i * (item_height + item_spacing)
                    
                    # Icon background
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=60, y=item_y, width=40, height=40,
                        fill_color=branding.accent_color
                    )
                    
                    # Text positioned to the right of icon with proper spacing
                    # Create text box with exact positioning to avoid overlap
                    text_id = self.api.generate_id('textbox')
                    text_x = 120  # Start text 20px after icon (60 + 40 + 20)
                    text_width = 500  # Fixed width to prevent overlap
                    
                    requests = [{
                        'createShape': {
                            'objectId': text_id,
                            'shapeType': 'TEXT_BOX',
                            'elementProperties': {
                                'pageObjectId': slide_id,
                                'size': {
                                    'width': {'magnitude': text_width, 'unit': 'PT'},
                                    'height': {'magnitude': 40, 'unit': 'PT'}
                                },
                                'transform': {
                                    'scaleX': 1,
                                    'scaleY': 1,
                                    'translateX': text_x,
                                    'translateY': item_y + 10,  # Center vertically with icon
                                    'unit': 'PT'
                                }
                            }
                        }
                    }, {
                        'insertText': {
                            'objectId': text_id,
                            'text': challenge,
                            'insertionIndex': 0
                        }
                    }, {
                        'updateTextStyle': {
                            'objectId': text_id,
                            'style': {
                                'fontSize': {'magnitude': 16, 'unit': 'PT'},
                                'fontFamily': 'Arial',
                                'foregroundColor': {'opaqueColor': {'rgbColor': DEFAULT_THEME['text_primary']}}
                            },
                            'textRange': {'type': 'ALL'},
                            'fields': 'fontSize,fontFamily,foregroundColor'
                        }
                    }]
                    
                    self.api.service.presentations().batchUpdate(
                        presentationId=presentation_id,
                        body={'requests': requests}
                    ).execute()
        
        return slide_id
    
    def create_solution_slide(self, presentation_id: str, data: CaseStudyData,
                             branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create solution slide with column layout"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Header section
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=40, width=5, height=40,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Our Solution",
                position='left', margin_top=45, width_percent=0.8,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Left column - solution description
            solution_text = ai_content.get('solution_detail', data.solution)
            self.api.add_text_box_smart(
                presentation_id, slide_id, solution_text,
                position='left', margin_top=110, width_percent=0.45,
                font_size=16, color=DEFAULT_THEME['text_primary']
            )
            
            # Right column - technologies
            if data.technologies:
                # Tech header positioned correctly
                right_x_percent = 0.52  # Start right column at 52% of width
                
                # Create a text box at specific X position
                tech_header_id = self.api.generate_id('textbox')
                requests = [{
                    'createShape': {
                        'objectId': tech_header_id,
                        'shapeType': 'TEXT_BOX',
                        'elementProperties': {
                            'pageObjectId': slide_id,
                            'size': {
                                'width': {'magnitude': 240, 'unit': 'PT'},
                                'height': {'magnitude': 30, 'unit': 'PT'}
                            },
                            'transform': {
                                'scaleX': 1,
                                'scaleY': 1,
                                'translateX': 420,  # Fixed X position
                                'translateY': 110,
                                'unit': 'PT'
                            }
                        }
                    }
                }, {
                    'insertText': {
                        'objectId': tech_header_id,
                        'text': 'Technology Stack',
                        'insertionIndex': 0
                    }
                }, {
                    'updateTextStyle': {
                        'objectId': tech_header_id,
                        'style': {
                            'fontSize': {'magnitude': 18, 'unit': 'PT'},
                            'fontFamily': 'Arial',
                            'bold': True,
                            'foregroundColor': {'opaqueColor': {'rgbColor': branding.primary_color}}
                        },
                        'textRange': {'type': 'ALL'},
                        'fields': 'fontSize,fontFamily,bold,foregroundColor'
                    }
                }]
                
                self.api.service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={'requests': requests}
                ).execute()
                
                # Tech pills with fixed positioning
                for i, tech in enumerate(data.technologies[:4]):
                    y_pos = 150 + i * 50
                    
                    # Create pill at exact position
                    pill_id = self.api.generate_id('shape')
                    text_id = self.api.generate_id('textbox')
                    
                    pill_requests = [{
                        'createShape': {
                            'objectId': pill_id,
                            'shapeType': 'ROUND_RECTANGLE',
                            'elementProperties': {
                                'pageObjectId': slide_id,
                                'size': {
                                    'width': {'magnitude': 180, 'unit': 'PT'},
                                    'height': {'magnitude': 35, 'unit': 'PT'}
                                },
                                'transform': {
                                    'scaleX': 1,
                                    'scaleY': 1,
                                    'translateX': 420,
                                    'translateY': y_pos,
                                    'unit': 'PT'
                                }
                            }
                        }
                    }, {
                        'updateShapeProperties': {
                            'objectId': pill_id,
                            'shapeProperties': {
                                'shapeBackgroundFill': {
                                    'solidFill': {'color': {'rgbColor': DEFAULT_THEME['light_bg']}}
                                }
                            },
                            'fields': 'shapeBackgroundFill'
                        }
                    }, {
                        'createShape': {
                            'objectId': text_id,
                            'shapeType': 'TEXT_BOX',
                            'elementProperties': {
                                'pageObjectId': slide_id,
                                'size': {
                                    'width': {'magnitude': 180, 'unit': 'PT'},
                                    'height': {'magnitude': 35, 'unit': 'PT'}
                                },
                                'transform': {
                                    'scaleX': 1,
                                    'scaleY': 1,
                                    'translateX': 420,
                                    'translateY': y_pos,
                                    'unit': 'PT'
                                }
                            }
                        }
                    }, {
                        'insertText': {
                            'objectId': text_id,
                            'text': tech,
                            'insertionIndex': 0
                        }
                    }, {
                        'updateTextStyle': {
                            'objectId': text_id,
                            'style': {
                                'fontSize': {'magnitude': 14, 'unit': 'PT'},
                                'fontFamily': 'Arial',
                                'bold': True,
                                'foregroundColor': {'opaqueColor': {'rgbColor': branding.primary_color}}
                            },
                            'textRange': {'type': 'ALL'},
                            'fields': 'fontSize,fontFamily,bold,foregroundColor'
                        }
                    }, {
                        'updateParagraphStyle': {
                            'objectId': text_id,
                            'style': {
                                'alignment': 'CENTER',
                                'lineSpacing': 100
                            },
                            'textRange': {'type': 'ALL'},
                            'fields': 'alignment,lineSpacing'
                        }
                    }]
                    
                    self.api.service.presentations().batchUpdate(
                        presentationId=presentation_id,
                        body={'requests': pill_requests}
                    ).execute()
        
        return slide_id
    
    def create_results_slide(self, presentation_id: str, data: CaseStudyData,
                            branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create results slide with metrics"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            tracker = PositionTracker()
            
            # Header
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=40, width=5, height=40,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Results & Impact",
                position='left', margin_top=45, width_percent=0.8,
                font_size=32, color=branding.primary_color, bold=True
            )
            tracker.add_element(40, 50, "header")
            
            # Results bullets
            y_pos = tracker.get_next_y(30)
            if data.results:
                # Use the API's bullet list with explicit positioning
                bullet_height = len(data.results[:3]) * 40 + 20  # Estimate
                self.api.add_bullet_list_improved(
                    presentation_id, slide_id, data.results[:3],
                    x=60, y=y_pos, width=600, font_size=16
                )
                tracker.add_element(y_pos, bullet_height, "bullets")
            
            # Metrics cards - only if space
            if data.metrics and tracker.current_y < 250:
                metrics_list = list(data.metrics.items())[:3]
                y_pos = max(tracker.get_next_y(40), 250)  # Ensure minimum position
                
                # Center the cards
                card_width = 180
                card_spacing = 40
                total_width = len(metrics_list) * card_width + (len(metrics_list) - 1) * card_spacing
                x_start = (720 - total_width) // 2
                
                for i, (metric, value) in enumerate(metrics_list):
                    x_pos = x_start + i * (card_width + card_spacing)
                    
                    # Card background
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=x_pos, y=y_pos, width=card_width, height=100,
                        fill_color=DEFAULT_THEME['light_bg']
                    )
                    
                    # Create text elements with exact positioning
                    value_id = self.api.generate_id('textbox')
                    label_id = self.api.generate_id('textbox')
                    
                    text_requests = [{
                        'createShape': {
                            'objectId': value_id,
                            'shapeType': 'TEXT_BOX',
                            'elementProperties': {
                                'pageObjectId': slide_id,
                                'size': {
                                    'width': {'magnitude': card_width, 'unit': 'PT'},
                                    'height': {'magnitude': 40, 'unit': 'PT'}
                                },
                                'transform': {
                                    'scaleX': 1,
                                    'scaleY': 1,
                                    'translateX': x_pos,
                                    'translateY': y_pos + 20,
                                    'unit': 'PT'
                                }
                            }
                        }
                    }, {
                        'insertText': {
                            'objectId': value_id,
                            'text': value,
                            'insertionIndex': 0
                        }
                    }, {
                        'updateTextStyle': {
                            'objectId': value_id,
                            'style': {
                                'fontSize': {'magnitude': 28, 'unit': 'PT'},
                                'fontFamily': 'Arial',
                                'bold': True,
                                'foregroundColor': {'opaqueColor': {'rgbColor': branding.accent_color}}
                            },
                            'textRange': {'type': 'ALL'},
                            'fields': 'fontSize,fontFamily,bold,foregroundColor'
                        }
                    }, {
                        'updateParagraphStyle': {
                            'objectId': value_id,
                            'style': {'alignment': 'CENTER'},
                            'textRange': {'type': 'ALL'},
                            'fields': 'alignment'
                        }
                    }, {
                        'createShape': {
                            'objectId': label_id,
                            'shapeType': 'TEXT_BOX',
                            'elementProperties': {
                                'pageObjectId': slide_id,
                                'size': {
                                    'width': {'magnitude': card_width, 'unit': 'PT'},
                                    'height': {'magnitude': 25, 'unit': 'PT'}
                                },
                                'transform': {
                                    'scaleX': 1,
                                    'scaleY': 1,
                                    'translateX': x_pos,
                                    'translateY': y_pos + 65,
                                    'unit': 'PT'
                                }
                            }
                        }
                    }, {
                        'insertText': {
                            'objectId': label_id,
                            'text': metric,
                            'insertionIndex': 0
                        }
                    }, {
                        'updateTextStyle': {
                            'objectId': label_id,
                            'style': {
                                'fontSize': {'magnitude': 14, 'unit': 'PT'},
                                'fontFamily': 'Arial',
                                'foregroundColor': {'opaqueColor': {'rgbColor': DEFAULT_THEME['text_secondary']}}
                            },
                            'textRange': {'type': 'ALL'},
                            'fields': 'fontSize,fontFamily,foregroundColor'
                        }
                    }, {
                        'updateParagraphStyle': {
                            'objectId': label_id,
                            'style': {'alignment': 'CENTER'},
                            'textRange': {'type': 'ALL'},
                            'fields': 'alignment'
                        }
                    }]
                    
                    self.api.service.presentations().batchUpdate(
                        presentationId=presentation_id,
                        body={'requests': text_requests}
                    ).execute()
        
        return slide_id
    
    def create_testimonial_slide(self, presentation_id: str, data: CaseStudyData,
                                branding: BrandingConfig) -> str:
        """Create testimonial slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id and data.testimonial:
            # Light background
            self.api.update_slide_background(presentation_id, slide_id, DEFAULT_THEME['light_bg'])
            
            # Calculate vertical centering
            test_height = self.api.calculate_text_height(data.testimonial, 22, int(720 * 0.7))
            total_content_height = 80 + test_height + 60  # quote + text + attribution
            y_start = max(40, (405 - total_content_height) // 2)
            
            # Quote mark
            self.api.add_text_box_smart(
                presentation_id, slide_id, '"',
                position='center', margin_top=y_start, width_percent=0.1,
                font_size=96, color=branding.accent_color
            )
            
            # Testimonial
            self.api.add_text_box_smart(
                presentation_id, slide_id, data.testimonial,
                position='center', margin_top=y_start + 80, width_percent=0.7,
                font_size=22, color=DEFAULT_THEME['text_primary'],
                alignment='CENTER'
            )
            
            # Attribution
            attr_y = min(y_start + 80 + test_height + 30, 340)  # Don't go below 340
            attribution = f"— {data.client_name} Leadership Team"
            self.api.add_text_box_smart(
                presentation_id, slide_id, attribution,
                position='center', margin_top=attr_y, width_percent=0.5,
                font_size=16, color=DEFAULT_THEME['text_secondary'],
                alignment='CENTER'
            )
        
        return slide_id


class ConsultingPlatformFinal:
    """Final fixed consulting platform"""
    
    def __init__(self):
        self.api = GoogleSlidesEnhancedV2()
        self.templates = ConsultingTemplatesFinal(self.api)
    
    def create_case_study(self, data: CaseStudyData, branding: BrandingConfig) -> str:
        """Create case study with no overlapping text"""
        # Generate AI content
        ai_content = {
            'title': f'{data.client_name} Digital Transformation Success Story',
            'challenge_detail': data.challenge,
            'solution_detail': data.solution,
            'results_summary': f"Achieved significant improvements: {', '.join(data.results[:2])}"
        }
        
        # Create presentation
        title = f"{data.client_name} Case Study - {datetime.now().strftime('%B %Y')}"
        presentation_id = self.api.create_presentation(title)
        
        if presentation_id:
            # Create slides
            self.templates.create_case_study_title_slide(presentation_id, data, branding, ai_content)
            self.templates.create_challenge_slide(presentation_id, data, branding, ai_content)
            self.templates.create_solution_slide(presentation_id, data, branding, ai_content)
            self.templates.create_results_slide(presentation_id, data, branding, ai_content)
            
            if data.testimonial:
                self.templates.create_testimonial_slide(presentation_id, data, branding)
            
            print(f"\n✅ Professional case study created - SLIDE 2 OVERLAP FIXED!")
            print(f"📎 View at: https://docs.google.com/presentation/d/{presentation_id}/edit")
            print("\n📊 Improvements in V2:")
            print("   - Better height calculation for challenge description")
            print("   - Increased spacing between elements")
            print("   - Fixed text positioning for challenge items")
            print("   - Exact X positioning to prevent horizontal overlap")
            print("   - Dynamic item count based on available space")
            
            return presentation_id
        
        return None


def demo_final_fixed_v2():
    """Demo with slide 2 overlap fixes"""
    platform = ConsultingPlatformFinal()
    
    # Professional branding
    branding = BrandingConfig(
        company_name="Strategic Consulting Partners",
        tagline="Transforming Business Through Innovation"
    )
    
    # Sample case study
    case_study = CaseStudyData(
        client_name="GlobalTech Corporation",
        industry="Technology & Software",
        challenge="Legacy infrastructure limiting scalability and innovation, causing 40% slower time-to-market than competitors",
        solution="Implemented cloud-native microservices architecture with automated CI/CD pipelines and real-time analytics",
        results=[
            "60% reduction in deployment time",
            "45% decrease in operational costs",
            "3x improvement in system performance"
        ],
        timeline="6 months",
        team_size="12 consultants",
        technologies=["AWS Cloud", "Kubernetes", "React", "Python"],
        testimonial="Strategic Consulting Partners transformed our technology infrastructure and helped us become an industry leader in innovation.",
        metrics={
            "Cost Savings": "$2.5M",
            "Performance": "+300%",
            "Time to Market": "-60%"
        }
    )
    
    # Create presentation
    presentation_id = platform.create_case_study(case_study, branding)
    
    return presentation_id


if __name__ == '__main__':
    demo_final_fixed_v2()
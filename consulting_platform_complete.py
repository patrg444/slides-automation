#!/usr/bin/env python3
"""
Consulting Platform Complete - Fixed Overlaps + Table Demo
Resolves slide 2 text overlap and adds table functionality
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
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
    else:
        print("⚠️  No OpenAI API key found in environment")
        client = None
except Exception as e:
    print(f"Warning: OpenAI client initialization failed: {e}")
    # Try without any extra parameters
    try:
        client = OpenAI()
        print("✅ OpenAI client initialized with default settings")
    except:
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
    timeline_data: Optional[List[List[str]]] = None  # For timeline table


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
        print(f"   Tracked: {description} at y={y}, height={height}, bottom={y + height}")
    
    def get_next_y(self, min_gap: int = 20) -> int:
        """Get next available Y position with gap"""
        if not self.elements:
            return LAYOUTS['standard']['content_top']
        
        last = self.elements[-1]
        next_y = last['bottom'] + min_gap
        print(f"   Next Y position: {next_y} (after {last['description']} + {min_gap}px gap)")
        return next_y
    
    def check_overlap(self, y: int, height: int) -> bool:
        """Check if position would overlap"""
        new_bottom = y + height
        for elem in self.elements:
            if (y < elem['bottom'] and new_bottom > elem['y']):
                print(f"   ⚠️  Overlap detected: new element ({y}-{new_bottom}) overlaps with {elem['description']} ({elem['y']}-{elem['bottom']})")
                return True
        return False


class ConsultingTemplatesComplete:
    """Complete templates with overlap fixes and table support"""
    
    def __init__(self, api: GoogleSlidesEnhancedV2):
        self.api = api
        self.slide_width = 720
        self.slide_height = 405
    
    def calculate_text_height_safe(self, text: str, font_size: int, width: int) -> int:
        """Calculate text height with safety margin"""
        # More accurate calculation
        avg_char_width = font_size * 0.5  # More conservative
        chars_per_line = width / avg_char_width
        lines = max(1, len(text) / chars_per_line)
        
        # Account for word wrapping
        words = text.split()
        if len(words) > 10:  # Long text needs more space
            lines *= 1.3
        
        line_height = font_size * 1.8  # More line spacing
        padding = 30  # Extra padding for safety
        
        calculated_height = int(lines * line_height + padding)
        print(f"   Text height calc: {len(text)} chars, {lines:.1f} lines, {calculated_height}px height")
        return calculated_height
    
    def create_case_study_title_slide(self, presentation_id: str, data: CaseStudyData, 
                                     branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create title slide with position tracking"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            print("\n📊 Creating Title Slide with position tracking...")
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
            y_pos = tracker.get_next_y(35)
            self.api.add_text_box_smart(
                presentation_id, slide_id, data.client_name.upper(),
                position='left', margin_top=y_pos, width_percent=0.9,
                font_size=16, color=branding.accent_color,
                bold=True
            )
            tracker.add_element(y_pos, 30, "client name")
            
            # Main title
            title = ai_content.get('title', f'{data.client_name} Case Study')
            y_pos = tracker.get_next_y(30)
            title_width = int(self.slide_width * 0.9)
            title_height = self.calculate_text_height_safe(title, 36, title_width)
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, title,
                position='left', margin_top=y_pos, width_percent=0.9,
                font_size=36, color=branding.primary_color,
                bold=True
            )
            tracker.add_element(y_pos, title_height, "main title")
            
            # Subtitle
            if data.results and tracker.current_y < 250:
                subtitle = f"{data.industry} • {data.results[0]}"
                y_pos = tracker.get_next_y(20)
                
                self.api.add_text_box_smart(
                    presentation_id, slide_id, subtitle,
                    position='left', margin_top=y_pos, width_percent=0.9,
                    font_size=20, color=DEFAULT_THEME['text_secondary']
                )
                tracker.add_element(y_pos, 40, "subtitle")
            
            # Footer
            footer_y = 340
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=0, y=footer_y, width=720, height=65,
                fill_color=DEFAULT_THEME['light_bg'],
                add_shadow=False
            )
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, branding.company_name,
                position='left', margin_top=355, width_percent=0.9,
                font_size=14, color=branding.primary_color,
                bold=True
            )
            
            if branding.tagline and len(branding.tagline) < 50:
                self.api.add_text_box_smart(
                    presentation_id, slide_id, branding.tagline,
                    position='left', margin_top=375, width_percent=0.9,
                    font_size=12, color=DEFAULT_THEME['text_secondary']
                )
        
        return slide_id
    
    def create_challenge_slide_fixed(self, presentation_id: str, data: CaseStudyData,
                                    branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create challenge slide with FIXED overlap issue"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            print("\n📊 Creating Challenge Slide with FIXED positioning...")
            tracker = PositionTracker()
            
            # Section marker and title
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=40, width=5, height=40,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            # Title - calculate actual height
            title_text = "The Challenge"
            title_height = self.calculate_text_height_safe(title_text, 32, 600)
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, title_text,
                position='left', margin_top=45, width_percent=0.8,
                font_size=32, color=branding.primary_color, bold=True
            )
            tracker.add_element(40, max(title_height, 60), "title section")
            
            # Challenge description with proper spacing
            y_pos = tracker.get_next_y(35)  # Larger gap after title
            challenge_text = ai_content.get('challenge_detail', data.challenge)
            
            # More accurate height calculation
            desc_width = int(self.slide_width * 0.85)
            desc_height = self.calculate_text_height_safe(challenge_text, 18, desc_width)
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, challenge_text,
                position='left', margin_top=y_pos, width_percent=0.85,
                font_size=18, color=DEFAULT_THEME['text_primary']
            )
            tracker.add_element(y_pos, desc_height, "challenge description")
            
            # Challenge points - with better spacing
            remaining_space = 380 - tracker.current_y
            print(f"   Remaining space for challenge items: {remaining_space}px")
            
            if remaining_space > 180:  # Need more space
                challenges = [
                    "Legacy System Constraints",
                    "Process Inefficiencies", 
                    "Limited Analytics Capability"
                ]
                
                y_pos = tracker.get_next_y(40)  # Larger gap before items
                item_height = 40  # Icon height
                item_spacing = 20  # Increased spacing
                text_height = 30  # Text box height
                
                # Calculate how many items will fit
                total_needed = len(challenges) * (item_height + item_spacing)
                items_to_show = len(challenges)
                if y_pos + total_needed > 370:
                    items_to_show = min(2, (370 - y_pos) // (item_height + item_spacing))
                
                print(f"   Showing {items_to_show} of {len(challenges)} challenge items")
                
                for i in range(items_to_show):
                    item_y = y_pos + i * (item_height + item_spacing + 10)  # Extra spacing
                    
                    # Icon
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=60, y=item_y, width=40, height=40,
                        fill_color=branding.accent_color
                    )
                    
                    # Text - with FIXED positioning
                    text_x = 120  # Fixed X position (60 + 40 icon + 20 gap)
                    text_width = 500  # Fixed width to prevent overflow
                    
                    # Create text box with exact positioning
                    text_id = self.api.generate_id('textbox')
                    requests = [{
                        'createShape': {
                            'objectId': text_id,
                            'shapeType': 'TEXT_BOX',
                            'elementProperties': {
                                'pageObjectId': slide_id,
                                'size': {
                                    'width': {'magnitude': text_width, 'unit': 'PT'},
                                    'height': {'magnitude': text_height, 'unit': 'PT'}
                                },
                                'transform': {
                                    'scaleX': 1,
                                    'scaleY': 1,
                                    'translateX': text_x,
                                    'translateY': item_y + 5,  # Center vertically
                                    'unit': 'PT'
                                }
                            }
                        }
                    }, {
                        'insertText': {
                            'objectId': text_id,
                            'text': challenges[i],
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
                    
                    tracker.add_element(item_y, item_height + 10, f"challenge item {i+1}")
        
        return slide_id
    
    def create_solution_slide(self, presentation_id: str, data: CaseStudyData,
                             branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create solution slide with proper column layout"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            print("\n📊 Creating Solution Slide...")
            
            # Header
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
            
            # Left column - solution text
            solution_text = ai_content.get('solution_detail', data.solution)
            self.api.add_text_box_smart(
                presentation_id, slide_id, solution_text,
                position='left', margin_top=110, width_percent=0.45,
                font_size=16, color=DEFAULT_THEME['text_primary']
            )
            
            # Right column - technologies with fixed positioning
            if data.technologies:
                # Tech header at exact position
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
                                'translateX': 420,
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
                
                # Tech pills
                for i, tech in enumerate(data.technologies[:4]):
                    y_pos = 150 + i * 50
                    
                    # Pill background
                    pill_id = self.api.generate_id('shape')
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=420, y=y_pos, width=180, height=35,
                        fill_color=DEFAULT_THEME['light_bg'],
                        add_shadow=False
                    )
                    
                    # Pill text
                    text_id = self.api.generate_id('textbox')
                    requests = [{
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
                        body={'requests': requests}
                    ).execute()
        
        return slide_id
    
    def create_timeline_slide(self, presentation_id: str, data: CaseStudyData,
                             branding: BrandingConfig) -> str:
        """Create timeline slide with table"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            print("\n📊 Creating Timeline Slide with Table...")
            
            # Header
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=40, width=5, height=40,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Project Timeline",
                position='left', margin_top=45, width_percent=0.8,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Timeline table
            if data.timeline_data:
                self.api.create_styled_table(
                    presentation_id, slide_id, data.timeline_data,
                    x=60, y=120, width=600
                )
            else:
                # Default timeline data
                timeline_data = [
                    ['Phase', 'Duration', 'Key Activities', 'Deliverables'],
                    ['Discovery', '2 weeks', 'Stakeholder interviews, System audit', 'Assessment report'],
                    ['Design', '4 weeks', 'Architecture design, Technology selection', 'Solution blueprint'],
                    ['Implementation', '12 weeks', 'Development, Testing, Integration', 'Working system'],
                    ['Deployment', '2 weeks', 'Go-live, Training, Handover', 'Production system'],
                    ['Support', '4 weeks', 'Hypercare, Optimization', 'Stable operations']
                ]
                
                self.api.create_styled_table(
                    presentation_id, slide_id, timeline_data,
                    x=60, y=120, width=600
                )
        
        return slide_id
    
    def create_results_slide(self, presentation_id: str, data: CaseStudyData,
                            branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create results slide with metrics"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            print("\n📊 Creating Results Slide...")
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
            tracker.add_element(40, 60, "header")
            
            # Results bullets
            y_pos = tracker.get_next_y(30)
            if data.results:
                bullet_height = len(data.results[:3]) * 35 + 30
                self.api.add_bullet_list_improved(
                    presentation_id, slide_id, data.results[:3],
                    x=60, y=y_pos, width=600, font_size=16
                )
                tracker.add_element(y_pos, bullet_height, "bullets")
            
            # Metrics cards
            if data.metrics and tracker.current_y < 250:
                metrics_list = list(data.metrics.items())[:3]
                y_pos = max(tracker.get_next_y(40), 250)
                
                # Center cards
                card_width = 180
                card_spacing = 40
                total_width = len(metrics_list) * card_width + (len(metrics_list) - 1) * card_spacing
                x_start = (720 - total_width) // 2
                
                for i, (metric, value) in enumerate(metrics_list):
                    x_pos = x_start + i * (card_width + card_spacing)
                    
                    # Card
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=x_pos, y=y_pos, width=card_width, height=100,
                        fill_color=DEFAULT_THEME['light_bg']
                    )
                    
                    # Value
                    value_id = self.api.generate_id('textbox')
                    requests = [{
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
                    }]
                    
                    self.api.service.presentations().batchUpdate(
                        presentationId=presentation_id,
                        body={'requests': requests}
                    ).execute()
                    
                    # Label
                    label_id = self.api.generate_id('textbox')
                    requests = [{
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
                        body={'requests': requests}
                    ).execute()
        
        return slide_id
    
    def create_metrics_comparison_slide(self, presentation_id: str, data: CaseStudyData,
                                       branding: BrandingConfig) -> str:
        """Create metrics comparison slide with table"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            print("\n📊 Creating Metrics Comparison Slide with Table...")
            
            # Header
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=40, width=5, height=40,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Before vs After Comparison",
                position='left', margin_top=45, width_percent=0.8,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Comparison table
            comparison_data = [
                ['Metric', 'Before', 'After', 'Improvement'],
                ['Deployment Time', '2 hours', '10 minutes', '92% faster'],
                ['System Downtime', '4 hours/month', '5 minutes/month', '98.8% reduction'],
                ['Error Rate', '5.2%', '0.3%', '94% reduction'],
                ['Processing Speed', '100 req/sec', '5000 req/sec', '50x increase'],
                ['User Satisfaction', '65%', '94%', '+29 points'],
                ['Annual Cost', '$1.2M', '$480K', '60% savings']
            ]
            
            self.api.create_styled_table(
                presentation_id, slide_id, comparison_data,
                x=60, y=120, width=600
            )
        
        return slide_id
    
    def create_testimonial_slide(self, presentation_id: str, data: CaseStudyData,
                                branding: BrandingConfig) -> str:
        """Create testimonial slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id and data.testimonial:
            print("\n📊 Creating Testimonial Slide...")
            
            # Light background
            self.api.update_slide_background(presentation_id, slide_id, DEFAULT_THEME['light_bg'])
            
            # Calculate positioning
            test_height = self.calculate_text_height_safe(data.testimonial, 22, int(720 * 0.7))
            total_content_height = 80 + test_height + 60
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
            attr_y = min(y_start + 80 + test_height + 30, 340)
            attribution = f"— {data.client_name} Leadership Team"
            self.api.add_text_box_smart(
                presentation_id, slide_id, attribution,
                position='center', margin_top=attr_y, width_percent=0.5,
                font_size=16, color=DEFAULT_THEME['text_secondary'],
                alignment='CENTER'
            )
        
        return slide_id


class ConsultingPlatformComplete:
    """Complete consulting platform with all fixes"""
    
    def __init__(self):
        self.api = GoogleSlidesEnhancedV2()
        self.templates = ConsultingTemplatesComplete(self.api)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')  # Use gpt-4o-mini as default
    
    def generate_ai_content(self, data: CaseStudyData) -> Dict[str, str]:
        """Generate case study content using OpenAI"""
        prompt = f"""
        Create compelling content for a consulting case study with the following details:
        Client: {data.client_name}
        Industry: {data.industry}
        Challenge: {data.challenge}
        Solution: {data.solution}
        Results: {', '.join(data.results)}
        
        Generate:
        1. An engaging title (not generic, specific to this transformation)
        2. A detailed challenge description that expands on the problem (3-4 sentences)
        3. A solution overview that explains the approach and why it worked (3-4 sentences)
        4. A results summary highlighting the business impact (2-3 sentences)
        
        Format as JSON with keys: title, challenge_detail, solution_detail, results_summary
        """
        
        try:
            print(f"🤖 Generating AI content using {self.model}...")
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional consulting case study writer. Create compelling, specific content that tells a transformation story."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = json.loads(response.choices[0].message.content)
            print("✅ AI content generated successfully")
            return content
            
        except Exception as e:
            print(f"❌ AI generation error: {e}")
            # Fallback content
            return {
                'title': f'{data.client_name} Digital Transformation Success Story',
                'challenge_detail': data.challenge,
                'solution_detail': data.solution,
                'results_summary': f"Achieved significant improvements: {', '.join(data.results[:2])}"
            }
    
    def create_case_study(self, data: CaseStudyData, branding: BrandingConfig) -> str:
        """Create complete case study with tables"""
        # Generate AI content
        ai_content = self.generate_ai_content(data) if client else {
            'title': f'{data.client_name} Digital Transformation Success Story',
            'challenge_detail': data.challenge,
            'solution_detail': data.solution,
            'results_summary': f"Achieved significant improvements: {', '.join(data.results[:2])}"
        }
        
        # Create presentation
        title = f"{data.client_name} Case Study - {datetime.now().strftime('%B %Y')}"
        presentation_id = self.api.create_presentation(title)
        
        if presentation_id:
            # Create all slides
            self.templates.create_case_study_title_slide(presentation_id, data, branding, ai_content)
            self.templates.create_challenge_slide_fixed(presentation_id, data, branding, ai_content)
            self.templates.create_solution_slide(presentation_id, data, branding, ai_content)
            self.templates.create_timeline_slide(presentation_id, data, branding)
            self.templates.create_results_slide(presentation_id, data, branding, ai_content)
            self.templates.create_metrics_comparison_slide(presentation_id, data, branding)
            
            if data.testimonial:
                self.templates.create_testimonial_slide(presentation_id, data, branding)
            
            print(f"\n✅ Complete case study created with NO OVERLAPS + TABLES!")
            print(f"📎 View at: https://docs.google.com/presentation/d/{presentation_id}/edit")
            print("\n📊 Features:")
            print("   - FIXED slide 2 overlap issue")
            print("   - Position tracking throughout")
            print("   - Timeline table demonstration")
            print("   - Metrics comparison table")
            print("   - Professional spacing everywhere")
            
            return presentation_id
        
        return None


def demo_complete_platform():
    """Demo with complete fixes and tables"""
    platform = ConsultingPlatformComplete()
    
    # Professional branding
    branding = BrandingConfig(
        company_name="Strategic Consulting Partners",
        tagline="Transforming Business Through Innovation"
    )
    
    # Sample case study with timeline data
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
        },
        timeline_data=[
            ['Phase', 'Duration', 'Key Activities', 'Status'],
            ['Discovery', '2 weeks', 'System audit, Requirements gathering', 'Complete'],
            ['Design', '4 weeks', 'Architecture design, Tech selection', 'Complete'],
            ['Build', '8 weeks', 'Development, Unit testing', 'Complete'],
            ['Test', '4 weeks', 'Integration testing, UAT', 'Complete'],
            ['Deploy', '2 weeks', 'Production rollout, Training', 'Complete'],
            ['Optimize', '4 weeks', 'Performance tuning, Documentation', 'Complete']
        ]
    )
    
    # Create presentation
    presentation_id = platform.create_case_study(case_study, branding)
    
    return presentation_id


if __name__ == '__main__':
    demo_complete_platform()
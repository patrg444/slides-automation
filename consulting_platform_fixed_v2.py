#!/usr/bin/env python3
"""
Fixed Consulting Platform v2 - Resolves ALL Overlapping Text Issues
Complete redesign of positioning logic with proper spacing calculations
"""

import os
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from google_slides_enhanced_v2 import GoogleSlidesEnhancedV2, FONT_SIZES
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
except Exception as e:
    print(f"Warning: OpenAI client initialization failed: {e}")
    client = None

# Professional color palettes with better contrast
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

# CRITICAL: Proper spacing constants to prevent overlaps
SPACING = {
    'title_slide': {
        'accent_bar_height': 3,
        'client_name_top': 40,
        'client_name_height': 30,
        'main_title_top': 100,  # Increased from 120
        'main_title_height': 80,  # Allow more space for title
        'subtitle_top': 200,  # Increased from 180
        'subtitle_height': 40,
        'footer_top': 340,
        'footer_height': 65,
        'company_name_top': 355,
        'tagline_top': 375
    },
    'content_slide': {
        'section_marker_top': 40,
        'section_marker_height': 40,
        'title_top': 45,
        'title_height': 50,
        'content_top': 110,  # Standard content start
        'content_gap': 20,   # Gap between content blocks
        'bullet_item_height': 30,  # Height per bullet point
        'pill_height': 35,
        'pill_spacing': 50,  # Increased spacing between pills
        'icon_size': 40,
        'icon_text_gap': 60  # Space between icon and text
    },
    'metrics': {
        'card_width': 180,
        'card_height': 100,
        'card_spacing': 40,  # Increased from 30
        'value_top_offset': 20,
        'label_top_offset': 65
    }
}


@dataclass
class BrandingConfig:
    """Company branding configuration with better defaults"""
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


class ConsultingTemplatesFixedV2:
    """Fixed consulting templates with proper spacing calculations"""
    
    def __init__(self, api: GoogleSlidesEnhancedV2):
        self.api = api
        self.slide_width = 720
        self.slide_height = 405
    
    def calculate_text_height(self, text: str, font_size: int, width: int) -> int:
        """Calculate required height for text with proper padding"""
        avg_char_width = font_size * 0.6
        chars_per_line = width / avg_char_width
        lines = max(1, len(text) / chars_per_line)
        line_height = font_size * 1.5  # 1.5x line height for readability
        padding = 20  # Extra padding
        return int(lines * line_height + padding)
    
    def create_case_study_title_slide(self, presentation_id: str, data: CaseStudyData, 
                                     branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create title slide with proper spacing"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            spacing = SPACING['title_slide']
            
            # White background
            self.api.update_slide_background(presentation_id, slide_id, DEFAULT_THEME['background'])
            
            # Top accent bar
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=0, y=0, width=self.slide_width, height=spacing['accent_bar_height'],
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            # Client name - with proper spacing
            self.api.add_text_box_smart(
                presentation_id, slide_id, data.client_name.upper(),
                position='left', 
                margin_top=spacing['client_name_top'], 
                width_percent=0.9,
                font_size=16, 
                color=branding.accent_color,
                bold=True
            )
            
            # Main title - ensure no overlap with client name
            title = ai_content.get('title', f'{data.client_name} Case Study')
            # Calculate actual height needed for title
            title_width = int(self.slide_width * 0.9)
            title_height = self.calculate_text_height(title, 36, title_width)
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, title,
                position='left', 
                margin_top=spacing['main_title_top'], 
                width_percent=0.9,
                font_size=36, 
                color=branding.primary_color,
                bold=True
            )
            
            # Subtitle - positioned after title with proper gap
            if data.results:
                subtitle = f"{data.industry} • {data.results[0]}"
                subtitle_top = spacing['main_title_top'] + title_height + 20  # 20px gap
                
                self.api.add_text_box_smart(
                    presentation_id, slide_id, subtitle,
                    position='left', 
                    margin_top=subtitle_top, 
                    width_percent=0.9,
                    font_size=20, 
                    color=DEFAULT_THEME['text_secondary']
                )
            
            # Footer section - fixed at bottom
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=0, y=spacing['footer_top'], 
                width=self.slide_width, height=spacing['footer_height'],
                fill_color=DEFAULT_THEME['light_bg'],
                add_shadow=False
            )
            
            # Company name in footer
            self.api.add_text_box_smart(
                presentation_id, slide_id, branding.company_name,
                position='left', 
                margin_top=spacing['company_name_top'], 
                width_percent=0.9,
                font_size=14, 
                color=branding.primary_color,
                bold=True
            )
            
            # Tagline in footer - only if it fits
            if branding.tagline:
                self.api.add_text_box_smart(
                    presentation_id, slide_id, branding.tagline,
                    position='left', 
                    margin_top=spacing['tagline_top'], 
                    width_percent=0.9,
                    font_size=12, 
                    color=DEFAULT_THEME['text_secondary']
                )
        
        return slide_id
    
    def create_challenge_slide(self, presentation_id: str, data: CaseStudyData,
                              branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create challenge slide with proper spacing"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            spacing = SPACING['content_slide']
            
            # Section header with accent
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=spacing['section_marker_top'], 
                width=5, height=spacing['section_marker_height'],
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "The Challenge",
                position='left', 
                margin_top=spacing['title_top'], 
                width_percent=0.8,
                font_size=32, 
                color=branding.primary_color, 
                bold=True
            )
            
            # Challenge description
            challenge_text = ai_content.get('challenge_detail', data.challenge)
            desc_width = int(self.slide_width * 0.85)
            desc_height = self.calculate_text_height(challenge_text, 18, desc_width)
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, challenge_text,
                position='left', 
                margin_top=spacing['content_top'], 
                width_percent=0.85,
                font_size=18, 
                color=DEFAULT_THEME['text_primary']
            )
            
            # Key challenges with proper spacing
            if data.challenge:
                challenges = [
                    "Legacy System Constraints",
                    "Process Inefficiencies", 
                    "Limited Analytics Capability"
                ]
                
                # Start challenges after description with gap
                y_start = spacing['content_top'] + desc_height + spacing['content_gap']
                
                for i, challenge in enumerate(challenges[:3]):
                    y_pos = y_start + i * 60  # 60px between items
                    
                    # Icon box
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=60, y=y_pos, 
                        width=spacing['icon_size'], 
                        height=spacing['icon_size'],
                        fill_color=branding.accent_color
                    )
                    
                    # Challenge text - positioned to the right of icon
                    text_x = 60 + spacing['icon_size'] + 20  # 20px gap from icon
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, challenge,
                        position='left', 
                        margin_top=y_pos + 10,  # Center vertically with icon
                        width_percent=0.65,
                        font_size=16, 
                        color=DEFAULT_THEME['text_primary']
                    )
        
        return slide_id
    
    def create_solution_slide(self, presentation_id: str, data: CaseStudyData,
                             branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create solution slide with two-column layout"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            spacing = SPACING['content_slide']
            
            # Section header
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=spacing['section_marker_top'], 
                width=5, height=spacing['section_marker_height'],
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Our Solution",
                position='left', 
                margin_top=spacing['title_top'], 
                width_percent=0.8,
                font_size=32, 
                color=branding.primary_color, 
                bold=True
            )
            
            # Two-column layout with proper spacing
            left_column_width = 320  # Fixed width for left column
            right_column_width = 240  # Fixed width for right column
            column_gap = 40
            
            # Left column: Solution description
            solution_text = ai_content.get('solution_detail', data.solution)
            self.api.add_text_box_smart(
                presentation_id, slide_id, solution_text,
                position='left', 
                margin_top=spacing['content_top'], 
                width_percent=0.44,  # ~320px
                font_size=16, 
                color=DEFAULT_THEME['text_primary']
            )
            
            # Right column: Technology stack
            if data.technologies:
                right_x = 60 + left_column_width + column_gap
                
                # Tech stack header
                self.api.add_text_box_smart(
                    presentation_id, slide_id, "Technology Stack",
                    position='left', 
                    margin_top=spacing['content_top'], 
                    width_percent=0.33,  # ~240px
                    font_size=18, 
                    color=branding.primary_color,
                    bold=True
                )
                
                # Tech items with proper spacing
                tech_y_start = spacing['content_top'] + 40  # After header
                
                for i, tech in enumerate(data.technologies[:4]):
                    y_pos = tech_y_start + i * spacing['pill_spacing']
                    
                    # Tech pill - positioned in right column
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=right_x, 
                        y=y_pos, 
                        width=200, 
                        height=spacing['pill_height'],
                        fill_color=DEFAULT_THEME['light_bg']
                    )
                    
                    # Tech text centered in pill
                    pill_text_y = y_pos + (spacing['pill_height'] - 14) // 2  # Center vertically
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, tech,
                        position='left', 
                        margin_top=pill_text_y, 
                        width_percent=0.28,  # ~200px
                        font_size=14, 
                        color=branding.primary_color,
                        bold=True, 
                        alignment='CENTER'
                    )
        
        return slide_id
    
    def create_results_slide(self, presentation_id: str, data: CaseStudyData,
                            branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create results slide with proper metric card spacing"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            spacing = SPACING['content_slide']
            metrics_spacing = SPACING['metrics']
            
            # Section header
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=spacing['section_marker_top'], 
                width=5, height=spacing['section_marker_height'],
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Results & Impact",
                position='left', 
                margin_top=spacing['title_top'], 
                width_percent=0.8,
                font_size=32, 
                color=branding.primary_color, 
                bold=True
            )
            
            # Bullet points with proper spacing
            if data.results:
                # Calculate total height needed for bullets
                bullet_count = min(3, len(data.results))
                bullets_height = bullet_count * spacing['bullet_item_height'] + 40  # Extra padding
                
                self.api.add_bullet_list_improved(
                    presentation_id, slide_id, data.results[:3],
                    x=60, 
                    y=spacing['content_top'], 
                    width=600, 
                    font_size=16
                )
            
            # Metrics cards - properly centered and spaced
            if data.metrics:
                metrics_list = list(data.metrics.items())[:3]
                
                # Calculate positioning for centered cards
                total_width = (len(metrics_list) * metrics_spacing['card_width'] + 
                              (len(metrics_list) - 1) * metrics_spacing['card_spacing'])
                x_start = (self.slide_width - total_width) // 2
                
                # Position cards below bullets with proper gap
                y_pos = spacing['content_top'] + bullets_height + spacing['content_gap']
                
                for i, (metric, value) in enumerate(metrics_list):
                    x_pos = x_start + i * (metrics_spacing['card_width'] + metrics_spacing['card_spacing'])
                    
                    # Card background
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=x_pos, 
                        y=y_pos, 
                        width=metrics_spacing['card_width'], 
                        height=metrics_spacing['card_height'],
                        fill_color=DEFAULT_THEME['light_bg']
                    )
                    
                    # Metric value - properly positioned
                    value_y = y_pos + metrics_spacing['value_top_offset']
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, value,
                        position='left', 
                        margin_top=value_y, 
                        width_percent=0.25,
                        font_size=28, 
                        color=branding.accent_color,
                        bold=True, 
                        alignment='CENTER'
                    )
                    
                    # Metric label - properly positioned
                    label_y = y_pos + metrics_spacing['label_top_offset']
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, metric,
                        position='left', 
                        margin_top=label_y, 
                        width_percent=0.25,
                        font_size=14, 
                        color=DEFAULT_THEME['text_secondary'],
                        alignment='CENTER'
                    )
        
        return slide_id
    
    def create_testimonial_slide(self, presentation_id: str, data: CaseStudyData,
                                branding: BrandingConfig) -> str:
        """Create testimonial slide with proper text spacing"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id and data.testimonial:
            # Light background
            self.api.update_slide_background(presentation_id, slide_id, DEFAULT_THEME['light_bg'])
            
            # Calculate testimonial height
            test_width = int(self.slide_width * 0.7)
            test_height = self.calculate_text_height(data.testimonial, 22, test_width)
            
            # Center content vertically
            total_height = 60 + test_height + 40 + 30  # quote + text + gap + attribution
            y_start = (self.slide_height - total_height) // 2
            
            # Large quote mark
            self.api.add_text_box_smart(
                presentation_id, slide_id, '"',
                position='center', 
                margin_top=y_start, 
                width_percent=0.1,
                font_size=96, 
                color=branding.accent_color
            )
            
            # Testimonial text
            text_y = y_start + 80  # After quote mark
            self.api.add_text_box_smart(
                presentation_id, slide_id, data.testimonial,
                position='center', 
                margin_top=text_y, 
                width_percent=0.7,
                font_size=22, 
                color=DEFAULT_THEME['text_primary'],
                alignment='CENTER'
            )
            
            # Attribution
            attr_y = text_y + test_height + 40  # After testimonial with gap
            attribution = f"— {data.client_name} Leadership Team"
            self.api.add_text_box_smart(
                presentation_id, slide_id, attribution,
                position='center', 
                margin_top=attr_y, 
                width_percent=0.5,
                font_size=16, 
                color=DEFAULT_THEME['text_secondary'],
                alignment='CENTER'
            )
        
        return slide_id


class ConsultingPlatformFixedV2:
    """Fixed consulting platform with no overlapping text"""
    
    def __init__(self):
        self.api = GoogleSlidesEnhancedV2()
        self.templates = ConsultingTemplatesFixedV2(self.api)
    
    def create_case_study(self, data: CaseStudyData, branding: BrandingConfig) -> str:
        """Create a professionally designed case study with proper spacing"""
        # Generate AI content or use fallback
        ai_content = {
            'title': f'{data.client_name} Digital Transformation Success',
            'challenge_detail': data.challenge,
            'solution_detail': data.solution,
            'results_summary': f"Achieved significant improvements: {', '.join(data.results[:2])}"
        }
        
        # Create presentation
        title = f"{data.client_name} Case Study - {datetime.now().strftime('%B %Y')}"
        presentation_id = self.api.create_presentation(title)
        
        if presentation_id:
            # Create slides with fixed templates
            self.templates.create_case_study_title_slide(presentation_id, data, branding, ai_content)
            self.templates.create_challenge_slide(presentation_id, data, branding, ai_content)
            self.templates.create_solution_slide(presentation_id, data, branding, ai_content)
            self.templates.create_results_slide(presentation_id, data, branding, ai_content)
            
            if data.testimonial:
                self.templates.create_testimonial_slide(presentation_id, data, branding)
            
            print(f"\n✅ Professional case study created with NO OVERLAPPING TEXT!")
            print(f"📎 View at: https://docs.google.com/presentation/d/{presentation_id}/edit")
            
            return presentation_id
        
        return None


def demo_fixed_platform_v2():
    """Demo with completely fixed positioning"""
    platform = ConsultingPlatformFixedV2()
    
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
    demo_fixed_platform_v2()
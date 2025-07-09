#!/usr/bin/env python3
"""
Fixed Consulting Platform with Better Visual Design
Addresses overlapping text, color scheme, and layout issues
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
    },
    'modern_tech': {
        'primary': {'red': 0.071, 'green': 0.071, 'blue': 0.071},       # Almost black
        'secondary': {'red': 0.267, 'green': 0.267, 'blue': 0.267},     # Dark gray
        'accent': {'red': 0.000, 'green': 0.588, 'blue': 0.533},        # Teal
        'background': {'red': 1.000, 'green': 1.000, 'blue': 1.000},    # White
        'light_bg': {'red': 0.980, 'green': 0.980, 'blue': 0.980},      # Light gray
        'text_primary': {'red': 0.071, 'green': 0.071, 'blue': 0.071},  # Almost black
        'text_secondary': {'red': 0.400, 'green': 0.400, 'blue': 0.400}, # Gray
        'success': {'red': 0.133, 'green': 0.545, 'blue': 0.133}        # Green
    }
}

# Use corporate blue as default
DEFAULT_THEME = PROFESSIONAL_THEMES['corporate_blue']


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
        # Use professional theme colors if not specified
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


class ConsultingTemplatesFixed:
    """Fixed consulting templates with better layout"""
    
    def __init__(self, api: GoogleSlidesEnhancedV2):
        self.api = api
    
    def create_case_study_title_slide(self, presentation_id: str, data: CaseStudyData, 
                                     branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create professionally designed title slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # White background for clean look
            self.api.update_slide_background(presentation_id, slide_id, DEFAULT_THEME['background'])
            
            # Top accent bar
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=0, y=0, width=720, height=3,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            # Client name in smaller text at top
            self.api.add_text_box_smart(
                presentation_id, slide_id, data.client_name.upper(),
                position='left', margin_top=30, width_percent=0.9,
                font_size=16, color=branding.accent_color,
                bold=True
            )
            
            # Main title - properly sized and positioned
            title = ai_content.get('title', f'{data.client_name} Case Study')
            self.api.add_text_box_smart(
                presentation_id, slide_id, title,
                position='left', margin_top=120, width_percent=0.9,
                font_size=36, color=branding.primary_color,
                bold=True
            )
            
            # Subtitle with key metric
            if data.results:
                subtitle = f"{data.industry} • {data.results[0]}"
                self.api.add_text_box_smart(
                    presentation_id, slide_id, subtitle,
                    position='left', margin_top=180, width_percent=0.9,
                    font_size=20, color=DEFAULT_THEME['text_secondary']
                )
            
            # Bottom section with company branding
            # Subtle background for footer
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=0, y=340, width=720, height=65,
                fill_color=DEFAULT_THEME['light_bg'],
                add_shadow=False
            )
            
            # Company name and tagline
            self.api.add_text_box_smart(
                presentation_id, slide_id, branding.company_name,
                position='left', margin_top=355, width_percent=0.9,
                font_size=14, color=branding.primary_color,
                bold=True
            )
            
            if branding.tagline:
                self.api.add_text_box_smart(
                    presentation_id, slide_id, branding.tagline,
                    position='left', margin_top=375, width_percent=0.9,
                    font_size=12, color=DEFAULT_THEME['text_secondary']
                )
        
        return slide_id
    
    def create_challenge_slide(self, presentation_id: str, data: CaseStudyData,
                              branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create challenge slide with better spacing"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Section header with accent
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=40, width=5, height=40,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "The Challenge",
                position='left', margin_top=45, width_percent=0.8,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Challenge description - with proper spacing
            challenge_text = ai_content.get('challenge_detail', data.challenge)
            self.api.add_text_box_smart(
                presentation_id, slide_id, challenge_text,
                position='left', margin_top=110, width_percent=0.85,
                font_size=18, color=DEFAULT_THEME['text_primary']
            )
            
            # Key challenges with icon boxes
            if data.challenge:
                challenges = [
                    "Legacy System Constraints",
                    "Process Inefficiencies", 
                    "Limited Analytics Capability"
                ]
                
                y_pos = 220
                for i, challenge in enumerate(challenges[:3]):
                    # Icon box
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=60, y=y_pos + i*50, width=40, height=40,
                        fill_color=branding.accent_color
                    )
                    
                    # Challenge text
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, challenge,
                        position='left', margin_top=y_pos + i*50 + 10, width_percent=0.7,
                        font_size=16, color=DEFAULT_THEME['text_primary']
                    )
        
        return slide_id
    
    def create_solution_slide(self, presentation_id: str, data: CaseStudyData,
                             branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create solution slide with proper layout"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Section header
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=40, width=5, height=40,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Our Solution",
                position='left', margin_top=45, width_percent=0.8,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Two-column layout
            # Left: Solution description
            solution_text = ai_content.get('solution_detail', data.solution)
            self.api.add_text_box_smart(
                presentation_id, slide_id, solution_text,
                position='left', margin_top=110, width_percent=0.45,
                font_size=16, color=DEFAULT_THEME['text_primary']
            )
            
            # Right: Technology stack
            if data.technologies:
                # Tech stack header
                self.api.add_text_box_smart(
                    presentation_id, slide_id, "Technology Stack",
                    position='left', margin_top=110, width_percent=0.35,
                    font_size=18, color=branding.primary_color,
                    bold=True
                )
                
                # Tech items with better spacing
                x_pos = 420
                y_pos = 150
                for i, tech in enumerate(data.technologies[:4]):
                    # Tech pill
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=x_pos, y=y_pos + i*45, width=180, height=35,
                        fill_color=DEFAULT_THEME['light_bg']
                    )
                    
                    # Tech text centered in pill
                    tech_x = x_pos + 90  # Center of pill
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, tech,
                        position='left', margin_top=y_pos + i*45 + 8, width_percent=0.25,
                        font_size=14, color=branding.primary_color,
                        bold=True, alignment='CENTER'
                    )
        
        return slide_id
    
    def create_results_slide(self, presentation_id: str, data: CaseStudyData,
                            branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create results slide with visual metrics"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Section header
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=60, y=40, width=5, height=40,
                fill_color=branding.accent_color,
                add_shadow=False
            )
            
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Results & Impact",
                position='left', margin_top=45, width_percent=0.8,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Key achievements as bullet points
            if data.results:
                self.api.add_bullet_list_improved(
                    presentation_id, slide_id, data.results[:3],
                    x=60, y=110, width=600, font_size=16
                )
            
            # Metrics cards with better design
            if data.metrics:
                metrics_list = list(data.metrics.items())[:3]
                card_width = 180
                card_height = 90
                spacing = 30
                total_width = len(metrics_list) * card_width + (len(metrics_list) - 1) * spacing
                x_start = (720 - total_width) // 2  # Center the cards
                y_pos = 250
                
                for i, (metric, value) in enumerate(metrics_list):
                    x_pos = x_start + i * (card_width + spacing)
                    
                    # Card background
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=x_pos, y=y_pos, width=card_width, height=card_height,
                        fill_color=DEFAULT_THEME['light_bg']
                    )
                    
                    # Metric value (large)
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, value,
                        position='left', margin_top=y_pos + 15, width_percent=0.25,
                        font_size=28, color=branding.accent_color,
                        bold=True, alignment='CENTER'
                    )
                    
                    # Metric label
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, metric,
                        position='left', margin_top=y_pos + 55, width_percent=0.25,
                        font_size=14, color=DEFAULT_THEME['text_secondary'],
                        alignment='CENTER'
                    )
        
        return slide_id
    
    def create_testimonial_slide(self, presentation_id: str, data: CaseStudyData,
                                branding: BrandingConfig) -> str:
        """Create testimonial slide with better design"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id and data.testimonial:
            # Light background
            self.api.update_slide_background(presentation_id, slide_id, DEFAULT_THEME['light_bg'])
            
            # Large quote mark
            self.api.add_text_box_smart(
                presentation_id, slide_id, '"',
                position='center', margin_top=60, width_percent=0.1,
                font_size=96, color=branding.accent_color
            )
            
            # Testimonial text - centered and properly sized
            self.api.add_text_box_smart(
                presentation_id, slide_id, data.testimonial,
                position='center', margin_top=140, width_percent=0.7,
                font_size=22, color=DEFAULT_THEME['text_primary'],
                alignment='CENTER'
            )
            
            # Attribution
            attribution = f"— {data.client_name} Leadership Team"
            self.api.add_text_box_smart(
                presentation_id, slide_id, attribution,
                position='center', margin_top=280, width_percent=0.5,
                font_size=16, color=DEFAULT_THEME['text_secondary'],
                alignment='CENTER'
            )
        
        return slide_id


class ConsultingPlatformFixed:
    """Fixed consulting platform with better visual design"""
    
    def __init__(self):
        self.api = GoogleSlidesEnhancedV2()
        self.templates = ConsultingTemplatesFixed(self.api)
    
    def create_case_study(self, data: CaseStudyData, branding: BrandingConfig) -> str:
        """Create a professionally designed case study"""
        # Generate AI content or use fallback
        ai_content = {
            'title': f'{data.client_name} Digital Transformation Success',
            'challenge_detail': data.challenge,
            'solution_detail': data.solution,
            'results_summary': f"Achieved significant improvements: {', '.join(data.results[:2])}"
        }
        
        # Create presentation with better naming
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
            
            print(f"\n✅ Professional case study created!")
            print(f"📎 View at: https://docs.google.com/presentation/d/{presentation_id}/edit")
            
            return presentation_id
        
        return None


def demo_fixed_platform():
    """Demo with fixed visual design"""
    platform = ConsultingPlatformFixed()
    
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
    demo_fixed_platform()
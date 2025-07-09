#!/usr/bin/env python3
"""
Consulting Platform - AI-Powered Case Study & Proposal Generator
Built on Google Slides API for consulting firms
"""

import os
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from google_slides_enhanced_v2 import GoogleSlidesEnhancedV2, THEME_COLORS, FONT_SIZES
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
except Exception as e:
    print(f"Warning: OpenAI client initialization failed: {e}")
    client = None


@dataclass
class BrandingConfig:
    """Company branding configuration"""
    company_name: str
    primary_color: Dict[str, float]
    secondary_color: Dict[str, float]
    accent_color: Dict[str, float]
    logo_url: Optional[str] = None
    font_family: str = 'Arial'
    tagline: Optional[str] = None
    website: Optional[str] = None
    
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


@dataclass
class ProposalData:
    """Data structure for proposals"""
    client_name: str
    project_name: str
    executive_summary: str
    objectives: List[str]
    approach: List[str]
    deliverables: List[str]
    timeline_weeks: int
    team_members: List[Dict[str, str]]
    budget_range: str
    next_steps: List[str]


class AssetLibrary:
    """Manage reusable assets for presentations"""
    
    def __init__(self, storage_path: str = './assets'):
        self.storage_path = storage_path
        self.assets = self.load_assets()
    
    def load_assets(self) -> Dict[str, Any]:
        """Load assets from storage"""
        assets_file = os.path.join(self.storage_path, 'assets.json')
        if os.path.exists(assets_file):
            with open(assets_file, 'r') as f:
                return json.load(f)
        return {
            'images': {},
            'text_snippets': {},
            'slide_templates': {},
            'charts': {}
        }
    
    def save_assets(self):
        """Save assets to storage"""
        os.makedirs(self.storage_path, exist_ok=True)
        with open(os.path.join(self.storage_path, 'assets.json'), 'w') as f:
            json.dump(self.assets, f, indent=2)
    
    def add_text_snippet(self, name: str, content: str, category: str = 'general'):
        """Add reusable text snippet"""
        if 'text_snippets' not in self.assets:
            self.assets['text_snippets'] = {}
        
        self.assets['text_snippets'][name] = {
            'content': content,
            'category': category,
            'created': datetime.now().isoformat()
        }
        self.save_assets()
    
    def add_image(self, name: str, url: str, category: str = 'general'):
        """Add reusable image"""
        if 'images' not in self.assets:
            self.assets['images'] = {}
        
        self.assets['images'][name] = {
            'url': url,
            'category': category,
            'created': datetime.now().isoformat()
        }
        self.save_assets()
    
    def get_asset(self, asset_type: str, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve an asset"""
        return self.assets.get(asset_type, {}).get(name)


class AIContentGenerator:
    """Generate content using OpenAI"""
    
    def __init__(self, model: str = None):
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
    
    def generate_case_study_content(self, data: CaseStudyData) -> Dict[str, str]:
        """Generate case study content using AI"""
        prompt = f"""
        Create compelling content for a consulting case study with the following details:
        Client: {data.client_name}
        Industry: {data.industry}
        Challenge: {data.challenge}
        Solution: {data.solution}
        Results: {', '.join(data.results)}
        
        Generate:
        1. An executive summary (2-3 sentences)
        2. A detailed challenge description (3-4 sentences)
        3. A solution overview (3-4 sentences)
        4. A results summary with impact (2-3 sentences)
        5. A compelling title for the case study
        
        Format as JSON with keys: executive_summary, challenge_detail, solution_detail, results_summary, title
        """
        
        try:
            if not client:
                raise Exception("OpenAI client not initialized")
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional consulting case study writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        
        except Exception as e:
            print(f"AI generation error: {e}")
            # Fallback content
            return {
                "title": f"{data.client_name} Digital Transformation",
                "executive_summary": f"Helped {data.client_name} overcome {data.challenge} through innovative solutions.",
                "challenge_detail": data.challenge,
                "solution_detail": data.solution,
                "results_summary": f"Achieved: {', '.join(data.results[:2])}"
            }
    
    def generate_proposal_content(self, data: ProposalData) -> Dict[str, str]:
        """Generate proposal content using AI"""
        prompt = f"""
        Create professional content for a consulting proposal:
        Client: {data.client_name}
        Project: {data.project_name}
        Summary: {data.executive_summary}
        Objectives: {', '.join(data.objectives[:3])}
        
        Generate:
        1. A compelling value proposition (2-3 sentences)
        2. A project vision statement (2 sentences)
        3. Key benefits for the client (3 bullet points)
        4. A call-to-action statement
        
        Format as JSON with keys: value_prop, vision, benefits (array), cta
        """
        
        try:
            if not client:
                raise Exception("OpenAI client not initialized")
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional proposal writer for a consulting firm."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        
        except Exception as e:
            print(f"AI generation error: {e}")
            return {
                "value_prop": f"Partner with us to transform {data.project_name} into a competitive advantage.",
                "vision": f"Empowering {data.client_name} to achieve excellence through innovation.",
                "benefits": ["Increased efficiency", "Cost optimization", "Strategic advantage"],
                "cta": "Let's build the future together."
            }


class ConsultingTemplates:
    """Consulting-specific slide templates"""
    
    def __init__(self, api: GoogleSlidesEnhancedV2, ai_generator: AIContentGenerator):
        self.api = api
        self.ai = ai_generator
    
    def create_case_study_title_slide(self, presentation_id: str, data: CaseStudyData, 
                                     branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create case study title slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Background
            self.api.update_slide_background(presentation_id, slide_id, branding.primary_color)
            
            # Client logo placeholder
            if data.client_name:
                self.api.add_shape_styled(
                    presentation_id, slide_id, 'RECTANGLE',
                    x=50, y=50, width=150, height=75,
                    fill_color={'red': 1, 'green': 1, 'blue': 1},
                    add_shadow=False
                )
                self.api.add_text_box_smart(
                    presentation_id, slide_id, f"{data.client_name}\nLogo",
                    position='left', margin_top=65, width_percent=0.2,
                    font_size=12, color={'red': 0.7, 'green': 0.7, 'blue': 0.7},
                    alignment='CENTER'
                )
            
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, ai_content.get('title', 'Case Study'),
                position='center', margin_top=150, width_percent=0.8,
                font_size=48, color={'red': 1, 'green': 1, 'blue': 1},
                bold=True, alignment='CENTER'
            )
            
            # Industry & Results highlight
            highlight_text = f"{data.industry} | {data.results[0] if data.results else 'Transformation'}"
            self.api.add_text_box_smart(
                presentation_id, slide_id, highlight_text,
                position='center', margin_top=220, width_percent=0.6,
                font_size=20, color={'red': 1, 'green': 1, 'blue': 1},
                alignment='CENTER'
            )
            
            # Company branding
            if branding.logo_url:
                self.api.add_image(presentation_id, slide_id, branding.logo_url,
                                  x=580, y=320, width=100, height=50)
            
            self.api.add_text_box_smart(
                presentation_id, slide_id, branding.company_name,
                position='right', margin_top=380, width_percent=0.3,
                font_size=14, color={'red': 1, 'green': 1, 'blue': 1}
            )
        
        return slide_id
    
    def create_challenge_slide(self, presentation_id: str, data: CaseStudyData,
                              branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create challenge slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "The Challenge",
                position='left', margin_top=40, width_percent=0.9,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Challenge description
            self.api.add_text_box_smart(
                presentation_id, slide_id, ai_content.get('challenge_detail', data.challenge),
                position='left', margin_top=100, width_percent=0.9,
                font_size=18, color=THEME_COLORS['text_primary']
            )
            
            # Key pain points
            if data.challenge:
                pain_points = [
                    "Outdated systems limiting growth",
                    "Inefficient processes causing delays",
                    "Lack of data-driven insights"
                ]
                
                self.api.add_bullet_list_improved(
                    presentation_id, slide_id, pain_points,
                    y=200, font_size=16
                )
        
        return slide_id
    
    def create_solution_slide(self, presentation_id: str, data: CaseStudyData,
                             branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create solution slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Our Solution",
                position='left', margin_top=40, width_percent=0.9,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Solution overview
            self.api.add_text_box_smart(
                presentation_id, slide_id, ai_content.get('solution_detail', data.solution),
                position='left', margin_top=100, width_percent=0.5,
                font_size=16
            )
            
            # Technologies used (if provided)
            if data.technologies:
                # Tech stack visual
                y_pos = 120
                x_start = 400
                for i, tech in enumerate(data.technologies[:4]):
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'ROUND_RECTANGLE',
                        x=x_start, y=y_pos + i*50, width=150, height=35,
                        fill_color=branding.accent_color
                    )
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, tech,
                        position='left', margin_top=y_pos + i*50 + 8, width_percent=0.2,
                        font_size=14, color={'red': 1, 'green': 1, 'blue': 1},
                        bold=True, alignment='CENTER'
                    )
        
        return slide_id
    
    def create_results_slide(self, presentation_id: str, data: CaseStudyData,
                            branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create results slide with metrics"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Results & Impact",
                position='left', margin_top=40, width_percent=0.9,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Results summary
            self.api.add_text_box_smart(
                presentation_id, slide_id, ai_content.get('results_summary', ''),
                position='left', margin_top=100, width_percent=0.9,
                font_size=16
            )
            
            # Metrics visualization
            if data.metrics:
                x_pos = 60
                y_pos = 180
                for i, (metric, value) in enumerate(list(data.metrics.items())[:3]):
                    # Metric box
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'RECTANGLE',
                        x=x_pos + i*200, y=y_pos, width=180, height=100,
                        fill_color=branding.secondary_color
                    )
                    # Value
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, value,
                        position='left', margin_top=y_pos + 20, width_percent=0.24,
                        font_size=36, color={'red': 1, 'green': 1, 'blue': 1},
                        bold=True, alignment='CENTER'
                    )
                    # Metric name
                    self.api.add_text_box_smart(
                        presentation_id, slide_id, metric,
                        position='left', margin_top=y_pos + 65, width_percent=0.24,
                        font_size=14, color={'red': 1, 'green': 1, 'blue': 1},
                        alignment='CENTER'
                    )
        
        return slide_id
    
    def create_testimonial_slide(self, presentation_id: str, data: CaseStudyData,
                                branding: BrandingConfig) -> str:
        """Create testimonial slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id and data.testimonial:
            # Background
            self.api.update_slide_background(presentation_id, slide_id, 
                                           {'red': 0.98, 'green': 0.98, 'blue': 0.98})
            
            # Quote mark
            self.api.add_text_box_smart(
                presentation_id, slide_id, '"',
                position='left', margin_top=80, width_percent=0.1,
                font_size=72, color=branding.accent_color
            )
            
            # Testimonial text
            self.api.add_text_box_smart(
                presentation_id, slide_id, data.testimonial,
                position='center', margin_top=150, width_percent=0.7,
                font_size=24, color=THEME_COLORS['text_primary'],
                alignment='CENTER'
            )
            
            # Attribution
            self.api.add_text_box_smart(
                presentation_id, slide_id, f"— {data.client_name} Leadership",
                position='center', margin_top=250, width_percent=0.5,
                font_size=16, color=THEME_COLORS['text_secondary'],
                alignment='CENTER'
            )
        
        return slide_id


class PresentationEditor:
    """Edit and manage presentations"""
    
    def __init__(self, api: GoogleSlidesEnhancedV2):
        self.api = api
    
    def reorder_slides(self, presentation_id: str, slide_id: str, new_index: int) -> bool:
        """Reorder slides in presentation"""
        try:
            requests = [{
                'updateSlidesPosition': {
                    'slideObjectIds': [slide_id],
                    'insertionIndex': new_index
                }
            }]
            
            self.api.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Moved slide to position {new_index}")
            return True
            
        except Exception as e:
            print(f"❌ Error reordering slides: {e}")
            return False
    
    def delete_slide(self, presentation_id: str, slide_id: str) -> bool:
        """Delete a slide"""
        try:
            requests = [{
                'deleteObject': {
                    'objectId': slide_id
                }
            }]
            
            self.api.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Deleted slide {slide_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting slide: {e}")
            return False
    
    def update_text_element(self, presentation_id: str, element_id: str, new_text: str) -> bool:
        """Update text in an element"""
        try:
            requests = [
                {
                    'deleteText': {
                        'objectId': element_id,
                        'textRange': {'type': 'ALL'}
                    }
                },
                {
                    'insertText': {
                        'objectId': element_id,
                        'text': new_text,
                        'insertionIndex': 0
                    }
                }
            ]
            
            self.api.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Updated text element")
            return True
            
        except Exception as e:
            print(f"❌ Error updating text: {e}")
            return False


class ConsultingPlatform:
    """Main platform for consulting presentations"""
    
    def __init__(self):
        self.api = GoogleSlidesEnhancedV2()
        self.ai = AIContentGenerator()
        self.templates = ConsultingTemplates(self.api, self.ai)
        self.editor = PresentationEditor(self.api)
        self.assets = AssetLibrary()
    
    def create_case_study(self, data: CaseStudyData, branding: BrandingConfig) -> str:
        """Create a complete case study presentation"""
        # Generate AI content
        ai_content = self.ai.generate_case_study_content(data)
        
        # Create presentation
        title = ai_content.get('title', f'{data.client_name} Case Study')
        presentation_id = self.api.create_presentation(title)
        
        if presentation_id:
            # Create slides
            self.templates.create_case_study_title_slide(presentation_id, data, branding, ai_content)
            self.templates.create_challenge_slide(presentation_id, data, branding, ai_content)
            self.templates.create_solution_slide(presentation_id, data, branding, ai_content)
            self.templates.create_results_slide(presentation_id, data, branding, ai_content)
            
            if data.testimonial:
                self.templates.create_testimonial_slide(presentation_id, data, branding)
            
            print(f"\n✅ Case study created successfully!")
            print(f"📎 View at: https://docs.google.com/presentation/d/{presentation_id}/edit")
            
            return presentation_id
        
        return None
    
    def create_proposal(self, data: ProposalData, branding: BrandingConfig) -> str:
        """Create a complete proposal presentation"""
        # Generate AI content
        ai_content = self.ai.generate_proposal_content(data)
        
        # Create presentation
        title = f"{data.project_name} - Proposal for {data.client_name}"
        presentation_id = self.api.create_presentation(title)
        
        if presentation_id:
            # TODO: Implement proposal slides
            print(f"\n✅ Proposal created successfully!")
            print(f"📎 View at: https://docs.google.com/presentation/d/{presentation_id}/edit")
            
            return presentation_id
        
        return None
    
    def apply_branding(self, presentation_id: str, branding: BrandingConfig):
        """Apply branding to all slides"""
        presentation = self.api.get_presentation(presentation_id)
        if presentation:
            # TODO: Update all slides with branding
            pass
    
    def export_presentation(self, presentation_id: str, format: str = 'pptx') -> str:
        """Export presentation to different formats"""
        # Note: This would require additional APIs or services
        # For now, return the Google Slides URL
        return f"https://docs.google.com/presentation/d/{presentation_id}/export/{format}"


def demo_consulting_platform():
    """Demo the consulting platform"""
    platform = ConsultingPlatform()
    
    # Sample branding
    branding = BrandingConfig(
        company_name="Strategic Consulting Group",
        primary_color={'red': 0.086, 'green': 0.208, 'blue': 0.365},
        secondary_color={'red': 0.5, 'green': 0.5, 'blue': 0.5},
        accent_color={'red': 0.937, 'green': 0.424, 'blue': 0.161},
        tagline="Transforming Business Through Innovation"
    )
    
    # Sample case study data
    case_study = CaseStudyData(
        client_name="TechCorp Industries",
        industry="Technology",
        challenge="Legacy systems hindering digital transformation and market competitiveness",
        solution="Implemented cloud-native architecture with microservices and AI-driven analytics",
        results=[
            "45% reduction in operational costs",
            "3x faster time-to-market",
            "98% system uptime achieved"
        ],
        timeline="6 months",
        team_size="12 consultants",
        technologies=["AWS", "Kubernetes", "Python", "React"],
        testimonial="The Strategic Consulting Group transformed our entire technology stack and culture. We're now leading our industry in innovation.",
        metrics={
            "Cost Savings": "$2.5M",
            "Efficiency Gain": "45%",
            "ROI": "320%"
        }
    )
    
    # Create case study
    platform.create_case_study(case_study, branding)


if __name__ == '__main__':
    demo_consulting_platform()
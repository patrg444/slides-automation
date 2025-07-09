#!/usr/bin/env python3
"""
Extended Consulting Templates - Proposals, Executive Summaries, and More
"""

from consulting_platform import (
    ConsultingTemplates, ProposalData, BrandingConfig,
    GoogleSlidesEnhancedV2, THEME_COLORS, FONT_SIZES
)
from typing import List, Dict, Optional


class ExtendedConsultingTemplates(ConsultingTemplates):
    """Extended templates for various consulting deliverables"""
    
    def create_proposal_title_slide(self, presentation_id: str, data: ProposalData,
                                   branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create proposal title slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Gradient background effect
            self.api.update_slide_background(presentation_id, slide_id, 
                                           {'red': 0.98, 'green': 0.98, 'blue': 0.98})
            
            # Top accent bar
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=0, y=0, width=720, height=60,
                fill_color=branding.primary_color,
                add_shadow=False
            )
            
            # Proposal title
            self.api.add_text_box_smart(
                presentation_id, slide_id, data.project_name,
                position='center', margin_top=120, width_percent=0.8,
                font_size=42, color=branding.primary_color,
                bold=True, alignment='CENTER'
            )
            
            # Client name
            self.api.add_text_box_smart(
                presentation_id, slide_id, f"Prepared for {data.client_name}",
                position='center', margin_top=180, width_percent=0.6,
                font_size=24, color=THEME_COLORS['text_secondary'],
                alignment='CENTER'
            )
            
            # Date
            from datetime import datetime
            self.api.add_text_box_smart(
                presentation_id, slide_id, datetime.now().strftime("%B %Y"),
                position='center', margin_top=240, width_percent=0.4,
                font_size=18, color=THEME_COLORS['text_secondary'],
                alignment='CENTER'
            )
            
            # Company info footer
            self.api.add_text_box_smart(
                presentation_id, slide_id, branding.company_name,
                position='center', margin_top=350, width_percent=0.6,
                font_size=16, color=branding.secondary_color,
                bold=True, alignment='CENTER'
            )
            
            if branding.tagline:
                self.api.add_text_box_smart(
                    presentation_id, slide_id, branding.tagline,
                    position='center', margin_top=375, width_percent=0.6,
                    font_size=12, color=THEME_COLORS['text_secondary'],
                    alignment='CENTER'
                )
        
        return slide_id
    
    def create_executive_summary_slide(self, presentation_id: str, data: ProposalData,
                                      branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create executive summary slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Executive Summary",
                position='left', margin_top=40, width_percent=0.9,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Summary text
            self.api.add_text_box_smart(
                presentation_id, slide_id, data.executive_summary,
                position='left', margin_top=100, width_percent=0.9,
                font_size=16, color=THEME_COLORS['text_primary']
            )
            
            # Key points
            if ai_content.get('benefits'):
                self.api.add_text_box_smart(
                    presentation_id, slide_id, "Key Benefits:",
                    position='left', margin_top=200, width_percent=0.9,
                    font_size=18, color=branding.secondary_color, bold=True
                )
                
                self.api.add_bullet_list_improved(
                    presentation_id, slide_id, ai_content['benefits'],
                    y=240, font_size=16
                )
        
        return slide_id
    
    def create_objectives_slide(self, presentation_id: str, data: ProposalData,
                               branding: BrandingConfig) -> str:
        """Create objectives slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Project Objectives",
                position='left', margin_top=40, width_percent=0.9,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Objectives with icons
            y_pos = 120
            for i, objective in enumerate(data.objectives[:4]):
                # Icon circle
                self.api.add_shape_styled(
                    presentation_id, slide_id, 'ELLIPSE',
                    x=60, y=y_pos + i*60, width=40, height=40,
                    fill_color=branding.accent_color
                )
                
                # Number
                self.api.add_text_box_smart(
                    presentation_id, slide_id, str(i+1),
                    position='left', margin_top=y_pos + i*60 + 10, width_percent=0.055,
                    font_size=20, color={'red': 1, 'green': 1, 'blue': 1},
                    bold=True, alignment='CENTER'
                )
                
                # Objective text
                self.api.add_text_box_smart(
                    presentation_id, slide_id, objective,
                    position='left', margin_top=y_pos + i*60 + 5, width_percent=0.75,
                    font_size=16, color=THEME_COLORS['text_primary']
                )
        
        return slide_id
    
    def create_approach_slide(self, presentation_id: str, data: ProposalData,
                             branding: BrandingConfig) -> str:
        """Create approach/methodology slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Our Approach",
                position='left', margin_top=40, width_percent=0.9,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Approach phases
            phases = data.approach[:4] if len(data.approach) > 4 else data.approach
            x_pos = 60
            y_pos = 120
            box_width = 150
            
            for i, phase in enumerate(phases):
                # Phase box
                self.api.add_shape_styled(
                    presentation_id, slide_id, 'ROUND_RECTANGLE',
                    x=x_pos + i*(box_width + 20), y=y_pos, width=box_width, height=180,
                    fill_color={'red': 0.95, 'green': 0.97, 'blue': 1.0}
                )
                
                # Phase number
                self.api.add_text_box_smart(
                    presentation_id, slide_id, f"Phase {i+1}",
                    position='left', margin_top=y_pos + 20, width_percent=0.2,
                    font_size=18, color=branding.primary_color,
                    bold=True, alignment='CENTER'
                )
                
                # Phase description
                self.api.add_text_box_smart(
                    presentation_id, slide_id, phase,
                    position='left', margin_top=y_pos + 60, width_percent=0.19,
                    font_size=14, color=THEME_COLORS['text_primary'],
                    alignment='CENTER'
                )
                
                # Arrow between phases
                if i < len(phases) - 1:
                    self.api.add_shape_styled(
                        presentation_id, slide_id, 'RIGHT_ARROW',
                        x=x_pos + (i+1)*(box_width + 20) - 20, y=y_pos + 80,
                        width=20, height=20,
                        fill_color=branding.accent_color
                    )
        
        return slide_id
    
    def create_team_slide(self, presentation_id: str, data: ProposalData,
                         branding: BrandingConfig) -> str:
        """Create team slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Project Team",
                position='left', margin_top=40, width_percent=0.9,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Team members grid
            members = data.team_members[:6]  # Max 6 members
            cols = 3
            rows = 2
            x_start = 60
            y_start = 120
            box_width = 200
            box_height = 100
            
            for i, member in enumerate(members):
                row = i // cols
                col = i % cols
                x_pos = x_start + col * (box_width + 20)
                y_pos = y_start + row * (box_height + 20)
                
                # Member box
                self.api.add_shape_styled(
                    presentation_id, slide_id, 'RECTANGLE',
                    x=x_pos, y=y_pos, width=box_width, height=box_height,
                    fill_color={'red': 0.98, 'green': 0.98, 'blue': 0.98}
                )
                
                # Profile circle (placeholder)
                self.api.add_shape_styled(
                    presentation_id, slide_id, 'ELLIPSE',
                    x=x_pos + 10, y=y_pos + 20, width=60, height=60,
                    fill_color=branding.secondary_color
                )
                
                # Name and role
                self.api.add_text_box_smart(
                    presentation_id, slide_id, member.get('name', 'Team Member'),
                    position='left', margin_top=y_pos + 25, width_percent=0.2,
                    font_size=14, color=THEME_COLORS['text_primary'],
                    bold=True
                )
                
                self.api.add_text_box_smart(
                    presentation_id, slide_id, member.get('role', 'Consultant'),
                    position='left', margin_top=y_pos + 45, width_percent=0.2,
                    font_size=12, color=THEME_COLORS['text_secondary']
                )
        
        return slide_id
    
    def create_timeline_slide(self, presentation_id: str, data: ProposalData,
                             branding: BrandingConfig) -> str:
        """Create timeline slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Project Timeline",
                position='left', margin_top=40, width_percent=0.9,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Timeline visualization
            weeks = data.timeline_weeks
            milestones = min(5, weeks // 2)  # Max 5 milestones
            
            # Timeline bar
            bar_width = 600
            bar_x = 60
            bar_y = 180
            
            self.api.add_shape_styled(
                presentation_id, slide_id, 'RECTANGLE',
                x=bar_x, y=bar_y, width=bar_width, height=10,
                fill_color=branding.secondary_color,
                add_shadow=False
            )
            
            # Milestones
            for i in range(milestones):
                x_pos = bar_x + (i * bar_width // (milestones - 1))
                
                # Milestone marker
                self.api.add_shape_styled(
                    presentation_id, slide_id, 'ELLIPSE',
                    x=x_pos - 10, y=bar_y - 5, width=20, height=20,
                    fill_color=branding.accent_color
                )
                
                # Week label
                week_num = (i * weeks) // (milestones - 1)
                self.api.add_text_box_smart(
                    presentation_id, slide_id, f"Week {week_num}",
                    position='left', margin_top=bar_y + 30, width_percent=0.1,
                    font_size=12, color=THEME_COLORS['text_secondary'],
                    alignment='CENTER'
                )
                
                # Milestone name
                milestone_names = ["Kickoff", "Discovery", "Design", "Implementation", "Delivery"]
                self.api.add_text_box_smart(
                    presentation_id, slide_id, milestone_names[i],
                    position='left', margin_top=bar_y - 40, width_percent=0.15,
                    font_size=14, color=THEME_COLORS['text_primary'],
                    bold=True, alignment='CENTER'
                )
        
        return slide_id
    
    def create_investment_slide(self, presentation_id: str, data: ProposalData,
                               branding: BrandingConfig) -> str:
        """Create investment/budget slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Investment",
                position='left', margin_top=40, width_percent=0.9,
                font_size=32, color=branding.primary_color, bold=True
            )
            
            # Budget range box
            self.api.add_shape_styled(
                presentation_id, slide_id, 'ROUND_RECTANGLE',
                x=200, y=120, width=320, height=100,
                fill_color=branding.primary_color
            )
            
            # Budget amount
            self.api.add_text_box_smart(
                presentation_id, slide_id, data.budget_range,
                position='center', margin_top=150, width_percent=0.4,
                font_size=36, color={'red': 1, 'green': 1, 'blue': 1},
                bold=True, alignment='CENTER'
            )
            
            # What's included
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Investment Includes:",
                position='left', margin_top=250, width_percent=0.9,
                font_size=18, color=branding.secondary_color, bold=True
            )
            
            includes = [
                "Full project team and resources",
                "All deliverables and documentation",
                "Post-implementation support",
                "Knowledge transfer and training"
            ]
            
            self.api.add_bullet_list_improved(
                presentation_id, slide_id, includes,
                y=290, font_size=16
            )
        
        return slide_id
    
    def create_next_steps_slide(self, presentation_id: str, data: ProposalData,
                               branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
        """Create next steps/CTA slide"""
        slide_id = self.api.add_slide(presentation_id, 'BLANK')
        
        if slide_id:
            # Background
            self.api.update_slide_background(presentation_id, slide_id, 
                                           branding.primary_color)
            
            # Title
            self.api.add_text_box_smart(
                presentation_id, slide_id, "Next Steps",
                position='center', margin_top=80, width_percent=0.8,
                font_size=42, color={'red': 1, 'green': 1, 'blue': 1},
                bold=True, alignment='CENTER'
            )
            
            # Next steps
            y_pos = 160
            for i, step in enumerate(data.next_steps[:3]):
                # Step number circle
                self.api.add_shape_styled(
                    presentation_id, slide_id, 'ELLIPSE',
                    x=150, y=y_pos + i*50, width=40, height=40,
                    fill_color={'red': 1, 'green': 1, 'blue': 1}
                )
                
                self.api.add_text_box_smart(
                    presentation_id, slide_id, str(i+1),
                    position='left', margin_top=y_pos + i*50 + 10, width_percent=0.055,
                    font_size=20, color=branding.primary_color,
                    bold=True, alignment='CENTER'
                )
                
                # Step text
                self.api.add_text_box_smart(
                    presentation_id, slide_id, step,
                    position='left', margin_top=y_pos + i*50 + 10, width_percent=0.6,
                    font_size=18, color={'red': 1, 'green': 1, 'blue': 1}
                )
            
            # CTA
            self.api.add_text_box_smart(
                presentation_id, slide_id, ai_content.get('cta', "Let's get started!"),
                position='center', margin_top=320, width_percent=0.8,
                font_size=24, color={'red': 1, 'green': 1, 'blue': 1},
                alignment='CENTER'
            )
        
        return slide_id


def create_full_proposal(api: GoogleSlidesEnhancedV2, data: ProposalData, 
                        branding: BrandingConfig, ai_content: Dict[str, str]) -> str:
    """Create a complete proposal presentation"""
    templates = ExtendedConsultingTemplates(api, None)
    
    # Create presentation
    title = f"{data.project_name} - Proposal for {data.client_name}"
    presentation_id = api.create_presentation(title)
    
    if presentation_id:
        # Create all slides
        templates.create_proposal_title_slide(presentation_id, data, branding, ai_content)
        templates.create_executive_summary_slide(presentation_id, data, branding, ai_content)
        templates.create_objectives_slide(presentation_id, data, branding)
        templates.create_approach_slide(presentation_id, data, branding)
        templates.create_team_slide(presentation_id, data, branding)
        templates.create_timeline_slide(presentation_id, data, branding)
        templates.create_investment_slide(presentation_id, data, branding)
        templates.create_next_steps_slide(presentation_id, data, branding, ai_content)
        
        print(f"\n✅ Full proposal created!")
        print(f"📎 View at: https://docs.google.com/presentation/d/{presentation_id}/edit")
        
        return presentation_id
    
    return None
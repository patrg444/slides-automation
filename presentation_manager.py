#!/usr/bin/env python3
"""
Google Slides Presentation Manager
High-level interface for creating complete presentations
"""

from typing import List, Dict, Optional, Any
from google_slides_enhanced import GoogleSlidesEnhanced
from datetime import datetime
import json


class PresentationManager:
    """Manage complete presentations with templates and themes"""
    
    def __init__(self):
        self.api = GoogleSlidesEnhanced()
        self.presentation_id = None
        self.slides = []
        self.theme = self.get_default_theme()
    
    def get_default_theme(self) -> Dict[str, Any]:
        """Get default theme settings"""
        return {
            'primary_color': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
            'secondary_color': {'red': 0.3, 'green': 0.3, 'blue': 0.3},
            'accent_color': {'red': 0.9, 'green': 0.3, 'blue': 0.2},
            'background_color': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
            'title_font_size': 48,
            'heading_font_size': 32,
            'body_font_size': 18,
            'font_family': 'Arial'
        }
    
    def create_presentation(self, title: str, theme: Optional[Dict] = None) -> str:
        """Create a new presentation with optional theme"""
        if theme:
            self.theme = {**self.theme, **theme}
        
        self.presentation_id = self.api.create_presentation(title)
        return self.presentation_id
    
    def add_title_slide(self, title: str, subtitle: str = "", 
                       author: str = "", date: Optional[str] = None) -> str:
        """Add a professional title slide"""
        slide_id = self.api.add_slide(self.presentation_id, 'BLANK')
        
        if slide_id:
            # Background
            self.api.update_slide_properties(
                self.presentation_id, slide_id,
                background_color=self.theme['background_color']
            )
            
            # Title
            self.api.add_formatted_text(
                self.presentation_id, slide_id, title,
                x=50, y=120, width=600, height=100,
                font_size=self.theme['title_font_size'],
                font_family=self.theme['font_family'],
                bold=True, alignment='CENTER',
                color=self.theme['primary_color']
            )
            
            # Subtitle
            if subtitle:
                self.api.add_formatted_text(
                    self.presentation_id, slide_id, subtitle,
                    x=50, y=250, width=600, height=60,
                    font_size=24,
                    font_family=self.theme['font_family'],
                    alignment='CENTER',
                    color=self.theme['secondary_color']
                )
            
            # Author and date
            footer_text = []
            if author:
                footer_text.append(author)
            if date:
                footer_text.append(date)
            elif date is None:
                footer_text.append(datetime.now().strftime("%B %d, %Y"))
            
            if footer_text:
                self.api.add_formatted_text(
                    self.presentation_id, slide_id, ' | '.join(footer_text),
                    x=50, y=450, width=600, height=40,
                    font_size=14,
                    font_family=self.theme['font_family'],
                    alignment='CENTER',
                    color=self.theme['secondary_color']
                )
            
            self.slides.append({'id': slide_id, 'type': 'title', 'title': title})
        
        return slide_id
    
    def add_agenda_slide(self, items: List[str]) -> str:
        """Add an agenda/outline slide"""
        slide_id = self.api.add_slide(self.presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_formatted_text(
                self.presentation_id, slide_id, "Agenda",
                x=50, y=30, width=600, height=60,
                font_size=self.theme['heading_font_size'],
                font_family=self.theme['font_family'],
                bold=True,
                color=self.theme['primary_color']
            )
            
            # Numbered list
            numbered_items = [f"{i+1}. {item}" for i, item in enumerate(items)]
            text = '\n\n'.join(numbered_items)
            
            self.api.add_formatted_text(
                self.presentation_id, slide_id, text,
                x=100, y=120, width=500, height=300,
                font_size=20,
                font_family=self.theme['font_family'],
                color=self.theme['secondary_color']
            )
            
            self.slides.append({'id': slide_id, 'type': 'agenda', 'items': items})
        
        return slide_id
    
    def add_section_divider(self, section_title: str, section_number: Optional[int] = None) -> str:
        """Add a section divider slide"""
        slide_id = self.api.add_slide(self.presentation_id, 'BLANK')
        
        if slide_id:
            # Colored background
            self.api.update_slide_properties(
                self.presentation_id, slide_id,
                background_color=self.theme['primary_color']
            )
            
            # Section number
            if section_number:
                self.api.add_formatted_text(
                    self.presentation_id, slide_id, str(section_number),
                    x=50, y=150, width=100, height=100,
                    font_size=72,
                    font_family=self.theme['font_family'],
                    bold=True, alignment='CENTER',
                    color={'red': 1, 'green': 1, 'blue': 1}
                )
            
            # Section title
            self.api.add_formatted_text(
                self.presentation_id, slide_id, section_title,
                x=150 if section_number else 50, y=200, 
                width=500 if section_number else 600, height=100,
                font_size=48,
                font_family=self.theme['font_family'],
                bold=True, alignment='LEFT' if section_number else 'CENTER',
                color={'red': 1, 'green': 1, 'blue': 1}
            )
            
            self.slides.append({'id': slide_id, 'type': 'section', 'title': section_title})
        
        return slide_id
    
    def add_content_slide(self, title: str, content: List[str], 
                         layout: str = 'bullets', image_url: Optional[str] = None) -> str:
        """Add a content slide with various layout options"""
        slide_id = self.api.add_slide(self.presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_formatted_text(
                self.presentation_id, slide_id, title,
                x=50, y=30, width=600, height=60,
                font_size=self.theme['heading_font_size'],
                font_family=self.theme['font_family'],
                bold=True,
                color=self.theme['primary_color']
            )
            
            # Content area dimensions
            content_x = 50
            content_width = 600
            if image_url:
                content_width = 350  # Make room for image
            
            # Add content based on layout
            if layout == 'bullets':
                self.api.add_bullet_list(
                    self.presentation_id, slide_id, content,
                    x=content_x, y=120, width=content_width, height=300,
                    font_size=self.theme['body_font_size']
                )
            elif layout == 'numbered':
                numbered_items = [f"{i+1}. {item}" for i, item in enumerate(content)]
                text = '\n\n'.join(numbered_items)
                self.api.add_formatted_text(
                    self.presentation_id, slide_id, text,
                    x=content_x, y=120, width=content_width, height=300,
                    font_size=self.theme['body_font_size'],
                    font_family=self.theme['font_family']
                )
            else:  # paragraph
                text = '\n\n'.join(content)
                self.api.add_formatted_text(
                    self.presentation_id, slide_id, text,
                    x=content_x, y=120, width=content_width, height=300,
                    font_size=self.theme['body_font_size'],
                    font_family=self.theme['font_family']
                )
            
            # Add image if provided
            if image_url:
                self.api.add_image(
                    self.presentation_id, slide_id, image_url,
                    x=420, y=120, width=230, height=300
                )
            
            self.slides.append({'id': slide_id, 'type': 'content', 'title': title})
        
        return slide_id
    
    def add_comparison_slide(self, title: str, left_title: str, right_title: str,
                            left_items: List[str], right_items: List[str]) -> str:
        """Add a two-column comparison slide"""
        slide_id = self.api.add_slide(self.presentation_id, 'BLANK')
        
        if slide_id:
            # Main title
            self.api.add_formatted_text(
                self.presentation_id, slide_id, title,
                x=50, y=30, width=600, height=60,
                font_size=self.theme['heading_font_size'],
                font_family=self.theme['font_family'],
                bold=True,
                color=self.theme['primary_color']
            )
            
            # Left column
            self.api.add_formatted_text(
                self.presentation_id, slide_id, left_title,
                x=50, y=100, width=280, height=40,
                font_size=24,
                font_family=self.theme['font_family'],
                bold=True, alignment='CENTER',
                color=self.theme['accent_color']
            )
            
            self.api.add_bullet_list(
                self.presentation_id, slide_id, left_items,
                x=50, y=150, width=280, height=250,
                font_size=16
            )
            
            # Right column
            self.api.add_formatted_text(
                self.presentation_id, slide_id, right_title,
                x=370, y=100, width=280, height=40,
                font_size=24,
                font_family=self.theme['font_family'],
                bold=True, alignment='CENTER',
                color=self.theme['accent_color']
            )
            
            self.api.add_bullet_list(
                self.presentation_id, slide_id, right_items,
                x=370, y=150, width=280, height=250,
                font_size=16
            )
            
            # Divider line
            self.api.add_shape(
                self.presentation_id, slide_id, 'RECTANGLE',
                x=350, y=100, width=2, height=300,
                fill_color=self.theme['secondary_color']
            )
            
            self.slides.append({'id': slide_id, 'type': 'comparison', 'title': title})
        
        return slide_id
    
    def add_data_slide(self, title: str, data: List[List[str]], 
                      chart_type: Optional[str] = None) -> str:
        """Add a slide with data table and optional chart placeholder"""
        slide_id = self.api.add_slide(self.presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_formatted_text(
                self.presentation_id, slide_id, title,
                x=50, y=30, width=600, height=60,
                font_size=self.theme['heading_font_size'],
                font_family=self.theme['font_family'],
                bold=True,
                color=self.theme['primary_color']
            )
            
            # Calculate table dimensions
            rows = len(data)
            cols = len(data[0]) if data else 0
            table_width = 600 if not chart_type else 350
            
            # Create and fill table
            table_id = self.api.create_table(
                self.presentation_id, slide_id,
                rows=rows, columns=cols,
                x=50, y=120, width=table_width, height=250
            )
            
            if table_id:
                self.api.fill_table(self.presentation_id, table_id, data, header_row=True)
            
            # Add chart placeholder if requested
            if chart_type:
                self.api.add_shape(
                    self.presentation_id, slide_id, 'RECTANGLE',
                    x=420, y=120, width=230, height=250,
                    fill_color={'red': 0.95, 'green': 0.95, 'blue': 0.95}
                )
                
                self.api.add_formatted_text(
                    self.presentation_id, slide_id, f"{chart_type} Chart\n(Add in Google Slides)",
                    x=420, y=220, width=230, height=50,
                    font_size=14,
                    font_family=self.theme['font_family'],
                    alignment='CENTER',
                    color=self.theme['secondary_color']
                )
            
            self.slides.append({'id': slide_id, 'type': 'data', 'title': title})
        
        return slide_id
    
    def add_conclusion_slide(self, title: str, key_points: List[str], 
                           call_to_action: Optional[str] = None) -> str:
        """Add a conclusion slide"""
        slide_id = self.api.add_slide(self.presentation_id, 'BLANK')
        
        if slide_id:
            # Title
            self.api.add_formatted_text(
                self.presentation_id, slide_id, title,
                x=50, y=30, width=600, height=60,
                font_size=self.theme['heading_font_size'],
                font_family=self.theme['font_family'],
                bold=True,
                color=self.theme['primary_color']
            )
            
            # Key points
            self.api.add_bullet_list(
                self.presentation_id, slide_id, key_points,
                x=50, y=120, width=600, height=200,
                font_size=self.theme['body_font_size']
            )
            
            # Call to action
            if call_to_action:
                # Background shape
                self.api.add_shape(
                    self.presentation_id, slide_id, 'RECTANGLE',
                    x=50, y=350, width=600, height=80,
                    fill_color=self.theme['accent_color']
                )
                
                # Text
                self.api.add_formatted_text(
                    self.presentation_id, slide_id, call_to_action,
                    x=50, y=370, width=600, height=40,
                    font_size=24,
                    font_family=self.theme['font_family'],
                    bold=True, alignment='CENTER',
                    color={'red': 1, 'green': 1, 'blue': 1}
                )
            
            self.slides.append({'id': slide_id, 'type': 'conclusion', 'title': title})
        
        return slide_id
    
    def add_thank_you_slide(self, contact_info: Optional[Dict[str, str]] = None) -> str:
        """Add a thank you slide with optional contact information"""
        slide_id = self.api.add_slide(self.presentation_id, 'BLANK')
        
        if slide_id:
            # Background
            self.api.update_slide_properties(
                self.presentation_id, slide_id,
                background_color={'red': 0.98, 'green': 0.98, 'blue': 0.98}
            )
            
            # Thank you text
            self.api.add_formatted_text(
                self.presentation_id, slide_id, "Thank You!",
                x=50, y=150, width=600, height=100,
                font_size=56,
                font_family=self.theme['font_family'],
                bold=True, alignment='CENTER',
                color=self.theme['primary_color']
            )
            
            # Contact information
            if contact_info:
                contact_lines = []
                if 'name' in contact_info:
                    contact_lines.append(contact_info['name'])
                if 'email' in contact_info:
                    contact_lines.append(contact_info['email'])
                if 'phone' in contact_info:
                    contact_lines.append(contact_info['phone'])
                if 'website' in contact_info:
                    contact_lines.append(contact_info['website'])
                
                if contact_lines:
                    self.api.add_formatted_text(
                        self.presentation_id, slide_id, '\n'.join(contact_lines),
                        x=50, y=300, width=600, height=120,
                        font_size=18,
                        font_family=self.theme['font_family'],
                        alignment='CENTER',
                        color=self.theme['secondary_color']
                    )
            
            self.slides.append({'id': slide_id, 'type': 'thank_you'})
        
        return slide_id
    
    def export_outline(self, filename: str = 'presentation_outline.json'):
        """Export presentation outline to JSON"""
        outline = {
            'presentation_id': self.presentation_id,
            'created': datetime.now().isoformat(),
            'theme': self.theme,
            'slides': self.slides
        }
        
        with open(filename, 'w') as f:
            json.dump(outline, f, indent=2)
        
        print(f"📄 Exported outline to {filename}")
    
    def get_presentation_url(self) -> str:
        """Get the URL to view/edit the presentation"""
        return f"https://docs.google.com/presentation/d/{self.presentation_id}/edit"


def demo_presentation():
    """Create a demo presentation showcasing all features"""
    manager = PresentationManager()
    
    # Custom theme
    custom_theme = {
        'primary_color': {'red': 0.1, 'green': 0.3, 'blue': 0.6},
        'accent_color': {'red': 0.9, 'green': 0.5, 'blue': 0.1}
    }
    
    # Create presentation
    manager.create_presentation("Company Overview 2024", theme=custom_theme)
    
    # Title slide
    manager.add_title_slide(
        "Tech Innovations Inc.",
        "Annual Review 2024",
        "John Smith, CEO"
    )
    
    # Agenda
    manager.add_agenda_slide([
        "Company Overview",
        "Financial Performance",
        "Product Updates",
        "Market Analysis",
        "Future Roadmap"
    ])
    
    # Section 1
    manager.add_section_divider("Company Overview", 1)
    
    manager.add_content_slide(
        "Our Mission",
        [
            "Innovate cutting-edge technology solutions",
            "Deliver exceptional customer value",
            "Foster sustainable growth",
            "Build a diverse and inclusive workplace"
        ]
    )
    
    # Section 2
    manager.add_section_divider("Financial Performance", 2)
    
    manager.add_data_slide(
        "Quarterly Revenue",
        [
            ['Quarter', 'Revenue', 'Growth', 'Target'],
            ['Q1 2024', '$2.5M', '+15%', '✓'],
            ['Q2 2024', '$3.1M', '+24%', '✓'],
            ['Q3 2024', '$3.8M', '+22%', '✓'],
            ['Q4 2024', '$4.2M', '+11%', '✓']
        ],
        chart_type="Bar"
    )
    
    # Comparison slide
    manager.add_comparison_slide(
        "2023 vs 2024 Performance",
        "2023 Achievements",
        "2024 Achievements",
        [
            "$10M total revenue",
            "50 enterprise clients",
            "85% customer retention",
            "3 product launches"
        ],
        [
            "$13.6M total revenue",
            "75 enterprise clients",
            "92% customer retention",
            "5 product launches"
        ]
    )
    
    # Conclusion
    manager.add_conclusion_slide(
        "Key Takeaways",
        [
            "36% year-over-year revenue growth",
            "Successfully launched 5 new products",
            "Expanded to 3 new markets",
            "Maintained industry-leading customer satisfaction"
        ],
        "Join us in shaping the future of technology!"
    )
    
    # Thank you
    manager.add_thank_you_slide({
        'name': 'John Smith, CEO',
        'email': 'john.smith@techinnovations.com',
        'website': 'www.techinnovations.com'
    })
    
    # Export outline
    manager.export_outline()
    
    print(f"\n✅ Demo presentation created!")
    print(f"📎 View at: {manager.get_presentation_url()}")


if __name__ == '__main__':
    demo_presentation()
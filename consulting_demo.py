#!/usr/bin/env python3
"""
Comprehensive Demo of Consulting Platform
Shows all features needed for the SaaS MVP
"""

import os
from datetime import datetime
from consulting_platform import (
    ConsultingPlatform, CaseStudyData, ProposalData, BrandingConfig
)
from consulting_templates_extended import create_full_proposal
from export_manager import ExportManager
from dotenv import load_dotenv

load_dotenv()


def demo_complete_platform():
    """Demonstrate all platform features"""
    print("\n🚀 Consulting Platform Demo - Full Feature Showcase")
    print("=" * 60)
    
    # Initialize platform
    platform = ConsultingPlatform()
    
    # Company branding
    branding = BrandingConfig(
        company_name="Innovate Consulting Partners",
        primary_color={'red': 0.043, 'green': 0.145, 'blue': 0.278},  # Navy blue
        secondary_color={'red': 0.408, 'green': 0.408, 'blue': 0.408},  # Gray
        accent_color={'red': 0.957, 'green': 0.545, 'blue': 0.027},  # Orange
        font_family='Arial',
        tagline="Transforming Vision into Value",
        website="www.innovateconsulting.com"
    )
    
    # Demo 1: Create Case Study
    print("\n📊 Demo 1: Creating AI-Powered Case Study")
    print("-" * 40)
    
    case_study_data = CaseStudyData(
        client_name="GlobalRetail Corp",
        industry="Retail & E-commerce",
        challenge="Struggling with digital transformation, losing market share to online competitors, and dealing with outdated inventory management systems",
        solution="Implemented omnichannel retail platform with real-time inventory tracking, AI-powered demand forecasting, and seamless online-offline integration",
        results=[
            "35% increase in online revenue",
            "50% reduction in inventory costs",
            "Customer satisfaction score improved by 28%",
            "Time to market for new products reduced by 60%"
        ],
        timeline="8 months",
        team_size="15 consultants",
        technologies=["AWS Cloud", "React Native", "Machine Learning", "SAP Integration"],
        testimonial="Innovate Consulting Partners didn't just upgrade our technology – they transformed our entire business model. We're now a leader in omnichannel retail.",
        metrics={
            "Revenue Growth": "+$12.5M",
            "Cost Savings": "$3.2M/year",
            "ROI": "425%",
            "Efficiency Gain": "60%"
        }
    )
    
    case_study_id = platform.create_case_study(case_study_data, branding)
    
    # Demo 2: Create Proposal
    print("\n📋 Demo 2: Creating AI-Enhanced Proposal")
    print("-" * 40)
    
    proposal_data = ProposalData(
        client_name="TechStart Industries",
        project_name="Digital Transformation Initiative",
        executive_summary="A comprehensive digital transformation program to modernize TechStart's operations, enhance customer experience, and drive competitive advantage through cutting-edge technology solutions.",
        objectives=[
            "Modernize legacy systems to cloud-native architecture",
            "Implement data-driven decision making processes",
            "Enhance customer experience through digital channels",
            "Achieve 40% operational efficiency improvement"
        ],
        approach=[
            "Discovery & Assessment",
            "Strategy & Design",
            "Implementation & Migration",
            "Optimization & Support"
        ],
        deliverables=[
            "Current state assessment report",
            "Digital transformation roadmap",
            "Cloud migration plan",
            "New system implementation",
            "Team training and documentation"
        ],
        timeline_weeks=16,
        team_members=[
            {"name": "Sarah Chen", "role": "Engagement Lead"},
            {"name": "Michael Ross", "role": "Technical Architect"},
            {"name": "Emma Wilson", "role": "Data Scientist"},
            {"name": "James Park", "role": "UX Designer"},
            {"name": "Lisa Kumar", "role": "Change Management"},
            {"name": "David Lee", "role": "Cloud Engineer"}
        ],
        budget_range="$850,000 - $1,200,000",
        next_steps=[
            "Schedule discovery workshop",
            "Sign engagement letter",
            "Kick off project within 2 weeks"
        ]
    )
    
    # Generate AI content for proposal
    ai_content = platform.ai.generate_proposal_content(proposal_data)
    
    # Create full proposal
    proposal_id = create_full_proposal(
        platform.api, proposal_data, branding, ai_content
    )
    
    # Demo 3: Asset Library
    print("\n📁 Demo 3: Asset Library Management")
    print("-" * 40)
    
    # Add reusable assets
    platform.assets.add_text_snippet(
        "value_prop_retail",
        "We help retail companies thrive in the digital age through innovative technology solutions and strategic transformation.",
        category="retail"
    )
    
    platform.assets.add_text_snippet(
        "methodology_overview",
        "Our proven 4-phase methodology ensures successful delivery: Discover, Design, Deliver, Optimize.",
        category="general"
    )
    
    platform.assets.add_image(
        "company_logo",
        "https://example.com/logo.png",
        category="branding"
    )
    
    print("✅ Added reusable assets to library")
    
    # Demo 4: Slide Editor Operations
    print("\n✏️ Demo 4: Slide Editor Capabilities")
    print("-" * 40)
    
    if case_study_id:
        # Get presentation details
        presentation = platform.api.get_presentation(case_study_id)
        if presentation and presentation.get('slides'):
            slides = presentation['slides']
            
            # Demonstrate reordering
            if len(slides) > 2:
                # Move third slide to second position
                platform.editor.reorder_slides(
                    case_study_id, 
                    slides[2]['objectId'], 
                    1
                )
                print("✅ Reordered slides")
            
            # Demonstrate duplication
            if slides:
                duplicated_id = platform.api.duplicate_slide(
                    case_study_id,
                    slides[0]['objectId']
                )
                if duplicated_id:
                    print("✅ Duplicated slide")
    
    # Demo 5: Export Functionality
    print("\n📤 Demo 5: Export Capabilities")
    print("-" * 40)
    
    # Initialize export manager
    export_manager = ExportManager(platform.api.creds)
    
    # Create export directory
    export_dir = "./exports"
    os.makedirs(export_dir, exist_ok=True)
    
    if case_study_id:
        # Export as PDF
        pdf_path = os.path.join(export_dir, "case_study.pdf")
        export_manager.export_as_pdf(case_study_id, pdf_path)
        
        # Export as PPTX
        pptx_path = os.path.join(export_dir, "case_study.pptx")
        export_manager.export_as_pptx(case_study_id, pptx_path)
        
        # Generate HTML preview
        html_path = os.path.join(export_dir, "case_study_preview.html")
        export_manager.generate_html_preview(case_study_id, html_path)
    
    # Demo 6: Branding Application
    print("\n🎨 Demo 6: Dynamic Branding Application")
    print("-" * 40)
    
    # Create alternative branding
    alt_branding = BrandingConfig(
        company_name="Tech Advisory Group",
        primary_color={'red': 0.522, 'green': 0.078, 'blue': 0.294},  # Burgundy
        secondary_color={'red': 0.302, 'green': 0.302, 'blue': 0.302},  # Dark gray
        accent_color={'red': 0.122, 'green': 0.722, 'blue': 0.451},  # Green
        tagline="Strategic Technology Leadership"
    )
    
    # Create case study with different branding
    alt_case_study_id = platform.create_case_study(case_study_data, alt_branding)
    print("✅ Created presentation with alternative branding")
    
    # Summary
    print("\n📊 Demo Summary")
    print("=" * 60)
    print("✅ AI-Powered Content Generation")
    print("✅ Multiple Presentation Types (Case Studies & Proposals)")
    print("✅ Reusable Asset Library")
    print("✅ Slide Editor Functions")
    print("✅ Multi-Format Export (PDF, PPTX, HTML)")
    print("✅ Dynamic Branding System")
    print("\n🔗 Created Presentations:")
    
    if case_study_id:
        print(f"   Case Study: https://docs.google.com/presentation/d/{case_study_id}/edit")
    if proposal_id:
        print(f"   Proposal: https://docs.google.com/presentation/d/{proposal_id}/edit")
    if alt_case_study_id:
        print(f"   Alt Branding: https://docs.google.com/presentation/d/{alt_case_study_id}/edit")
    
    print("\n💡 Platform Ready for Pilot!")
    print("   - AI content generation ✓")
    print("   - Google Slides integration ✓")
    print("   - Editor capabilities ✓")
    print("   - Asset management ✓")
    print("   - Export functionality ✓")
    print("   - Branding controls ✓")


def demo_quick_case_study():
    """Quick demo - just create a case study"""
    platform = ConsultingPlatform()
    
    branding = BrandingConfig(
        company_name="Quick Consulting Co",
        primary_color={'red': 0.2, 'green': 0.4, 'blue': 0.8},
        secondary_color={'red': 0.5, 'green': 0.5, 'blue': 0.5},
        accent_color={'red': 0.9, 'green': 0.3, 'blue': 0.2}
    )
    
    case_study = CaseStudyData(
        client_name="Sample Client",
        industry="Technology",
        challenge="Needed to scale their infrastructure",
        solution="Implemented cloud-native architecture",
        results=["50% cost reduction", "3x performance improvement"],
        timeline="3 months",
        team_size="5 consultants",
        technologies=["AWS", "Kubernetes"],
        metrics={"Cost Savings": "$500K", "Performance": "+300%"}
    )
    
    presentation_id = platform.create_case_study(case_study, branding)
    return presentation_id


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        # Quick demo
        print("\n🚀 Running quick case study demo...")
        demo_quick_case_study()
    else:
        # Full demo
        demo_complete_platform()
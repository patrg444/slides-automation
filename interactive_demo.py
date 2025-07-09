#!/usr/bin/env python3
"""
Interactive Google Slides API Demo
Menu-driven interface for testing various API features
"""

import os
from datetime import datetime
from google_slides_enhanced import GoogleSlidesEnhanced
from presentation_manager import PresentationManager


class InteractiveDemo:
    def __init__(self):
        self.api = GoogleSlidesEnhanced()
        self.manager = PresentationManager()
        self.current_presentation_id = None
        self.current_slide_id = None
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("🎯 Google Slides API Interactive Demo")
        print("="*60)
        
        if self.current_presentation_id:
            print(f"📊 Current presentation: {self.current_presentation_id}")
            print(f"🔗 View at: https://docs.google.com/presentation/d/{self.current_presentation_id}/edit")
        else:
            print("📊 No presentation loaded")
        
        print("\n--- Presentation Management ---")
        print("1. Create new presentation")
        print("2. Create demo presentation (with manager)")
        print("3. Load existing presentation")
        
        print("\n--- Slide Operations ---")
        print("4. Add slide")
        print("5. List all slides")
        print("6. Duplicate current slide")
        
        print("\n--- Content Operations ---")
        print("7. Add text box")
        print("8. Add formatted text")
        print("9. Add bullet list")
        print("10. Add table")
        print("11. Add shapes")
        print("12. Add image from URL")
        
        print("\n--- Advanced Features ---")
        print("13. Change slide background")
        print("14. Create title slide")
        print("15. Create comparison slide")
        print("16. Create data visualization slide")
        
        print("\n--- Utilities ---")
        print("17. Run automated test suite")
        print("18. Export presentation outline")
        print("0. Exit")
        
        print("="*60)
    
    def create_new_presentation(self):
        """Create a new presentation"""
        title = input("Enter presentation title: ") or f"Demo {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        self.current_presentation_id = self.api.create_presentation(title)
        if self.current_presentation_id:
            print(f"✅ Created presentation: {title}")
    
    def create_demo_presentation(self):
        """Create a full demo presentation using the manager"""
        print("\n🎨 Creating demo presentation with multiple slides...")
        
        title = input("Enter presentation title: ") or "API Demo Presentation"
        self.current_presentation_id = self.manager.create_presentation(title)
        
        # Add various slides
        self.manager.add_title_slide(
            "Google Slides API Demo",
            "Showcasing API Capabilities",
            "Created with Python"
        )
        
        self.manager.add_agenda_slide([
            "Basic Text Operations",
            "Advanced Formatting",
            "Tables and Data",
            "Shapes and Graphics",
            "Layouts and Templates"
        ])
        
        self.manager.add_content_slide(
            "Key Features",
            [
                "Programmatic slide creation",
                "Rich text formatting",
                "Table management",
                "Shape and image insertion",
                "Batch operations for efficiency"
            ]
        )
        
        self.manager.add_data_slide(
            "Sample Data",
            [
                ['Feature', 'Status', 'Performance'],
                ['Text API', 'Stable', '99.9%'],
                ['Shape API', 'Stable', '99.8%'],
                ['Table API', 'Stable', '99.7%']
            ]
        )
        
        self.manager.add_thank_you_slide({
            'name': 'Google Slides API',
            'website': 'developers.google.com/slides'
        })
        
        print(f"✅ Demo presentation created with {len(self.manager.slides)} slides")
    
    def load_presentation(self):
        """Load an existing presentation"""
        presentation_id = input("Enter presentation ID: ").strip()
        if presentation_id:
            # Verify it exists
            pres = self.api.get_presentation(presentation_id)
            if pres:
                self.current_presentation_id = presentation_id
                print(f"✅ Loaded presentation: {pres.get('title', 'Untitled')}")
            else:
                print("❌ Could not load presentation")
    
    def add_slide(self):
        """Add a new slide"""
        if not self.current_presentation_id:
            print("❌ No presentation loaded")
            return
        
        print("\nAvailable layouts:")
        layouts = ['BLANK', 'TITLE', 'TITLE_AND_BODY', 'TITLE_AND_TWO_COLUMNS', 
                  'TITLE_ONLY', 'SECTION_HEADER', 'SECTION_TITLE_AND_DESCRIPTION',
                  'ONE_COLUMN_TEXT', 'MAIN_POINT', 'BIG_NUMBER']
        
        for i, layout in enumerate(layouts):
            print(f"{i+1}. {layout}")
        
        choice = input("\nSelect layout (1-10) or press Enter for BLANK: ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(layouts):
            layout = layouts[int(choice)-1]
        else:
            layout = 'BLANK'
        
        self.current_slide_id = self.api.add_slide(self.current_presentation_id, layout)
        if self.current_slide_id:
            print(f"✅ Added {layout} slide")
    
    def add_text_box(self):
        """Add a text box to current slide"""
        if not self.current_presentation_id or not self.current_slide_id:
            print("❌ No presentation or slide selected")
            return
        
        text = input("Enter text: ")
        x = int(input("X position (default 100): ") or "100")
        y = int(input("Y position (default 100): ") or "100")
        
        element_id = self.api.add_text_box(
            self.current_presentation_id, 
            self.current_slide_id, 
            text, x, y
        )
        
        if element_id:
            print("✅ Text box added")
    
    def add_formatted_text(self):
        """Add formatted text"""
        if not self.current_presentation_id or not self.current_slide_id:
            print("❌ No presentation or slide selected")
            return
        
        text = input("Enter text: ")
        font_size = int(input("Font size (default 18): ") or "18")
        bold = input("Bold? (y/n): ").lower() == 'y'
        italic = input("Italic? (y/n): ").lower() == 'y'
        
        # Color input
        use_color = input("Use custom color? (y/n): ").lower() == 'y'
        color = None
        if use_color:
            r = float(input("Red (0-1): ") or "0")
            g = float(input("Green (0-1): ") or "0")
            b = float(input("Blue (0-1): ") or "0")
            color = {'red': r, 'green': g, 'blue': b}
        
        element_id = self.api.add_formatted_text(
            self.current_presentation_id,
            self.current_slide_id,
            text,
            font_size=font_size,
            bold=bold,
            italic=italic,
            color=color
        )
        
        if element_id:
            print("✅ Formatted text added")
    
    def add_bullet_list(self):
        """Add a bullet list"""
        if not self.current_presentation_id or not self.current_slide_id:
            print("❌ No presentation or slide selected")
            return
        
        print("Enter list items (empty line to finish):")
        items = []
        while True:
            item = input(f"Item {len(items)+1}: ")
            if not item:
                break
            items.append(item)
        
        if items:
            element_id = self.api.add_bullet_list(
                self.current_presentation_id,
                self.current_slide_id,
                items
            )
            if element_id:
                print(f"✅ Added bullet list with {len(items)} items")
    
    def add_table(self):
        """Add a table"""
        if not self.current_presentation_id or not self.current_slide_id:
            print("❌ No presentation or slide selected")
            return
        
        rows = int(input("Number of rows: ") or "3")
        cols = int(input("Number of columns: ") or "3")
        
        table_id = self.api.create_table(
            self.current_presentation_id,
            self.current_slide_id,
            rows, cols
        )
        
        if table_id:
            print("✅ Table created")
            
            # Offer to fill with sample data
            if input("Fill with sample data? (y/n): ").lower() == 'y':
                data = []
                for r in range(rows):
                    row_data = []
                    for c in range(cols):
                        if r == 0:
                            cell = input(f"Header {c+1}: ") or f"Column {c+1}"
                        else:
                            cell = input(f"Row {r}, Col {c+1}: ") or f"Data {r},{c+1}"
                        row_data.append(cell)
                    data.append(row_data)
                
                self.api.fill_table(
                    self.current_presentation_id,
                    table_id,
                    data,
                    header_row=True
                )
                print("✅ Table filled with data")
    
    def add_shapes(self):
        """Add shapes to slide"""
        if not self.current_presentation_id or not self.current_slide_id:
            print("❌ No presentation or slide selected")
            return
        
        shapes = ['RECTANGLE', 'ELLIPSE', 'TRIANGLE', 'DIAMOND', 'ROUND_RECTANGLE',
                 'PARALLELOGRAM', 'TRAPEZOID', 'PENTAGON', 'HEXAGON', 'OCTAGON']
        
        print("\nAvailable shapes:")
        for i, shape in enumerate(shapes):
            print(f"{i+1}. {shape}")
        
        choice = input("\nSelect shape (1-10): ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(shapes):
            shape_type = shapes[int(choice)-1]
            
            # Get color
            r = float(input("Fill color - Red (0-1): ") or "0.5")
            g = float(input("Fill color - Green (0-1): ") or "0.5")
            b = float(input("Fill color - Blue (0-1): ") or "0.5")
            
            shape_id = self.api.add_shape(
                self.current_presentation_id,
                self.current_slide_id,
                shape_type,
                fill_color={'red': r, 'green': g, 'blue': b}
            )
            
            if shape_id:
                print(f"✅ Added {shape_type} shape")
    
    def change_background(self):
        """Change slide background"""
        if not self.current_presentation_id or not self.current_slide_id:
            print("❌ No presentation or slide selected")
            return
        
        print("\nBackground options:")
        print("1. Solid color")
        print("2. Image from URL")
        
        choice = input("Select option: ")
        
        if choice == "1":
            r = float(input("Red (0-1): ") or "1")
            g = float(input("Green (0-1): ") or "1")
            b = float(input("Blue (0-1): ") or "1")
            
            success = self.api.update_slide_properties(
                self.current_presentation_id,
                self.current_slide_id,
                background_color={'red': r, 'green': g, 'blue': b}
            )
            
            if success:
                print("✅ Background color updated")
        
        elif choice == "2":
            url = input("Enter image URL: ")
            success = self.api.update_slide_properties(
                self.current_presentation_id,
                self.current_slide_id,
                background_image_url=url
            )
            
            if success:
                print("✅ Background image set")
    
    def run_test_suite(self):
        """Run automated test suite"""
        print("\n🧪 Running automated test suite...")
        
        # Create test presentation
        test_id = self.api.create_presentation(f"Automated Test {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        if test_id:
            # Test various operations
            tests_passed = 0
            tests_total = 10
            
            # Test 1: Add blank slide
            slide1 = self.api.add_slide(test_id, 'BLANK')
            if slide1:
                tests_passed += 1
                print("✅ Test 1: Add blank slide - PASSED")
            else:
                print("❌ Test 1: Add blank slide - FAILED")
            
            # Test 2: Add text box
            if slide1:
                text_id = self.api.add_text_box(test_id, slide1, "Test text")
                if text_id:
                    tests_passed += 1
                    print("✅ Test 2: Add text box - PASSED")
                else:
                    print("❌ Test 2: Add text box - FAILED")
            
            # Test 3: Add formatted text
            if slide1:
                fmt_id = self.api.add_formatted_text(
                    test_id, slide1, "Formatted text",
                    font_size=24, bold=True, color={'red': 1, 'green': 0, 'blue': 0}
                )
                if fmt_id:
                    tests_passed += 1
                    print("✅ Test 3: Add formatted text - PASSED")
                else:
                    print("❌ Test 3: Add formatted text - FAILED")
            
            # Test 4: Add bullet list
            slide2 = self.api.add_slide(test_id, 'BLANK')
            if slide2:
                list_id = self.api.add_bullet_list(
                    test_id, slide2, ["Item 1", "Item 2", "Item 3"]
                )
                if list_id:
                    tests_passed += 1
                    print("✅ Test 4: Add bullet list - PASSED")
                else:
                    print("❌ Test 4: Add bullet list - FAILED")
            
            # Test 5: Create table
            if slide2:
                table_id = self.api.create_table(test_id, slide2, 3, 3)
                if table_id:
                    tests_passed += 1
                    print("✅ Test 5: Create table - PASSED")
                else:
                    print("❌ Test 5: Create table - FAILED")
            
            # Test 6: Add shape
            slide3 = self.api.add_slide(test_id, 'BLANK')
            if slide3:
                shape_id = self.api.add_shape(
                    test_id, slide3, 'RECTANGLE',
                    fill_color={'red': 0, 'green': 0.5, 'blue': 1}
                )
                if shape_id:
                    tests_passed += 1
                    print("✅ Test 6: Add shape - PASSED")
                else:
                    print("❌ Test 6: Add shape - FAILED")
            
            # Test 7: Update slide background
            if slide3:
                success = self.api.update_slide_properties(
                    test_id, slide3,
                    background_color={'red': 0.9, 'green': 0.9, 'blue': 0.9}
                )
                if success:
                    tests_passed += 1
                    print("✅ Test 7: Update slide background - PASSED")
                else:
                    print("❌ Test 7: Update slide background - FAILED")
            
            # Test 8: Duplicate slide
            if slide1:
                dup_id = self.api.duplicate_slide(test_id, slide1)
                if dup_id:
                    tests_passed += 1
                    print("✅ Test 8: Duplicate slide - PASSED")
                else:
                    print("❌ Test 8: Duplicate slide - FAILED")
            
            # Test 9: Get presentation
            pres = self.api.get_presentation(test_id)
            if pres:
                tests_passed += 1
                print("✅ Test 9: Get presentation - PASSED")
            else:
                print("❌ Test 9: Get presentation - FAILED")
            
            # Test 10: Add titled slide
            title_slide = self.api.add_slide(test_id, 'TITLE')
            if title_slide:
                tests_passed += 1
                print("✅ Test 10: Add titled slide - PASSED")
            else:
                print("❌ Test 10: Add titled slide - FAILED")
            
            print(f"\n📊 Test Results: {tests_passed}/{tests_total} passed")
            print(f"🔗 View test presentation: https://docs.google.com/presentation/d/{test_id}/edit")
    
    def list_slides(self):
        """List all slides in the presentation"""
        if not self.current_presentation_id:
            print("❌ No presentation loaded")
            return
        
        presentation = self.api.get_presentation(self.current_presentation_id)
        if presentation:
            slides = presentation.get('slides', [])
            print(f"\n📑 Presentation has {len(slides)} slides:")
            
            for i, slide in enumerate(slides):
                slide_id = slide.get('objectId')
                elements = slide.get('pageElements', [])
                print(f"\n  Slide {i+1} (ID: {slide_id})")
                print(f"  Elements: {len(elements)}")
                
                # Show slide selection option
                if i == len(slides) - 1:
                    select = input("\nSelect a slide number to make it current (or press Enter to skip): ")
                    if select.isdigit() and 1 <= int(select) <= len(slides):
                        self.current_slide_id = slides[int(select)-1].get('objectId')
                        print(f"✅ Selected slide {select}")
    
    def run(self):
        """Main loop"""
        print("\n🎨 Welcome to Google Slides API Interactive Demo!")
        print("This tool helps you test various Google Slides API features.")
        
        while True:
            self.display_menu()
            choice = input("\nSelect option: ").strip()
            
            if choice == '0':
                print("\n👋 Goodbye!")
                break
            elif choice == '1':
                self.create_new_presentation()
            elif choice == '2':
                self.create_demo_presentation()
            elif choice == '3':
                self.load_presentation()
            elif choice == '4':
                self.add_slide()
            elif choice == '5':
                self.list_slides()
            elif choice == '6':
                if self.current_slide_id:
                    new_id = self.api.duplicate_slide(self.current_presentation_id, self.current_slide_id)
                    if new_id:
                        self.current_slide_id = new_id
                        print("✅ Slide duplicated")
                else:
                    print("❌ No slide selected")
            elif choice == '7':
                self.add_text_box()
            elif choice == '8':
                self.add_formatted_text()
            elif choice == '9':
                self.add_bullet_list()
            elif choice == '10':
                self.add_table()
            elif choice == '11':
                self.add_shapes()
            elif choice == '12':
                if self.current_presentation_id and self.current_slide_id:
                    url = input("Enter image URL: ")
                    self.api.add_image(self.current_presentation_id, self.current_slide_id, url)
                else:
                    print("❌ No presentation or slide selected")
            elif choice == '13':
                self.change_background()
            elif choice == '14':
                if self.current_presentation_id:
                    title = input("Enter title: ")
                    subtitle = input("Enter subtitle (optional): ")
                    slide_id = self.api.create_title_slide(self.current_presentation_id, title, subtitle)
                    if slide_id:
                        self.current_slide_id = slide_id
                else:
                    print("❌ No presentation loaded")
            elif choice == '15':
                if self.current_presentation_id:
                    self.current_slide_id = self.manager.add_comparison_slide(
                        "Comparison",
                        "Option A", "Option B",
                        ["Feature 1", "Feature 2"], ["Feature A", "Feature B"]
                    )
                else:
                    print("❌ No presentation loaded")
            elif choice == '16':
                if self.current_presentation_id:
                    self.current_slide_id = self.manager.add_data_slide(
                        "Data Visualization",
                        [['Category', 'Value'], ['A', '100'], ['B', '200']],
                        chart_type="Bar"
                    )
                else:
                    print("❌ No presentation loaded")
            elif choice == '17':
                self.run_test_suite()
            elif choice == '18':
                if self.manager.presentation_id:
                    self.manager.export_outline()
                else:
                    print("❌ No presentation created with manager")
            else:
                print("❌ Invalid option")
            
            input("\nPress Enter to continue...")


if __name__ == '__main__':
    demo = InteractiveDemo()
    demo.run()
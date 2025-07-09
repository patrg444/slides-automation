#!/usr/bin/env python3
"""
Web Interface for Consulting Platform
Simple Flask app for creating presentations via web UI
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from consulting_platform import (
    ConsultingPlatform, CaseStudyData, ProposalData, BrandingConfig
)
from export_manager import ExportManager

app = Flask(__name__)
CORS(app)

# Global platform instance
platform = ConsultingPlatform()


@app.route('/')
def index():
    """Main page"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Consulting Platform - AI Presentation Generator</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: #1a237e;
            color: white;
            padding: 30px 0;
            text-align: center;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #333;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        .btn {
            background: #1976d2;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            margin-right: 10px;
        }
        .btn:hover {
            background: #1565c0;
        }
        .btn-secondary {
            background: #757575;
        }
        .btn-secondary:hover {
            background: #616161;
        }
        .success {
            background: #4caf50;
            color: white;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }
        .error {
            background: #f44336;
            color: white;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .tabs {
            display: flex;
            border-bottom: 2px solid #ddd;
            margin-bottom: 20px;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            background: none;
            border: none;
            font-size: 16px;
            border-bottom: 3px solid transparent;
        }
        .tab.active {
            color: #1976d2;
            border-bottom-color: #1976d2;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        #loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #1976d2;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI-Powered Consulting Presentation Generator</h1>
        <p>Transform your project materials into professional presentations</p>
    </div>
    
    <div class="container">
        <div class="tabs">
            <button class="tab active" onclick="showTab('case-study')">Case Study</button>
            <button class="tab" onclick="showTab('proposal')">Proposal</button>
            <button class="tab" onclick="showTab('branding')">Branding</button>
        </div>
        
        <!-- Case Study Form -->
        <div id="case-study" class="tab-content active">
            <div class="card">
                <h2>Create Case Study</h2>
                <form id="caseStudyForm">
                    <div class="grid">
                        <div class="form-group">
                            <label>Client Name</label>
                            <input type="text" name="client_name" required>
                        </div>
                        <div class="form-group">
                            <label>Industry</label>
                            <input type="text" name="industry" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Challenge</label>
                        <textarea name="challenge" required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label>Solution</label>
                        <textarea name="solution" required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label>Results (one per line)</label>
                        <textarea name="results" placeholder="50% cost reduction&#10;3x performance improvement" required></textarea>
                    </div>
                    
                    <div class="grid">
                        <div class="form-group">
                            <label>Timeline</label>
                            <input type="text" name="timeline" placeholder="e.g., 6 months">
                        </div>
                        <div class="form-group">
                            <label>Team Size</label>
                            <input type="text" name="team_size" placeholder="e.g., 10 consultants">
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Technologies (comma-separated)</label>
                        <input type="text" name="technologies" placeholder="AWS, Python, React">
                    </div>
                    
                    <div class="form-group">
                        <label>Testimonial (optional)</label>
                        <textarea name="testimonial"></textarea>
                    </div>
                    
                    <button type="submit" class="btn">Generate Case Study</button>
                </form>
            </div>
        </div>
        
        <!-- Proposal Form -->
        <div id="proposal" class="tab-content">
            <div class="card">
                <h2>Create Proposal</h2>
                <form id="proposalForm">
                    <div class="grid">
                        <div class="form-group">
                            <label>Client Name</label>
                            <input type="text" name="client_name" required>
                        </div>
                        <div class="form-group">
                            <label>Project Name</label>
                            <input type="text" name="project_name" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Executive Summary</label>
                        <textarea name="executive_summary" required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label>Objectives (one per line)</label>
                        <textarea name="objectives" required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label>Approach Phases (one per line)</label>
                        <textarea name="approach" required></textarea>
                    </div>
                    
                    <div class="grid">
                        <div class="form-group">
                            <label>Timeline (weeks)</label>
                            <input type="number" name="timeline_weeks" required>
                        </div>
                        <div class="form-group">
                            <label>Budget Range</label>
                            <input type="text" name="budget_range" placeholder="$100K - $250K" required>
                        </div>
                    </div>
                    
                    <button type="submit" class="btn">Generate Proposal</button>
                </form>
            </div>
        </div>
        
        <!-- Branding Settings -->
        <div id="branding" class="tab-content">
            <div class="card">
                <h2>Branding Settings</h2>
                <form id="brandingForm">
                    <div class="form-group">
                        <label>Company Name</label>
                        <input type="text" id="company_name" value="Your Consulting Firm">
                    </div>
                    
                    <div class="grid">
                        <div class="form-group">
                            <label>Primary Color</label>
                            <input type="color" id="primary_color" value="#1a237e">
                        </div>
                        <div class="form-group">
                            <label>Accent Color</label>
                            <input type="color" id="accent_color" value="#ff6f00">
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Tagline</label>
                        <input type="text" id="tagline" placeholder="Your company tagline">
                    </div>
                    
                    <button type="button" class="btn" onclick="saveBranding()">Save Branding</button>
                </form>
            </div>
        </div>
        
        <!-- Results -->
        <div id="results" style="display: none;">
            <div class="card">
                <h2>Generated Presentation</h2>
                <div id="resultContent"></div>
            </div>
        </div>
        
        <!-- Loading -->
        <div id="loading">
            <div class="spinner"></div>
            <p>Generating your presentation with AI...</p>
        </div>
    </div>
    
    <script>
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        // Handle case study form
        document.getElementById('caseStudyForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            // Process arrays
            data.results = data.results.split('\\n').filter(r => r.trim());
            data.technologies = data.technologies.split(',').map(t => t.trim());
            
            // Get branding
            const branding = getBranding();
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            try {
                const response = await fetch('/api/create-case-study', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({data, branding})
                });
                
                const result = await response.json();
                showResult(result);
            } catch (error) {
                showError(error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        // Handle proposal form
        document.getElementById('proposalForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            // Process arrays
            data.objectives = data.objectives.split('\\n').filter(o => o.trim());
            data.approach = data.approach.split('\\n').filter(a => a.trim());
            data.timeline_weeks = parseInt(data.timeline_weeks);
            
            // Get branding
            const branding = getBranding();
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            try {
                const response = await fetch('/api/create-proposal', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({data, branding})
                });
                
                const result = await response.json();
                showResult(result);
            } catch (error) {
                showError(error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        function getBranding() {
            return {
                company_name: document.getElementById('company_name').value,
                primary_color: hexToRgb(document.getElementById('primary_color').value),
                accent_color: hexToRgb(document.getElementById('accent_color').value),
                tagline: document.getElementById('tagline').value
            };
        }
        
        function hexToRgb(hex) {
            const result = /^#?([a-f\\d]{2})([a-f\\d]{2})([a-f\\d]{2})$/i.exec(hex);
            return result ? {
                red: parseInt(result[1], 16) / 255,
                green: parseInt(result[2], 16) / 255,
                blue: parseInt(result[3], 16) / 255
            } : null;
        }
        
        function showResult(result) {
            const resultsDiv = document.getElementById('results');
            const resultContent = document.getElementById('resultContent');
            
            if (result.success) {
                resultContent.innerHTML = `
                    <div class="success">
                        <h3>✅ Presentation Created Successfully!</h3>
                        <p><strong>Presentation ID:</strong> ${result.presentation_id}</p>
                        <div style="margin-top: 20px;">
                            <a href="${result.url}" target="_blank" class="btn">Open in Google Slides</a>
                            <button class="btn btn-secondary" onclick="exportPresentation('${result.presentation_id}', 'pdf')">Export as PDF</button>
                            <button class="btn btn-secondary" onclick="exportPresentation('${result.presentation_id}', 'pptx')">Export as PPTX</button>
                        </div>
                    </div>
                `;
            } else {
                resultContent.innerHTML = `
                    <div class="error">
                        <h3>❌ Error</h3>
                        <p>${result.error}</p>
                    </div>
                `;
            }
            
            resultsDiv.style.display = 'block';
        }
        
        function showError(message) {
            const resultsDiv = document.getElementById('results');
            const resultContent = document.getElementById('resultContent');
            
            resultContent.innerHTML = `
                <div class="error">
                    <h3>❌ Error</h3>
                    <p>${message}</p>
                </div>
            `;
            
            resultsDiv.style.display = 'block';
        }
        
        async function exportPresentation(presentationId, format) {
            try {
                const response = await fetch(`/api/export/${presentationId}/${format}`);
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `presentation.${format}`;
                    a.click();
                }
            } catch (error) {
                showError('Export failed: ' + error.message);
            }
        }
        
        function saveBranding() {
            alert('Branding settings saved!');
        }
    </script>
</body>
</html>
    '''


@app.route('/api/create-case-study', methods=['POST'])
def create_case_study():
    """API endpoint to create case study"""
    try:
        request_data = request.json
        data = request_data['data']
        branding_data = request_data['branding']
        
        # Create data objects
        case_study = CaseStudyData(
            client_name=data['client_name'],
            industry=data['industry'],
            challenge=data['challenge'],
            solution=data['solution'],
            results=data['results'],
            timeline=data.get('timeline', ''),
            team_size=data.get('team_size', ''),
            technologies=data.get('technologies', []),
            testimonial=data.get('testimonial', ''),
            metrics={}
        )
        
        branding = BrandingConfig(
            company_name=branding_data['company_name'],
            primary_color=branding_data['primary_color'],
            secondary_color={'red': 0.5, 'green': 0.5, 'blue': 0.5},
            accent_color=branding_data['accent_color'],
            tagline=branding_data.get('tagline', '')
        )
        
        # Create presentation
        presentation_id = platform.create_case_study(case_study, branding)
        
        if presentation_id:
            return jsonify({
                'success': True,
                'presentation_id': presentation_id,
                'url': f'https://docs.google.com/presentation/d/{presentation_id}/edit'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create presentation'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/create-proposal', methods=['POST'])
def create_proposal():
    """API endpoint to create proposal"""
    try:
        request_data = request.json
        data = request_data['data']
        branding_data = request_data['branding']
        
        # Create data objects
        proposal = ProposalData(
            client_name=data['client_name'],
            project_name=data['project_name'],
            executive_summary=data['executive_summary'],
            objectives=data['objectives'],
            approach=data['approach'],
            deliverables=[],  # Would be added in full implementation
            timeline_weeks=data['timeline_weeks'],
            team_members=[],  # Would be added in full implementation
            budget_range=data['budget_range'],
            next_steps=['Schedule kickoff meeting', 'Sign agreement', 'Begin project']
        )
        
        branding = BrandingConfig(
            company_name=branding_data['company_name'],
            primary_color=branding_data['primary_color'],
            secondary_color={'red': 0.5, 'green': 0.5, 'blue': 0.5},
            accent_color=branding_data['accent_color'],
            tagline=branding_data.get('tagline', '')
        )
        
        # Create presentation
        from consulting_templates_extended import create_full_proposal
        ai_content = platform.ai.generate_proposal_content(proposal)
        presentation_id = create_full_proposal(platform.api, proposal, branding, ai_content)
        
        if presentation_id:
            return jsonify({
                'success': True,
                'presentation_id': presentation_id,
                'url': f'https://docs.google.com/presentation/d/{presentation_id}/edit'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create presentation'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/export/<presentation_id>/<format>')
def export_presentation(presentation_id, format):
    """Export presentation in requested format"""
    try:
        export_manager = ExportManager(platform.api.creds)
        
        if format == 'pdf':
            output_path = f'/tmp/{presentation_id}.pdf'
            export_manager.export_as_pdf(presentation_id, output_path)
            return send_file(output_path, as_attachment=True)
        
        elif format == 'pptx':
            output_path = f'/tmp/{presentation_id}.pptx'
            export_manager.export_as_pptx(presentation_id, output_path)
            return send_file(output_path, as_attachment=True)
        
        else:
            return jsonify({'error': 'Invalid format'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
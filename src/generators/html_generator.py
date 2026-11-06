"""
HTML Generator for Business Plans
Creates responsive HTML business plans with CSS styling
"""
from jinja2 import Template
from datetime import datetime
from typing import Dict, Any
import os


class HTMLGenerator:
    """Generate HTML business plans"""
    
    def __init__(self):
        self.template = self._create_template()
    
    def _create_template(self) -> Template:
        """Create Jinja2 HTML template"""
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ business_name }} - Business Plan</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        .cover-page {
            padding: 100px 50px;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .cover-page h1 {
            font-size: 3em;
            margin-bottom: 20px;
        }
        
        .cover-page h2 {
            font-size: 1.5em;
            font-weight: 300;
            margin-bottom: 40px;
        }
        
        .cover-page .info {
            font-size: 1.1em;
            line-height: 2;
        }
        
        .content {
            padding: 50px;
        }
        
        .section {
            margin-bottom: 50px;
            page-break-inside: avoid;
        }
        
        h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        h2 {
            color: #34495e;
            font-size: 1.8em;
            margin-bottom: 15px;
            margin-top: 30px;
        }
        
        h3 {
            color: #7f8c8d;
            font-size: 1.3em;
            margin-bottom: 10px;
            margin-top: 20px;
        }
        
        p {
            margin-bottom: 15px;
            text-align: justify;
        }
        
        ul, ol {
            margin-left: 30px;
            margin-bottom: 15px;
        }
        
        li {
            margin-bottom: 8px;
        }
        
        .toc {
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 5px;
            margin-bottom: 40px;
        }
        
        .toc ul {
            list-style: none;
            margin-left: 0;
        }
        
        .toc li {
            padding: 8px 0;
            border-bottom: 1px solid #dee2e6;
        }
        
        .toc li:last-child {
            border-bottom: none;
        }
        
        .toc a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        
        .toc a:hover {
            color: #764ba2;
        }
        
        .business-info {
            background-color: #e8f4f8;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .business-info p {
            margin-bottom: 10px;
        }
        
        .business-info strong {
            color: #2c3e50;
        }
        
        .footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
        }
        
        @media print {
            body {
                background-color: white;
            }
            
            .container {
                box-shadow: none;
            }
            
            .section {
                page-break-after: always;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Cover Page -->
        <div class="cover-page">
            <h1>{{ business_name }}</h1>
            <h2>Comprehensive Business Plan</h2>
            <div class="info">
                <p><strong>Industry:</strong> {{ industry }}</p>
                <p><strong>Location:</strong> {{ location }}</p>
                <p><strong>Date:</strong> {{ date }}</p>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="content">
            <!-- Table of Contents -->
            <div class="toc">
                <h2>Table of Contents</h2>
                <ul>
                    <li><a href="#executive-summary">1. Executive Summary</a></li>
                    <li><a href="#business-description">2. Business Description</a></li>
                    <li><a href="#market-analysis">3. Market Analysis</a></li>
                    <li><a href="#swot-analysis">4. SWOT Analysis</a></li>
                    <li><a href="#financial-projections">5. Financial Projections</a></li>
                    <li><a href="#innovation-strategy">6. Innovation & Implementation Strategy</a></li>
                </ul>
            </div>
            
            <!-- Executive Summary -->
            {% if executive_summary %}
            <div id="executive-summary" class="section">
                <h1>Executive Summary</h1>
                {{ executive_summary | safe }}
            </div>
            {% endif %}
            
            <!-- Business Description -->
            <div id="business-description" class="section">
                <h1>Business Description</h1>
                <div class="business-info">
                    <p><strong>Business Name:</strong> {{ business_name }}</p>
                    <p><strong>Industry:</strong> {{ industry }}</p>
                    <p><strong>Business Type:</strong> {{ business_type }}</p>
                    <p><strong>Location:</strong> {{ location }}</p>
                </div>
                <h3>Description</h3>
                <p>{{ description }}</p>
                <h3>Target Market</h3>
                <p>{{ target_market }}</p>
                <h3>Products/Services</h3>
                <p>{{ products_services }}</p>
            </div>
            
            <!-- Market Analysis -->
            {% if market_analysis %}
            <div id="market-analysis" class="section">
                <h1>Market Analysis</h1>
                {{ market_analysis | safe }}
            </div>
            {% endif %}
            
            <!-- SWOT Analysis -->
            {% if swot_analysis %}
            <div id="swot-analysis" class="section">
                <h1>SWOT Analysis</h1>
                {{ swot_analysis | safe }}
            </div>
            {% endif %}
            
            <!-- Financial Projections -->
            {% if financial_projections %}
            <div id="financial-projections" class="section">
                <h1>Financial Projections</h1>
                {{ financial_projections | safe }}
            </div>
            {% endif %}
            
            <!-- Innovation Strategy -->
            {% if innovation_strategy %}
            <div id="innovation-strategy" class="section">
                <h1>Innovation & Implementation Strategy</h1>
                {{ innovation_strategy | safe }}
            </div>
            {% endif %}
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Generated by Business Plan Generator - {{ date }}</p>
        </div>
    </div>
</body>
</html>
        """
        return Template(template_str)
    
    def generate(self, business_data: Dict[str, Any], sections: Dict[str, str], 
                 output_path: str) -> str:
        """Generate HTML business plan"""
        
        # Prepare template data
        template_data = {
            'business_name': business_data.get('business_name', 'Business Plan'),
            'industry': business_data.get('industry', 'N/A'),
            'business_type': business_data.get('business_type', 'N/A'),
            'location': business_data.get('location', 'N/A'),
            'description': business_data.get('description', 'No description provided.'),
            'target_market': business_data.get('target_market', 'N/A'),
            'products_services': business_data.get('products_services', 'N/A'),
            'date': datetime.now().strftime('%B %d, %Y'),
        }
        
        # Add sections (convert newlines to HTML)
        for key, value in sections.items():
            template_data[key] = self._format_content(value)
        
        # Render HTML
        html_content = self.template.render(**template_data)
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _format_content(self, content: str) -> str:
        """Format content for HTML display"""
        # Split into paragraphs
        paragraphs = content.split('\n\n')
        html_parts = []
        
        for para in paragraphs:
            if para.strip():
                # Convert single newlines to <br>
                para = para.replace('\n', '<br>')
                html_parts.append(f'<p>{para}</p>')
        
        return '\n'.join(html_parts)

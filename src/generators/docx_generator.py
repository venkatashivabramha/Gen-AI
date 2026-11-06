"""
DOCX Generator for Business Plans
Uses python-docx to create Word documents
"""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from typing import Dict, Any


class DOCXGenerator:
    """Generate Word document business plans"""
    
    def __init__(self):
        self.doc = None
    
    def generate(self, business_data: Dict[str, Any], sections: Dict[str, str], 
                 output_path: str) -> str:
        """Generate DOCX business plan"""
        
        self.doc = Document()
        
        # Set document properties
        self.doc.core_properties.title = f"{business_data.get('business_name', 'Business Plan')}"
        self.doc.core_properties.author = "Business Plan Generator"
        self.doc.core_properties.created = datetime.now()
        
        # Cover Page
        self._create_cover_page(business_data)
        self.doc.add_page_break()
        
        # Table of Contents
        self._add_heading("Table of Contents", 1)
        self._create_toc()
        self.doc.add_page_break()
        
        # Executive Summary
        if 'executive_summary' in sections:
            self._add_heading("Executive Summary", 1)
            self._add_content(sections['executive_summary'])
            self.doc.add_page_break()
        
        # Business Description
        self._add_heading("Business Description", 1)
        self._add_business_description(business_data)
        self.doc.add_page_break()
        
        # Market Analysis
        if 'market_analysis' in sections:
            self._add_heading("Market Analysis", 1)
            self._add_content(sections['market_analysis'])
            self.doc.add_page_break()
        
        # SWOT Analysis
        if 'swot_analysis' in sections:
            self._add_heading("SWOT Analysis", 1)
            self._add_content(sections['swot_analysis'])
            self.doc.add_page_break()
        
        # Financial Projections
        if 'financial_projections' in sections:
            self._add_heading("Financial Projections", 1)
            self._add_content(sections['financial_projections'])
            self.doc.add_page_break()
        
        # Innovation Strategy
        if 'innovation_strategy' in sections:
            self._add_heading("Innovation & Implementation Strategy", 1)
            self._add_content(sections['innovation_strategy'])
        
        # Save document
        self.doc.save(output_path)
        
        return output_path
    
    def _create_cover_page(self, business_data: Dict[str, Any]):
        """Create cover page"""
        # Title
        title = self.doc.add_paragraph()
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = title.add_run(business_data.get('business_name', 'Business Plan'))
        run.font.size = Pt(28)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        
        # Subtitle
        subtitle = self.doc.add_paragraph()
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = subtitle.add_run("Comprehensive Business Plan")
        run.font.size = Pt(18)
        
        # Add spacing
        self.doc.add_paragraph()
        self.doc.add_paragraph()
        
        # Business information
        info = self.doc.add_paragraph()
        info.alignment = WD_ALIGN_PARAGRAPH.CENTER
        info.add_run(f"Industry: {business_data.get('industry', 'N/A')}\n")
        info.add_run(f"Location: {business_data.get('location', 'N/A')}\n")
        info.add_run(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    
    def _create_toc(self):
        """Create table of contents"""
        toc_items = [
            "1. Executive Summary",
            "2. Business Description",
            "3. Market Analysis",
            "4. SWOT Analysis",
            "5. Financial Projections",
            "6. Innovation & Implementation Strategy"
        ]
        
        for item in toc_items:
            self.doc.add_paragraph(item, style='List Number')
    
    def _add_heading(self, text: str, level: int = 1):
        """Add a heading"""
        heading = self.doc.add_heading(text, level=level)
        heading.style.font.color.rgb = RGBColor(44, 62, 80)
    
    def _add_content(self, content: str):
        """Add content paragraphs"""
        paragraphs = content.split('\n\n')
        for para_text in paragraphs:
            if para_text.strip():
                para = self.doc.add_paragraph(para_text.strip())
                para.paragraph_format.space_after = Pt(12)
                para.paragraph_format.line_spacing = 1.15
    
    def _add_business_description(self, business_data: Dict[str, Any]):
        """Add business description section"""
        # Business name
        self.doc.add_paragraph(f"Business Name: {business_data.get('business_name', 'N/A')}", 
                               style='List Bullet')
        self.doc.add_paragraph(f"Industry: {business_data.get('industry', 'N/A')}", 
                               style='List Bullet')
        self.doc.add_paragraph(f"Business Type: {business_data.get('business_type', 'N/A')}", 
                               style='List Bullet')
        self.doc.add_paragraph(f"Location: {business_data.get('location', 'N/A')}", 
                               style='List Bullet')
        
        self.doc.add_paragraph()
        
        # Description
        self._add_heading("Description", 2)
        self.doc.add_paragraph(business_data.get('description', 'No description provided.'))
        
        # Target Market
        self._add_heading("Target Market", 2)
        self.doc.add_paragraph(business_data.get('target_market', 'N/A'))
        
        # Products/Services
        self._add_heading("Products/Services", 2)
        self.doc.add_paragraph(business_data.get('products_services', 'N/A'))

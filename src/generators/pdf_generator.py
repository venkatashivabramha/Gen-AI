"""
PDF Generator for Business Plans
Uses ReportLab to create professional PDF documents
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
from typing import Dict, Any
import os


class PDFGenerator:
    """Generate professional PDF business plans"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=14
        ))
    
    def generate(self, business_data: Dict[str, Any], sections: Dict[str, str], 
                 output_path: str) -> str:
        """Generate PDF business plan"""
        
        # Create document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build content
        story = []
        
        # Cover Page
        story.extend(self._create_cover_page(business_data))
        story.append(PageBreak())
        
        # Table of Contents
        story.extend(self._create_toc())
        story.append(PageBreak())
        
        # Executive Summary
        if 'executive_summary' in sections:
            story.extend(self._create_section(
                "Executive Summary",
                sections['executive_summary']
            ))
            story.append(PageBreak())
        
        # Business Description
        story.extend(self._create_section(
            "Business Description",
            self._format_business_description(business_data)
        ))
        story.append(PageBreak())
        
        # Market Analysis
        if 'market_analysis' in sections:
            story.extend(self._create_section(
                "Market Analysis",
                sections['market_analysis']
            ))
            story.append(PageBreak())
        
        # SWOT Analysis
        if 'swot_analysis' in sections:
            story.extend(self._create_section(
                "SWOT Analysis",
                sections['swot_analysis']
            ))
            story.append(PageBreak())
        
        # Financial Projections
        if 'financial_projections' in sections:
            story.extend(self._create_section(
                "Financial Projections",
                sections['financial_projections']
            ))
            story.append(PageBreak())
        
        # Innovation Strategy
        if 'innovation_strategy' in sections:
            story.extend(self._create_section(
                "Innovation & Implementation Strategy",
                sections['innovation_strategy']
            ))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _create_cover_page(self, business_data: Dict[str, Any]) -> list:
        """Create cover page elements"""
        elements = []
        
        # Add spacing
        elements.append(Spacer(1, 2*inch))
        
        # Business name
        title = Paragraph(
            business_data.get('business_name', 'Business Plan'),
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Subtitle
        subtitle = Paragraph(
            "Comprehensive Business Plan",
            self.styles['Heading2']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 0.5*inch))
        
        # Business info
        info = f"""
        <para alignment="center">
        <b>Industry:</b> {business_data.get('industry', 'N/A')}<br/>
        <b>Location:</b> {business_data.get('location', 'N/A')}<br/>
        <b>Date:</b> {datetime.now().strftime('%B %d, %Y')}
        </para>
        """
        elements.append(Paragraph(info, self.styles['Normal']))
        
        return elements
    
    def _create_toc(self) -> list:
        """Create table of contents"""
        elements = []
        
        toc_title = Paragraph("Table of Contents", self.styles['CustomHeading'])
        elements.append(toc_title)
        elements.append(Spacer(1, 0.2*inch))
        
        toc_items = [
            "1. Executive Summary",
            "2. Business Description",
            "3. Market Analysis",
            "4. SWOT Analysis",
            "5. Financial Projections",
            "6. Innovation & Implementation Strategy"
        ]
        
        for item in toc_items:
            elements.append(Paragraph(item, self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_section(self, title: str, content: str) -> list:
        """Create a section with title and content"""
        elements = []
        
        # Section title
        title_para = Paragraph(title, self.styles['CustomHeading'])
        elements.append(title_para)
        elements.append(Spacer(1, 0.2*inch))
        
        # Sanitize content - remove problematic XML/HTML tags from AI output
        content = self._sanitize_text(content)
        
        # Section content
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                # Clean and format paragraph
                para_text = para.replace('\n', '<br/>')
                elements.append(Paragraph(para_text, self.styles['CustomBody']))
                elements.append(Spacer(1, 0.15*inch))
        
        return elements
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize text by removing/escaping problematic XML tags from AI output"""
        import re
        
        # Remove XML-like tags that aren't valid ReportLab markup
        # Keep only: <b>, <i>, <u>, <br/>, and escape everything else
        text = re.sub(r'<para[^>]*>', '', text)
        text = re.sub(r'</para>', '', text)
        text = re.sub(r'<Segment[^>]*>', '', text)
        text = re.sub(r'</Segment>', '', text)
        
        # Escape special XML characters in content
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;').replace('>', '&gt;')
        
        # But restore the valid tags we want to keep
        text = text.replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
        text = text.replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>')
        text = text.replace('&lt;u&gt;', '<u>').replace('&lt;/u&gt;', '</u>')
        text = text.replace('&lt;br/&gt;', '<br/>').replace('&lt;br&gt;', '<br/>')
        
        # Remove any remaining malformed tags
        text = re.sub(r'[|]+[-]+[|]+', '', text)  # Remove table-like separators
        
        return text
        
        # Section content
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                # Clean and format paragraph
                para_text = para.replace('\n', '<br/>')
                elements.append(Paragraph(para_text, self.styles['CustomBody']))
                elements.append(Spacer(1, 0.15*inch))
        
        return elements
    
    def _format_business_description(self, business_data: Dict[str, Any]) -> str:
        """Format business description from data"""
        description = f"""
        <b>Business Name:</b> {business_data.get('business_name', 'N/A')}<br/>
        <b>Industry:</b> {business_data.get('industry', 'N/A')}<br/>
        <b>Business Type:</b> {business_data.get('business_type', 'N/A')}<br/>
        <b>Location:</b> {business_data.get('location', 'N/A')}<br/><br/>
        
        <b>Description:</b><br/>
        {business_data.get('description', 'No description provided.')}
        <br/><br/>
        
        <b>Target Market:</b><br/>
        {business_data.get('target_market', 'N/A')}
        <br/><br/>
        
        <b>Products/Services:</b><br/>
        {business_data.get('products_services', 'N/A')}
        """
        
        return description

"""
Main Business Plan Generator
Orchestrates AI, MCP, and document generation
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import re
from datetime import datetime

from ai.llm_manager import LLMManager
from mcp.mcp_client import MCPClient, MCPBusinessTools
from generators.pdf_generator import PDFGenerator
from generators.html_generator import HTMLGenerator
from generators.docx_generator import DOCXGenerator
from config.config import OUTPUT_DIR, BUSINESS_TYPES


class BusinessPlanGenerator:
    """Main orchestrator for business plan generation"""
    
    def __init__(self, llm_provider: str = "openai"):
        self.llm_manager = LLMManager(llm_provider)
        self.mcp_client = MCPClient()
        self.mcp_tools = MCPBusinessTools()
        
        self.pdf_generator = PDFGenerator()
        self.html_generator = HTMLGenerator()
        self.docx_generator = DOCXGenerator()
        
        # Initialize RAG Engine for 3-5x faster generation!
        try:
            from rag.rag_engine import get_rag_engine
            self.rag_engine = get_rag_engine()
            self.use_rag = True
            print("🚀 RAG Engine activated - Generation will be 3-5x faster!")
        except ImportError:
            self.rag_engine = None
            self.use_rag = False
            print("ℹ️  Using standard generation")
    
    def generate_from_form(self, form_data: Dict[str, Any], 
                          output_formats: List[str] = ['pdf']) -> Dict[str, str]:
        """Generate business plan from form data"""
        
        print("Generating business plan from form data...")
        
        # Enhance with MCP data if available
        if self.mcp_client.is_available():
            form_data = self.mcp_client.enhance_business_plan(form_data)
            print("Enhanced with MCP data")
        
        # Generate sections using AI
        sections = self._generate_all_sections(form_data)
        
        # Generate documents
        output_files = self._generate_documents(form_data, sections, output_formats)
        
        return {
            'status': 'success',
            'files': output_files,
            'sections': sections
        }
    
    def generate_from_template(self, business_type: str, 
                              basic_info: Dict[str, Any],
                              output_formats: List[str] = ['pdf']) -> Dict[str, str]:
        """Generate business plan from template"""
        
        print(f"Generating business plan from template: {business_type}")
        
        # Load template data
        template_data = self._get_template_data(business_type)
        
        # Merge with basic info
        form_data = {**template_data, **basic_info}
        
        # Generate plan
        return self.generate_from_form(form_data, output_formats)
    
    def generate_from_natural_language(self, description: str,
                                      output_formats: List[str] = ['pdf']) -> Dict[str, str]:
        """Generate business plan from natural language description"""
        
        print("Generating business plan from natural language...")
        
        # Extract structured data from description
        extracted_info = self.llm_manager.generate_from_natural_language(description)
        
        # Parse the extracted info (it comes as text, need to structure it)
        form_data = self._parse_extracted_info(extracted_info, description)
        
        # Generate plan
        return self.generate_from_form(form_data, output_formats)
    
    def _generate_all_sections(self, business_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate all business plan sections using AI"""
        
        sections = {}
        
        print("Generating Market Analysis...")
        if self.use_rag and self.rag_engine:
            # Use RAG for 3-5x faster generation!
            sections['market_analysis'] = self.rag_engine.generate_market_analysis_with_rag(
                business_data,
                lambda prompt: self.llm_manager.provider.generate(prompt)
            )
        else:
            sections['market_analysis'] = self.llm_manager.generate_market_analysis(business_data)
        
        print("Generating SWOT Analysis...")
        if self.use_rag and self.rag_engine:
            sections['swot_analysis'] = self.rag_engine.generate_swot_with_rag(
                business_data,
                lambda prompt: self.llm_manager.provider.generate(prompt)
            )
        else:
            sections['swot_analysis'] = self.llm_manager.generate_swot_analysis(business_data)
        
        print("Generating Financial Projections...")
        if self.use_rag and self.rag_engine:
            sections['financial_projections'] = self.rag_engine.generate_financial_with_rag(
                business_data,
                lambda prompt: self.llm_manager.provider.generate(prompt)
            )
        else:
            sections['financial_projections'] = self.llm_manager.generate_financial_projections(business_data)
        
        print("Generating Innovation Strategy...")
        sections['innovation_strategy'] = self.llm_manager.generate_innovation_strategy(business_data)
        
        print("Generating Executive Summary...")
        sections['executive_summary'] = self.llm_manager.generate_executive_summary(
            business_data, sections
        )
        
        return sections
    
    def _generate_documents(self, business_data: Dict[str, Any], 
                           sections: Dict[str, str],
                           output_formats: List[str]) -> Dict[str, str]:
        """Generate documents in specified formats"""
        
        output_files = {}
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        business_name = business_data.get('business_name', 'business_plan')
        
        # Sanitize filename - remove invalid characters
        import re
        business_name = re.sub(r'[<>:"/\\|?*\n\r\t]', '_', business_name)
        business_name = business_name.replace(' ', '_').lower()
        business_name = re.sub(r'_+', '_', business_name)  # Remove multiple underscores
        business_name = business_name.strip('_')  # Remove leading/trailing underscores
        
        base_filename = f"{business_name}_{timestamp}"
        
        for fmt in output_formats:
            output_path = OUTPUT_DIR / f"{base_filename}.{fmt}"
            
            # Ensure output directory exists
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            
            try:
                if fmt == 'pdf':
                    print(f"Generating PDF: {output_path}")
                    self.pdf_generator.generate(business_data, sections, str(output_path))
                    output_files['pdf'] = str(output_path)
                
                elif fmt == 'html':
                    print(f"Generating HTML: {output_path}")
                    self.html_generator.generate(business_data, sections, str(output_path))
                    output_files['html'] = str(output_path)
                
                elif fmt == 'docx':
                    print(f"Generating DOCX: {output_path}")
                    self.docx_generator.generate(business_data, sections, str(output_path))
                    output_files['docx'] = str(output_path)
            
            except Exception as e:
                print(f"Error generating {fmt}: {e}")
                import traceback
                traceback.print_exc()
                output_files[fmt] = f"Error: {str(e)}"
        
        return output_files
    
    def _get_template_data(self, business_type: str) -> Dict[str, Any]:
        """Get template data for a specific business type"""
        
        templates = {
            "Technology Startup": {
                "business_type": "Technology Startup",
                "industry": "Technology",
                "description": "An innovative technology startup focused on solving modern problems with cutting-edge solutions.",
                "target_market": "Tech-savvy consumers and businesses looking for innovative solutions.",
                "products_services": "Software products, SaaS solutions, mobile applications.",
                "revenue_model": "Subscription-based, freemium model, and enterprise licensing.",
                "innovation_focus": "AI integration, cloud computing, mobile-first approach"
            },
            "E-commerce": {
                "business_type": "E-commerce",
                "industry": "Retail/E-commerce",
                "description": "Online retail platform offering curated products to a targeted audience.",
                "target_market": "Online shoppers seeking quality products and convenient shopping experience.",
                "products_services": "Online product catalog, shopping cart, payment processing, delivery services.",
                "revenue_model": "Product sales, marketplace fees, premium memberships.",
                "innovation_focus": "Personalization, AI recommendations, omnichannel experience"
            },
            "Restaurant/Food Service": {
                "business_type": "Restaurant/Food Service",
                "industry": "Food & Hospitality",
                "description": "Modern dining establishment offering unique culinary experiences.",
                "target_market": "Food enthusiasts, local community, tourists.",
                "products_services": "Dine-in services, takeout, catering, specialty dishes.",
                "revenue_model": "Food sales, beverage sales, catering services.",
                "innovation_focus": "Farm-to-table, sustainable sourcing, unique dining experience"
            },
            "Consulting Services": {
                "business_type": "Consulting Services",
                "industry": "Professional Services",
                "description": "Expert consulting firm providing specialized knowledge and solutions.",
                "target_market": "Businesses seeking expert guidance and strategic solutions.",
                "products_services": "Consulting sessions, strategic planning, implementation support.",
                "revenue_model": "Hourly rates, project-based fees, retainer agreements.",
                "innovation_focus": "Data-driven insights, digital transformation, industry expertise"
            }
        }
        
        return templates.get(business_type, {
            "business_type": business_type,
            "industry": "General",
            "description": "A business focused on delivering value to its target market.",
            "target_market": "Target customers in the specified market.",
            "products_services": "Products and services tailored to customer needs.",
            "revenue_model": "Multiple revenue streams.",
            "innovation_focus": "Continuous improvement and innovation"
        })
    
    def _parse_extracted_info(self, extracted_text: str, original_description: str) -> Dict[str, Any]:
        """Parse extracted information from AI response"""
        
        # This is a simple parser - in production, you'd want more robust parsing
        # For now, we'll create a basic structure
        
        return {
            "business_name": "Innovative Business",  # Could extract from text
            "industry": "General",
            "business_type": "Other",
            "location": "United States",
            "description": original_description,
            "target_market": "Market to be determined based on analysis",
            "products_services": "Products and services as described",
            "revenue_model": "To be determined",
            "innovation_focus": "Innovation opportunities to be explored",
            "ai_extracted_info": extracted_text
        }
    
    def save_project(self, business_data: Dict[str, Any], sections: Dict[str, str], 
                    project_name: str) -> str:
        """Save business plan project for later editing"""
        
        project_data = {
            'business_data': business_data,
            'sections': sections,
            'created_at': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        project_path = OUTPUT_DIR / f"{project_name}_project.json"
        
        with open(project_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2)
        
        return str(project_path)
    
    def load_project(self, project_path: str) -> Dict[str, Any]:
        """Load a saved business plan project"""
        
        with open(project_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        
        return project_data

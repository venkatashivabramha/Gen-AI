"""
Template Manager - Loads and manages business plan templates
"""
import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path


class TemplateManager:
    """Manages pre-written business plan templates for RAG"""
    
    def __init__(self, templates_dir: str = "data/templates"):
        self.templates_dir = Path(templates_dir)
        self.templates: Dict[str, Any] = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all template files from the templates directory"""
        if not self.templates_dir.exists():
            print(f"Warning: Templates directory not found: {self.templates_dir}")
            return
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    template_name = template_file.stem
                    self.templates[template_name] = template_data
                    print(f"✓ Loaded template: {template_name}")
            except Exception as e:
                print(f"✗ Error loading {template_file}: {e}")
    
    def get_market_analysis_template(self, industry: str) -> Optional[str]:
        """Get market analysis template for specific industry"""
        template = self.templates.get('market_analysis_template', {})
        industries = template.get('industries', {})
        
        # Try exact match first
        if industry.lower() in industries:
            return industries[industry.lower()]['template']
        
        # Try fuzzy matching
        industry_lower = industry.lower()
        for key in industries.keys():
            if key in industry_lower or industry_lower in key:
                return industries[key]['template']
        
        # Default to technology if no match
        return industries.get('technology', {}).get('template')
    
    def get_financial_template(self, revenue_model: str) -> Optional[str]:
        """Get financial projections template for specific revenue model"""
        template = self.templates.get('financial_template', {})
        models = template.get('revenue_models', {})
        
        # Map common terms to template keys
        model_mapping = {
            'commission': 'commission_based',
            'marketplace': 'commission_based',
            'subscription': 'subscription_saas',
            'saas': 'subscription_saas',
            'software': 'subscription_saas'
        }
        
        model_key = revenue_model.lower()
        for key, value in model_mapping.items():
            if key in model_key:
                model_key = value
                break
        
        if model_key in models:
            return models[model_key]['template']
        
        # Default to commission_based
        return models.get('commission_based', {}).get('template')
    
    def get_swot_template(self, business_type: str) -> Optional[Dict[str, List[str]]]:
        """Get SWOT analysis template for specific business type"""
        template = self.templates.get('swot_template', {})
        types = template.get('business_types', {})
        
        # Map business types
        type_mapping = {
            'marketplace': 'marketplace_platform',
            'platform': 'marketplace_platform',
            'saas': 'saas_b2b',
            'b2b': 'saas_b2b',
            'software': 'saas_b2b',
            'ecommerce': 'ecommerce_retail',
            'retail': 'ecommerce_retail',
            'store': 'ecommerce_retail'
        }
        
        type_key = business_type.lower()
        for key, value in type_mapping.items():
            if key in type_key:
                type_key = value
                break
        
        if type_key in types:
            return types[type_key]
        
        # Default to marketplace_platform
        return types.get('marketplace_platform', {})
    
    def fill_template(self, template: str, variables: Dict[str, Any]) -> str:
        """Fill template with variables"""
        try:
            return template.format(**variables)
        except KeyError as e:
            # If a variable is missing, return template with placeholders
            print(f"Warning: Missing variable {e}, using placeholder")
            return template
    
    def get_default_values(self, section: str, category: str) -> Dict[str, Any]:
        """Get default values for a template section"""
        if section == 'market_analysis':
            template = self.templates.get('market_analysis_template', {})
            industries = template.get('industries', {})
            return industries.get(category, {}).get('default_values', {})
        elif section == 'financial':
            template = self.templates.get('financial_template', {})
            models = template.get('revenue_models', {})
            return models.get(category, {}).get('default_values', {})
        return {}
    
    def get_available_templates(self) -> Dict[str, List[str]]:
        """Get list of available templates"""
        available = {}
        
        if 'market_analysis_template' in self.templates:
            available['market_analysis'] = list(
                self.templates['market_analysis_template'].get('industries', {}).keys()
            )
        
        if 'financial_template' in self.templates:
            available['financial'] = list(
                self.templates['financial_template'].get('revenue_models', {}).keys()
            )
        
        if 'swot_template' in self.templates:
            available['swot'] = list(
                self.templates['swot_template'].get('business_types', {}).keys()
            )
        
        return available
    
    def extract_industry_keywords(self, description: str) -> List[str]:
        """Extract industry-related keywords from business description"""
        keywords = []
        
        # Common industry indicators
        industry_terms = {
            'technology': ['tech', 'software', 'app', 'platform', 'digital', 'ai', 'ml', 'saas'],
            'marketplace': ['marketplace', 'platform', 'connect', 'freelance', 'gig', 'booking'],
            'saas': ['saas', 'subscription', 'cloud', 'software', 'service'],
            'ecommerce': ['ecommerce', 'store', 'retail', 'shop', 'sell', 'products'],
            'healthcare': ['health', 'medical', 'patient', 'doctor', 'clinic', 'wellness'],
            'fintech': ['finance', 'payment', 'banking', 'money', 'crypto', 'wallet'],
            'education': ['education', 'learning', 'course', 'training', 'school', 'teach']
        }
        
        description_lower = description.lower()
        for industry, terms in industry_terms.items():
            for term in terms:
                if term in description_lower:
                    if industry not in keywords:
                        keywords.append(industry)
                    break
        
        return keywords if keywords else ['technology']  # Default to technology


# Singleton instance
_template_manager = None

def get_template_manager() -> TemplateManager:
    """Get or create TemplateManager singleton"""
    global _template_manager
    if _template_manager is None:
        _template_manager = TemplateManager()
    return _template_manager

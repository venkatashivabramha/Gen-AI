"""
LLM Manager for AI-powered content generation
Supports OpenAI, Anthropic, OpenRouter, Groq, and other providers
"""
import os
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

from config.config import OPENAI_API_KEY, ANTHROPIC_API_KEY, DEFAULT_LLM_PROVIDER, DEFAULT_MODEL


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        if not OpenAI:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=kwargs.get("model", self.model),
                messages=[
                    {"role": "system", "content": "You are an expert business consultant helping to create comprehensive business plans."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating content: {str(e)}"


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter API provider (FREE options available)"""
    
    def __init__(self, api_key: str, model: str = "meta-llama/llama-3.2-3b-instruct:free"):
        if not OpenAI:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        # OpenRouter uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using OpenRouter API (many free models!)"""
        try:
            response = self.client.chat.completions.create(
                model=kwargs.get("model", self.model),
                messages=[
                    {"role": "system", "content": "You are an expert business consultant helping to create comprehensive business plans."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating content: {str(e)}"


class GroqProvider(BaseLLMProvider):
    """Groq API provider (FREE and FAST!)"""
    
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        if not OpenAI:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        # Groq uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using Groq API (FREE!)"""
        try:
            response = self.client.chat.completions.create(
                model=kwargs.get("model", self.model),
                messages=[
                    {"role": "system", "content": "You are an expert business consultant helping to create comprehensive business plans."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating content: {str(e)}"


class HuggingFaceProvider(BaseLLMProvider):
    """HuggingFace Inference API provider (FREE tier available)"""
    
    def __init__(self, api_key: str, model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"):
        if not OpenAI:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        # HuggingFace can use OpenAI-compatible interface
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api-inference.huggingface.co/v1"
        )
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using HuggingFace API"""
        try:
            response = self.client.chat.completions.create(
                model=kwargs.get("model", self.model),
                messages=[
                    {"role": "system", "content": "You are an expert business consultant helping to create comprehensive business plans."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating content: {str(e)}"


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        if not Anthropic:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
        self.client = Anthropic(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using Anthropic API"""
        try:
            # Use the correct API format for anthropic 2.x
            response = self.client.messages.create(
                model=kwargs.get("model", self.model),
                max_tokens=kwargs.get("max_tokens", 2000),
                system="You are an expert business consultant helping to create comprehensive business plans.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
                # Note: temperature is optional, don't pass if not needed
            )
            return response.content[0].text
        except Exception as e:
            return f"Error generating content: {str(e)}"


class LLMManager:
    """Main LLM Manager to handle multiple providers"""
    
    def __init__(self, provider: str = DEFAULT_LLM_PROVIDER):
        self.provider_name = provider
        self.provider = self._initialize_provider(provider)
    
    def _initialize_provider(self, provider: str) -> Optional[BaseLLMProvider]:
        """Initialize the specified LLM provider"""
        
        if provider == "openai":
            if not OPENAI_API_KEY:
                raise ValueError("OpenAI API key not found in environment variables")
            return OpenAIProvider(OPENAI_API_KEY, DEFAULT_MODEL)
        
        elif provider == "anthropic":
            if not ANTHROPIC_API_KEY:
                raise ValueError("Anthropic API key not found in environment variables")
            return AnthropicProvider(ANTHROPIC_API_KEY, DEFAULT_MODEL)
        
        elif provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OpenRouter API key not found. Get free key at: https://openrouter.ai/keys")
            model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free")
            return OpenRouterProvider(api_key, model)
        
        elif provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("Groq API key not found. Get free key at: https://console.groq.com/keys")
            model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
            return GroqProvider(api_key, model)
        
        elif provider == "huggingface":
            api_key = os.getenv("HUGGINGFACE_API_KEY")
            if not api_key:
                raise ValueError("HuggingFace API key not found. Get free key at: https://huggingface.co/settings/tokens")
            model = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1")
            return HuggingFaceProvider(api_key, model)
        
        else:
            raise ValueError(f"Unsupported provider: {provider}. Options: openai, anthropic, openrouter, groq, huggingface")
    
    def generate_market_analysis(self, business_data: Dict[str, Any]) -> str:
        """Generate market analysis section"""
        prompt = f"""
        Create a comprehensive market analysis for the following business:
        
        Business Name: {business_data.get('business_name', 'N/A')}
        Industry: {business_data.get('industry', 'N/A')}
        Target Market: {business_data.get('target_market', 'N/A')}
        Location: {business_data.get('location', 'N/A')}
        
        Additional Context: {business_data.get('description', 'N/A')}
        
        Please provide:
        1. Industry Overview and Trends
        2. Target Market Demographics and Psychographics
        3. Market Size and Growth Potential
        4. Competitive Landscape
        5. Market Entry Strategy
        6. Key Market Insights
        
        Format the response in clear sections with bullet points where appropriate.
        """
        return self.provider.generate(prompt)
    
    def generate_swot_analysis(self, business_data: Dict[str, Any]) -> str:
        """Generate SWOT analysis"""
        prompt = f"""
        Create a detailed SWOT analysis for the following business:
        
        Business Name: {business_data.get('business_name', 'N/A')}
        Industry: {business_data.get('industry', 'N/A')}
        Business Model: {business_data.get('business_model', 'N/A')}
        
        Additional Context: {business_data.get('description', 'N/A')}
        
        Provide a comprehensive SWOT analysis with:
        - Strengths (internal positive factors)
        - Weaknesses (internal negative factors)
        - Opportunities (external positive factors)
        - Threats (external negative factors)
        
        Include at least 5 points for each category.
        """
        return self.provider.generate(prompt)
    
    def generate_financial_projections(self, business_data: Dict[str, Any]) -> str:
        """Generate financial projections"""
        prompt = f"""
        Create financial projections for the following business:
        
        Business Name: {business_data.get('business_name', 'N/A')}
        Industry: {business_data.get('industry', 'N/A')}
        Initial Investment: {business_data.get('initial_investment', 'N/A')}
        Revenue Model: {business_data.get('revenue_model', 'N/A')}
        
        Additional Context: {business_data.get('description', 'N/A')}
        
        Please provide:
        1. Revenue Projections (3-year outlook)
        2. Cost Structure and Operating Expenses
        3. Break-even Analysis
        4. Profit Margins
        5. Cash Flow Considerations
        6. Key Financial Assumptions
        
        Present realistic numbers based on industry standards.
        """
        return self.provider.generate(prompt)
    
    def generate_innovation_strategy(self, business_data: Dict[str, Any]) -> str:
        """Generate innovation and implementation strategy"""
        prompt = f"""
        Create an innovation strategy and implementation plan for:
        
        Business Name: {business_data.get('business_name', 'N/A')}
        Industry: {business_data.get('industry', 'N/A')}
        Innovation Focus: {business_data.get('innovation_focus', 'N/A')}
        
        Additional Context: {business_data.get('description', 'N/A')}
        
        Please provide:
        1. Innovative Business Ideas and Differentiators
        2. Technology Integration Opportunities
        3. Product/Service Innovation Roadmap
        4. Implementation Timeline (Phases)
        5. Resource Requirements
        6. Success Metrics and KPIs
        
        Focus on practical, actionable innovations.
        """
        return self.provider.generate(prompt)
    
    def generate_from_natural_language(self, description: str) -> Dict[str, Any]:
        """Extract business plan components from natural language description"""
        prompt = f"""
        Based on the following business description, extract key information needed for a business plan:
        
        Description: {description}
        
        Please provide structured information about:
        1. Business Name (suggest one if not mentioned)
        2. Industry/Sector
        3. Target Market
        4. Business Model
        5. Key Products/Services
        6. Unique Value Proposition
        7. Estimated Initial Investment Range
        8. Revenue Streams
        
        Format your response as a structured JSON-like format.
        """
        return self.provider.generate(prompt, temperature=0.5)
    
    def generate_executive_summary(self, business_data: Dict[str, Any], 
                                   all_sections: Dict[str, str]) -> str:
        """Generate executive summary based on all other sections"""
        prompt = f"""
        Create a compelling executive summary for a business plan with the following information:
        
        Business Name: {business_data.get('business_name', 'N/A')}
        Industry: {business_data.get('industry', 'N/A')}
        
        Based on the following detailed sections:
        {all_sections.get('market_analysis', '')[:500]}...
        {all_sections.get('swot_analysis', '')[:500]}...
        {all_sections.get('financial_projections', '')[:500]}...
        
        Create a concise executive summary (2-3 paragraphs) that:
        1. Captures the business opportunity
        2. Highlights key competitive advantages
        3. Summarizes financial potential
        4. Presents a compelling call to action
        """
        return self.provider.generate(prompt, max_tokens=800)

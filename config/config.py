"""
Configuration management for Business Plan Generator
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = DATA_DIR / "business_templates"

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# AI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4-turbo-preview")

# MCP Configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8080")
MCP_ENABLED = os.getenv("MCP_ENABLED", "true").lower() == "true"

# Application Settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# Business plan sections
BUSINESS_PLAN_SECTIONS = [
    "Executive Summary",
    "Business Description",
    "Market Analysis",
    "SWOT Analysis",
    "Marketing Strategy",
    "Financial Projections",
    "Innovation Strategy",
    "Implementation Plan",
    "Risk Analysis",
    "Appendix"
]

# Template business types
BUSINESS_TYPES = [
    "Technology Startup",
    "E-commerce",
    "Restaurant/Food Service",
    "Retail Store",
    "Consulting Services",
    "Manufacturing",
    "Healthcare Services",
    "Real Estate",
    "Education/Training",
    "Other"
]

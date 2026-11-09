"""
Business Plan Generator Page
Main generation interface with form, AI, and template modes
"""
import streamlit as st
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from business_plan_generator import BusinessPlanGenerator

st.set_page_config(page_title="Generate Business Plan", page_icon="??", layout="wide")

st.title("?? Generate Your Business Plan")

# Check authentication (optional for demo)
# if not st.session_state.get('authenticated', False):
#     st.warning("Please login to generate business plans")
#     st.stop()

# Sidebar - Settings
with st.sidebar:
    st.header("?? Settings")
    
    # LLM Provider selection
    llm_provider = "groq"  # Only Groq API enabled
    st.info("?? Using Groq API (FREE & Fast!)")
    
    # Real market data toggle
    use_real_data = st.checkbox(
        "?? Use Real Market Data",
        value=True,
        help="Fetch live data from Yahoo Finance"
    )
    
    # Output formats
    st.subheader("Output Formats")
    format_pdf = st.checkbox("PDF", value=True)
    format_docx = st.checkbox("DOCX", value=False)
    format_html = st.checkbox("HTML", value=False)
    format_md = st.checkbox("Markdown", value=False)

# Main content - Mode selection
mode = st.radio(
    "Choose Input Mode:",
    ["?? Form Input", "?? AI Description", "?? Template"],
    horizontal=True
)

st.markdown("---")

# Initialize generator
@st.cache_resource
def get_generator(provider, use_data):
    return BusinessPlanGenerator(provider, use_real_data=use_data)

# Form Input Mode
if mode == "?? Form Input":
    st.header("Fill in Your Business Details")
    
    with st.form("business_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            business_name = st.text_input("Business Name *", placeholder="e.g., TechVision AI")
            industry = st.text_input("Industry *", placeholder="e.g., Technology - AI")
            business_type = st.text_input("Business Type", placeholder="e.g., SaaS Startup")
            location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
            
        with col2:
            revenue_model = st.text_input("Revenue Model", placeholder="e.g., Subscription-based")
            initial_investment = st.text_input("Initial Investment", placeholder="e.g., $150,000")
            innovation_focus = st.text_area("Innovation Focus", placeholder="Key innovations...")
        
        target_market = st.text_area(
            "Target Market *",
            placeholder="Describe your target customers, market size, demographics..."
        )
        
        products_services = st.text_area(
            "Products/Services *",
            placeholder="List your main products or services..."
        )
        
        description = st.text_area(
            "Business Description *",
            placeholder="Provide a comprehensive description of your business...",
            height=150
        )
        
        submitted = st.form_submit_button("?? Generate Business Plan", use_container_width=True)
        
        if submitted:
            if not business_name or not industry or not target_market or not description:
                st.error("Please fill in all required fields (*)")
            else:
                # Collect formats
                formats = []
                if format_pdf: formats.append("pdf")
                if format_docx: formats.append("docx")
                if format_html: formats.append("html")
                if format_md: formats.append("md")
                
                if not formats:
                    st.error("Please select at least one output format")
                else:
                    with st.spinner("?? Generating your business plan... This may take 2-5 minutes..."):
                        try:
                            generator = get_generator(llm_provider, use_real_data)
                            
                            data = {
                                'business_name': business_name,
                                'industry': industry,
                                'business_type': business_type,
                                'location': location,
                                'target_market': target_market,
                                'products_services': products_services,
                                'revenue_model': revenue_model,
                                'initial_investment': initial_investment,
                                'innovation_focus': innovation_focus,
                                'description': description
                            }
                            
                            result = generator.generate_from_form(data, formats)
                            
                            if result['status'] == 'success':
                                st.success("? Business plan generated successfully!")
                                
                                # Display download buttons
                                st.subheader("?? Download Your Business Plan")
                                
                                for fmt, filepath in result['files'].items():
                                    if os.path.exists(filepath):
                                        with open(filepath, 'rb') as f:
                                            file_data = f.read()
                                            st.download_button(
                                                label=f"Download {fmt.upper()}",
                                                data=file_data,
                                                file_name=os.path.basename(filepath),
                                                mime=f"application/{fmt}",
                                                key=f"download_{fmt}"
                                            )
                            else:
                                st.error("? Generation failed. Please check your API keys and try again.")
                                
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                            st.exception(e)

# AI Description Mode
elif mode == "?? AI Description":
    st.header("Describe Your Business Idea")
    st.markdown("Simply describe your business in natural language, and AI will create a comprehensive plan.")
    
    description = st.text_area(
        "Business Description",
        placeholder="""Example: I want to start a technology startup that uses AI to help small businesses automate their customer service. We'll target small to medium businesses in the retail sector with 10-500 employees. Our platform will integrate with existing CRM systems and provide 24/7 automated support with human escalation when needed.""",
        height=200
    )
    
    if st.button("?? Generate with AI", use_container_width=True):
        if not description or description.startswith("Example:"):
            st.error("Please provide your business description")
        else:
            # Collect formats
            formats = []
            if format_pdf: formats.append("pdf")
            if format_docx: formats.append("docx")
            if format_html: formats.append("html")
            if format_md: formats.append("md")
            
            if not formats:
                st.error("Please select at least one output format in the sidebar")
            else:
                with st.spinner("?? AI is creating your business plan... This may take 2-5 minutes..."):
                    try:
                        generator = get_generator(llm_provider, use_real_data)
                        result = generator.generate_from_natural_language(description, formats)
                        
                        if result['status'] == 'success':
                            st.success("? Business plan generated successfully!")
                            
                            st.subheader("?? Download Your Business Plan")
                            
                            for fmt, filepath in result['files'].items():
                                if os.path.exists(filepath):
                                    with open(filepath, 'rb') as f:
                                        file_data = f.read()
                                        st.download_button(
                                            label=f"Download {fmt.upper()}",
                                            data=file_data,
                                            file_name=os.path.basename(filepath),
                                            mime=f"application/{fmt}",
                                            key=f"download_ai_{fmt}"
                                        )
                        else:
                            st.error("? Generation failed. Please check your API keys.")
                            
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

# Template Mode  
elif mode == "?? Template":
    st.header("Choose a Business Template")
    
    from config.config import BUSINESS_TYPES
    
    business_type = st.selectbox("Select Business Type", BUSINESS_TYPES)
    
    st.markdown("### Basic Information")
    
    col1, col2 = st.columns(2)
    with col1:
        business_name = st.text_input("Business Name *")
        location = st.text_input("Location")
    with col2:
        specific_focus = st.text_input("Specific Focus", placeholder="e.g., Mobile apps, Healthcare AI")
    
    if st.button("?? Generate from Template", use_container_width=True):
        if not business_name:
            st.error("Please provide a business name")
        else:
            # Collect formats
            formats = []
            if format_pdf: formats.append("pdf")
            if format_docx: formats.append("docx")
            if format_html: formats.append("html")
            if format_md: formats.append("md")
            
            if not formats:
                st.error("Please select at least one output format in the sidebar")
            else:
                with st.spinner("?? Generating from template... This may take 2-5 minutes..."):
                    try:
                        generator = get_generator(llm_provider, use_real_data)
                        
                        basic_info = {
                            'business_name': business_name,
                            'location': location,
                            'specific_focus': specific_focus
                        }
                        
                        result = generator.generate_from_template(business_type, basic_info, formats)
                        
                        if result['status'] == 'success':
                            st.success("? Business plan generated successfully!")
                            
                            st.subheader("?? Download Your Business Plan")
                            
                            for fmt, filepath in result['files'].items():
                                if os.path.exists(filepath):
                                    with open(filepath, 'rb') as f:
                                        file_data = f.read()
                                        st.download_button(
                                            label=f"Download {fmt.upper()}",
                                            data=file_data,
                                            file_name=os.path.basename(filepath),
                                            mime=f"application/{fmt}",
                                            key=f"download_template_{fmt}"
                                        )
                        else:
                            st.error("? Generation failed. Please try again.")
                            
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

# Info section
with st.expander("?? Tips for Best Results"):
    st.markdown("""
    ### ?? Form Input Mode
    - Provide detailed information for each field
    - Be specific about your target market and demographics
    - Include concrete numbers where possible (market size, investment, etc.)
    
    ### ?? AI Description Mode
    - Write at least 3-4 sentences
    - Include: what you do, who your customers are, how you make money
    - Mention any unique innovations or competitive advantages
    
    ### ?? Template Mode
    - Quick start with industry-standard structures
    - Customize the template output with your specific details
    - Best for common business types
    
    ### ? Performance Tips
    - First generation may take 3-5 minutes
    - Real market data adds 30-60 seconds but provides verified information
    - Groq provider is fastest (recommended)
    """)

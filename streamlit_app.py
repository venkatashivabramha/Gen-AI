"""
Business Plan Generator - Web Version
Streamlit-based web application for online deployment
"""
import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Page config
st.set_page_config(
    page_title="Business Plan Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #DC143C;
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #8B0000;
    }
</style>
""", unsafe_allow_html=True)

# Main page
def main():
    st.markdown('<div class="main-header">🚀 Business Plan Generator</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; font-size: 1.2rem; margin-bottom: 2rem;'>
        AI-Powered Professional Business Plans with Real Market Data
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🤖 AI-Powered</h3>
            <p>Advanced AI generates comprehensive business plans with industry-specific insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>📊 Real Market Data</h3>
            <p>Live data from Yahoo Finance - verified market sizes, growth rates, and competitors</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>📄 Multiple Formats</h3>
            <p>Export to PDF, DOCX, HTML, and Markdown formats</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Getting Started
    st.header("🎯 Getting Started")
    
    st.markdown("""
    ### Three Easy Ways to Generate Your Business Plan:
    
    1. **📝 Form Input** - Fill out a detailed form with all your business information
    2. **🤖 AI Description** - Simply describe your business idea in natural language
    3. **📋 Template** - Choose from pre-built industry templates
    
    **Get started by selecting a page from the sidebar! →**
    """)
    
    st.markdown("---")
    
    # Features detail
    st.header("✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Comprehensive Analysis
        - Market analysis and trends
        - SWOT analysis
        - Financial projections (3-year forecasts)
        - Competitive landscape
        - Risk assessment
        - Operations planning
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 Powerful Tools
        - Real-time market data from Yahoo Finance
        - RAG-enhanced AI generation
        - Multiple LLM providers (Groq, OpenAI, Anthropic)
        - User authentication system
        - Admin dashboard
        - Multi-format export
        """)
    
    st.markdown("---")
    
    # System Info
    with st.expander("ℹ️ System Information"):
        st.markdown("""
        **Version:** 2.0.0 (Web Version)
        
        **AI Providers:**
        - Groq (Free & Fast)
        - OpenRouter (Multiple models)
        - Anthropic (Claude)
        - OpenAI (GPT models)
        - HuggingFace (Open source)
        
        **Data Sources:**
        - Yahoo Finance (Real-time market data)
        - Industry templates (Pre-built business models)
        
        **Supported Formats:**
        - PDF (Professional documents)
        - DOCX (Editable Word files)
        - HTML (Web-ready pages)
        - Markdown (Developer-friendly)
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        Made with ❤️ using Streamlit | 
        <a href='https://github.com/venkatashivabramha/Gen-AI' target='_blank'>View on GitHub</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    
    main()

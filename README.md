# Business Plan Generator 🚀

An **AI-powered desktop application** for generating comprehensive, professional business plans with market analysis, financial projections, SWOT analysis, and innovation strategies.

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Key Features

### 🎯 Three Input Modes
- **📝 Form Input**: Detailed structured data entry
- **🤖 AI Description**: Natural language business description
- **📋 Template**: Pre-built templates for common business types

### 📊 Comprehensive Analysis
- **Market Analysis**: Industry overview, target market, competitive landscape
- **SWOT Analysis**: Strengths, Weaknesses, Opportunities, Threats
- **Financial Projections**: 3-year forecasts, break-even analysis, cost structure
- **Innovation Strategy**: Implementation roadmap, technology integration, KPIs

### 📄 Multiple Export Formats
- **PDF**: Professional, print-ready documents
- **HTML**: Web-ready, responsive pages
- **DOCX**: Editable Word documents

### 🤖 Advanced AI Integration
- **Multiple LLM Providers**: OpenAI, Anthropic, Groq, OpenRouter, HuggingFace
- **FREE API Options**: Use Groq, OpenRouter, or HuggingFace for FREE! 🎉
- **MCP Support**: Model Context Protocol for enhanced capabilities
- **Intelligent Content**: Context-aware, industry-specific insights

### 🎨 Modern Interface
- **Dark/Light Theme**: Comfortable viewing in any environment
- **Responsive Design**: Clean, intuitive user interface
- **Real-time Progress**: Track generation status

## 💡 FREE API Options Available! 

**No credit card required!** Choose from these FREE AI providers:

- **Groq** ⚡ (Recommended - fastest, free, easy)
- **OpenRouter** 🎨 (Multiple free models)
- **HuggingFace** ❤️ (Open source models)

**See [FREE_API_GUIDE.md](docs/FREE_API_GUIDE.md) for setup instructions!**

---

## 🚀 Quick Start

### Windows Users

1. **Run Setup**:
   ```powershell
   setup.bat
   ```

2. **Configure API Key** (Choose ONE):
   - **FREE Option**: Get a Groq key from https://console.groq.com/keys
   - **Paid Option**: OpenAI or Anthropic key
   - Edit `.env` file and add your key

3. **Launch Application**:
   ```powershell
   run_app.bat
   ```

### Manual Setup

1. **Install Dependencies**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```powershell
   Copy-Item .env.example .env
   # Edit .env and add your API key
   ```

3. **Run Application**:
   ```powershell
   python src/main.py
   ```

## 📚 Documentation

- **[Installation Guide](INSTALLATION.md)**: Detailed setup instructions
- **[Usage Guide](USAGE_GUIDE.md)**: How to use all features
- **[MCP Setup](MCP_SETUP.md)**: Model Context Protocol configuration

## 🎯 Use Cases

### For Entrepreneurs
- Create investor-ready business plans
- Explore business viability
- Structure business ideas

### For Students
- Learn business planning
- Complete assignments
- Study entrepreneurship

### For Consultants
- Generate client proposals
- Create multiple plan variants
- Save time on documentation

### For Accelerators/Incubators
- Help startups structure plans
- Standardize plan quality
- Scale mentorship

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.10+ |
| **GUI Framework** | CustomTkinter |
| **AI/LLM** | OpenAI API, Anthropic Claude |
| **PDF Generation** | ReportLab |
| **Word Generation** | python-docx |
| **HTML Templates** | Jinja2 |
| **MCP** | Model Context Protocol |
| **Data Processing** | pandas, numpy |

## 📁 Project Structure

```
business-plan-generator/
├── 📄 README.md                    # Project overview
├── 📄 INSTALLATION.md              # Setup guide
├── 📄 USAGE_GUIDE.md               # User manual
├── 📄 MCP_SETUP.md                 # MCP configuration
├── 📄 requirements.txt             # Dependencies
├── 📄 .env.example                 # Environment template
├── 🔧 setup.bat                    # Windows setup script
├── ▶️ run_app.bat                  # Launch script
├── 📁 src/
│   ├── 🐍 main.py                  # Application entry
│   ├── 🐍 business_plan_generator.py  # Core orchestrator
│   ├── 📁 gui/
│   │   └── 🐍 main_window.py       # Main UI
│   ├── 📁 ai/
│   │   └── 🐍 llm_manager.py       # LLM providers
│   ├── 📁 generators/
│   │   ├── 🐍 pdf_generator.py     # PDF creation
│   │   ├── 🐍 html_generator.py    # HTML creation
│   │   └── 🐍 docx_generator.py    # Word creation
│   └── 📁 mcp/
│       └── 🐍 mcp_client.py        # MCP integration
├── 📁 config/
│   └── 🐍 config.py                # Configuration
├── 📁 data/
│   └── 📁 business_templates/      # Templates
└── 📁 output/                      # Generated plans
```

## 🎓 How It Works

1. **Input**: Choose your preferred input method (form, AI, or template)
2. **AI Processing**: LLM analyzes your input and generates comprehensive content
3. **Enhancement**: Optional MCP integration adds real-time market data
4. **Generation**: Documents are created in your selected formats
5. **Output**: Professional business plans ready for use

## 🔑 API Keys

You need at least one AI API key:

### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create account and generate API key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Anthropic
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create account and generate API key
3. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

## 🎨 Screenshots

### Main Interface
Modern, clean interface with three input modes and intuitive navigation.

### Form Input Mode
Structured data entry with comprehensive fields for detailed business information.

### AI Description Mode
Natural language input for quick business plan generation.

### Template Mode
Pre-built templates for common business types with customization options.

## 🔧 Configuration

### Environment Variables (`.env`)

```env
# Required: At least one API key
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional: LLM Configuration
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-4-turbo-preview

# Optional: MCP Configuration
MCP_ENABLED=false
MCP_SERVER_URL=http://localhost:8080

# Optional: Application Settings
DEBUG_MODE=false
OUTPUT_DIRECTORY=./output
```

## 🎯 Roadmap

- [x] Multiple input modes
- [x] AI-powered content generation
- [x] PDF, HTML, DOCX export
- [x] MCP integration support
- [ ] Multi-language support
- [ ] Financial calculators
- [ ] Collaboration features
- [ ] Cloud storage integration
- [ ] Mobile companion app

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional business templates
- Enhanced financial models
- More document formats
- Improved AI prompts
- MCP server implementations

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## ⚠️ Disclaimer

This tool generates business plans based on AI and should be reviewed by business professionals. Financial projections are estimates and should be validated with actual market research and financial analysis.

## 🆘 Support

- **Installation Issues**: See [INSTALLATION.md](INSTALLATION.md)
- **Usage Questions**: See [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **MCP Setup**: See [MCP_SETUP.md](MCP_SETUP.md)

## 🌟 Features in Detail

### Market Analysis
- Industry overview and trends
- Target market demographics
- Market size and growth potential
- Competitive landscape analysis
- Market entry strategies

### SWOT Analysis
- Comprehensive strength identification
- Honest weakness assessment
- Opportunity exploration
- Threat evaluation
- Strategic recommendations

### Financial Projections
- 3-year revenue forecasts
- Cost structure breakdown
- Break-even analysis
- Profit margin calculations
- Cash flow considerations
- Key financial assumptions

### Innovation Strategy
- Unique value propositions
- Technology integration plans
- Implementation timeline
- Resource requirements
- Success metrics and KPIs
- Risk mitigation strategies

---

**Built with ❤️ for entrepreneurs, by entrepreneurs**

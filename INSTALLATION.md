# Installation Guide

## Prerequisites

- **Python 3.10 or higher**
- **pip** (Python package installer)
- **Virtual environment** (recommended)
- **API Keys** (at least one):
  - OpenAI API key, OR
  - Anthropic API key

## Step-by-Step Installation

### 1. Clone or Download the Project

```bash
cd D:\Project_Kiro
```

### 2. Create Virtual Environment (Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   # OR
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
   ```

### 5. Run the Application

```powershell
python src/main.py
```

## Getting API Keys

### OpenAI API Key
1. Visit: https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key to your `.env` file

### Anthropic API Key
1. Visit: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key to your `.env` file

## Troubleshooting

### Import Errors

If you see import errors, make sure you're in the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### API Key Issues

If you see "No API key found" errors:
1. Check that `.env` file exists in the project root
2. Verify the API key format is correct
3. Make sure there are no quotes around the key

### GUI Not Starting

If the GUI doesn't start:
1. Install customtkinter: `pip install customtkinter`
2. Check Python version: `python --version` (should be 3.10+)
3. Try reinstalling dependencies: `pip install -r requirements.txt --force-reinstall`

### MCP Server Connection Issues

If MCP features aren't working:
1. MCP is optional - the app will work without it
2. Check `MCP_ENABLED=true` in `.env`
3. Verify MCP server is running at the configured URL

## Optional: MCP Server Setup

MCP (Model Context Protocol) provides enhanced capabilities:

1. Install MCP server dependencies:
   ```powershell
   pip install mcp
   ```

2. Configure MCP in `.env`:
   ```
   MCP_ENABLED=true
   MCP_SERVER_URL=http://localhost:8080
   ```

3. Start your MCP server (see MCP documentation)

## Project Structure

```
business-plan-generator/
├── src/
│   ├── main.py                 # Entry point
│   ├── business_plan_generator.py  # Main orchestrator
│   ├── gui/                    # GUI components
│   │   └── main_window.py      # Main application window
│   ├── ai/                     # AI/LLM integration
│   │   └── llm_manager.py      # LLM provider management
│   ├── generators/             # Document generators
│   │   ├── pdf_generator.py    # PDF generation
│   │   ├── html_generator.py   # HTML generation
│   │   └── docx_generator.py   # Word generation
│   ├── mcp/                    # MCP integration
│   │   └── mcp_client.py       # MCP client
│   └── templates/              # Business templates
├── config/
│   └── config.py               # Configuration management
├── data/
│   └── business_templates/     # Template storage
├── output/                     # Generated business plans
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # Project overview
```

## Next Steps

1. **Configure API Keys**: Add your OpenAI or Anthropic API key
2. **Run the Application**: `python src/main.py`
3. **Create Your First Plan**: Choose an input mode and start generating!

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the README.md file
- Check that all dependencies are installed correctly

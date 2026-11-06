# Quick Start Guide ⚡

Get up and running with the Business Plan Generator in 5 minutes!

## 🎉 NEW: FREE API Options!

You don't need a paid API! **FREE options available**:
- ⚡ **Groq** (Recommended - fastest & free)  
- 🎨 **OpenRouter** (Multiple free models)
- ❤️ **HuggingFace** (Open source)

**See [docs/FREE_API_GUIDE.md](docs/FREE_API_GUIDE.md) for setup!**

---

## 🎯 Prerequisites

- Windows PC
- Python 3.10 or higher
- Internet connection
- API key (FREE options available - see above!)

## 📦 Installation (2 minutes)

### Option 1: Automated Setup (Recommended)

```powershell
# 1. Run the setup script
setup.bat

# 2. Edit .env file and add your API key (Groq is FREE!)
notepad .env

# 3. Launch the application
run_app.bat
```

### Option 2: Manual Setup

```powershell
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
Copy-Item .env.example .env
notepad .env  # Add your API key

# 4. Run application
python src/main.py
```

## 🔑 Get API Key (1 minute)

### Groq ⚡ (FREE - Recommended)
1. Go to: https://console.groq.com/keys
2. Sign up (no credit card needed!)
3. Click "Create API Key"
4. Copy the key to `.env`:
   ```env
   GROQ_API_KEY=your_key_here
   DEFAULT_LLM_PROVIDER=groq
   ```

### OpenAI 💰 (PAID)
1. Go to: https://platform.openai.com/api-keys
2. Sign up/login
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Paste in `.env`: `OPENAI_API_KEY=sk-your-key-here`

### Anthropic (Alternative)
1. Go to: https://console.anthropic.com/
2. Sign up/login
3. Generate API key
4. Copy the key (starts with `sk-ant-`)
5. Paste in `.env`: `ANTHROPIC_API_KEY=sk-ant-your-key-here`

## 🚀 First Business Plan (2 minutes)

### Using Form Input (Most Control)

1. **Launch app**: `run_app.bat`
2. **Click** "📝 Form Input" (already selected)
3. **Fill in**:
   - Business Name: "My Awesome Startup"
   - Industry: "Technology"
   - Business Type: "SaaS"
   - Location: "San Francisco, CA"
   - Description: Brief description of your business
4. **Select** output format (PDF recommended)
5. **Click** "🚀 Generate Business Plan"
6. **Wait** 2-3 minutes for AI to generate
7. **Find** your plan in the `output/` folder

### Using AI Description (Fastest)

1. **Click** "🤖 AI Description"
2. **Delete** the example text
3. **Write** 3-5 sentences about your business idea
4. **Select** PDF format
5. **Click** "🤖 Generate with AI"
6. **Wait** 2-3 minutes
7. **Open** the generated PDF

### Using Template (Easiest)

1. **Click** "📋 Template"
2. **Select** your business type (e.g., "Technology Startup")
3. **Fill in** basic info:
   - Business Name
   - Location
   - Specific Focus
4. **Select** PDF format
5. **Click** "📋 Generate from Template"
6. **Wait** 2-3 minutes
7. **Review** your plan

## 📄 Output Formats

| Format | Best For | Features |
|--------|----------|----------|
| **PDF** | Presentations, printing | Professional layout, ready to share |
| **HTML** | Web viewing, sharing | Responsive, styled, clickable |
| **DOCX** | Editing, customizing | Fully editable in Word |

**Tip**: Generate all three formats! Each has different uses.

## 🎨 Interface Overview

### Sidebar (Left)
- **Input Modes**: Form, AI, Template
- **Settings**: LLM provider selection
- **Theme**: Dark/Light toggle

### Main Area (Right)
- **Input Forms**: Different for each mode
- **Output Selection**: Choose PDF, HTML, DOCX
- **Generate Button**: Start the magic ✨

## 💡 Tips for Best Results

### For All Modes
✅ Be specific about your industry  
✅ Describe your target market clearly  
✅ Mention competitive advantages  
✅ Include realistic numbers  

### Form Mode
✅ Fill in as many fields as possible  
✅ Write detailed descriptions  
✅ Be specific about your innovation  

### AI Description Mode
✅ Write 3-5 paragraphs  
✅ Cover: What, Who, How, Why  
✅ Include target market and revenue model  
✅ Mention any unique selling points  

### Template Mode
✅ Choose the closest matching template  
✅ Customize with your specifics  
✅ Review and edit the output  

## ⚠️ Troubleshooting

### "No API key found"
- Check `.env` file exists
- Verify key is on the correct line
- No quotes around the key
- No spaces before/after `=`

### "Generation failed"
- Check internet connection
- Verify API key is valid
- Check you have API credits
- Try again (sometimes it's a temporary issue)

### "Module not found"
- Activate virtual environment: `.\venv\Scripts\Activate.ps1`
- Reinstall: `pip install -r requirements.txt`

### GUI doesn't start
- Check Python version: `python --version` (need 3.10+)
- Install customtkinter: `pip install customtkinter`
- Check console for error messages

## 📁 Where Are My Files?

Generated business plans are saved in:
```
D:\Project_Kiro\output\
```

Files are named:
```
your_business_name_20261106_143025.pdf
your_business_name_20261106_143025.html
your_business_name_20261106_143025.docx
```

**Tip**: Click "Yes" when asked "Open output folder?" after generation!

## ⚡ Keyboard Shortcuts

- **Ctrl+O**: Open output folder
- **Ctrl+Q**: Quit application
- **F11**: Fullscreen mode

## 🎯 Common Use Cases

### Investor Pitch
1. Use **Form Mode** for maximum control
2. Fill in all financial details
3. Generate **PDF** format
4. Review and customize if needed

### Quick Prototype
1. Use **AI Description Mode**
2. Write 2-3 paragraphs
3. Generate **HTML** to view quickly
4. Iterate if needed

### Course Assignment
1. Use **Template Mode**
2. Choose appropriate business type
3. Generate **DOCX** for easy editing
4. Add custom sections as required

### Accelerator Application
1. Use **Form Mode**
2. Be very detailed
3. Generate **all formats**
4. Use DOCX to add team bios, etc.

## 🔄 Iterating on Your Plan

1. **First Generation**: Get the basic structure
2. **Review**: Read through all sections
3. **Refine**: Adjust your input based on output
4. **Regenerate**: Create improved version
5. **Customize**: Edit DOCX for final touches

## 📚 Next Steps

After generating your first plan:

1. ✅ Read through the entire plan
2. ✅ Check the market analysis
3. ✅ Verify financial projections
4. ✅ Review SWOT analysis
5. ✅ Edit DOCX version for customization
6. ✅ Share with advisors for feedback
7. ✅ Iterate and improve

## 🆘 Need Help?

- **Setup Issues**: See [INSTALLATION.md](INSTALLATION.md)
- **Usage Questions**: See [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **MCP Setup**: See [MCP_SETUP.md](MCP_SETUP.md)
- **All Features**: See [README.md](README.md)

## 💰 API Costs

**Approximate costs per business plan**:

| Provider | Cost per Plan | Notes |
|----------|---------------|-------|
| OpenAI GPT-4 | $0.50 - $2.00 | Depends on detail level |
| Anthropic Claude | $0.40 - $1.80 | Similar to GPT-4 |

**Tips to reduce costs**:
- Start with shorter descriptions
- Generate one format first to preview
- Use templates (less AI processing)

## ⭐ Pro Tips

1. **Save Your Inputs**: Keep a text file with your business description for iterations
2. **Generate Multiple Versions**: Try different approaches to see what works best
3. **Edit the DOCX**: Always customize the Word version for final use
4. **Use Templates First**: Get familiar with the structure before detailed input
5. **Review Competitors**: Look at real business plans for inspiration
6. **Iterate**: Your first plan won't be perfect - that's okay!

## 🎉 You're Ready!

You now know enough to:
- ✅ Install and configure the app
- ✅ Generate your first business plan
- ✅ Choose the right input mode
- ✅ Understand the output formats
- ✅ Troubleshoot common issues

**Now go create something amazing!** 🚀

---

**Remember**: This tool helps you structure and articulate your business idea. The AI provides intelligent suggestions, but YOU know your business best. Review, customize, and make it your own!

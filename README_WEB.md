# Business Plan Generator 🚀

**AI-Powered Professional Business Plans | Desktop + Web Versions**

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.39-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🎉 **TWO VERSIONS AVAILABLE!**

### 🖥️ **Desktop Version** (Original)
- Windows executable (.exe)
- CustomTkinter GUI
- SQLite database
- Local file storage
- **Download:** [Latest Release](https://github.com/venkatashivabramha/Gen-AI/releases)

### 🌐 **Web Version** (NEW!)
- Browser-based interface
- Deployed on Streamlit Cloud
- MongoDB Atlas database
- Cloud file handling
- **Live Demo:** `https://your-app.streamlit.app` (after deployment)

---

## ✨ Key Features

### 🎯 Three Input Modes
- **📝 Form Input** - Detailed structured data entry
- **🤖 AI Description** - Natural language business description
- **📋 Template** - Pre-built industry templates

### 📊 Comprehensive Analysis
- Market analysis with **real-time data** from Yahoo Finance
- SWOT analysis
- 3-year financial projections
- Competitive landscape
- Risk assessment
- Operations planning

### 📄 Multiple Export Formats
- **PDF** - Professional, print-ready
- **DOCX** - Editable Word documents  
- **HTML** - Web-ready pages
- **Markdown** - Developer-friendly

### 🤖 Advanced AI Integration
- Multiple LLM providers (Groq, OpenAI, Anthropic, OpenRouter, HuggingFace)
- RAG (Retrieval Augmented Generation)
- Real market data integration ($9.3T+ markets verified!)
- Industry-specific templates

---

## 🚀 Quick Start

### Option 1: Web Version (Easiest!)

**Try it online (after deployment):**
1. Visit: `https://your-app.streamlit.app`
2. Create account
3. Generate business plan
4. Download in your preferred format

**Deploy your own:**
```bash
# 1. Clone repo
git clone https://github.com/venkatashivabramha/Gen-AI.git
cd Gen-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up MongoDB Atlas (FREE)
# Get connection string from: https://www.mongodb.com/cloud/atlas

# 4. Configure secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml with your MongoDB URI and API keys

# 5. Run locally
streamlit run streamlit_app.py

# 6. Deploy to Streamlit Cloud
# Push to GitHub, then connect at https://streamlit.io/cloud
```

### Option 2: Desktop Version

**Windows Users:**
1. Download `BusinessPlanGenerator.exe` from [Releases](https://github.com/venkatashivabramha/Gen-AI/releases)
2. Run the executable
3. Create account/login
4. Start generating!

**From Source:**
```bash
git clone https://github.com/venkatashivabramha/Gen-AI.git
cd Gen-AI
pip install -r requirements.txt
python main_with_login.py
```

---

## 📖 Documentation

- **[Installation Guide](INSTALLATION.md)** - Detailed setup instructions
- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[Usage Guide](USAGE_GUIDE.md)** - Feature walkthrough
- **[Streamlit Deployment](STREAMLIT_DEPLOYMENT.md)** - Deploy web version
- **[Admin Guide](ADMIN_QUICK_GUIDE.md)** - User management
- **[CLI Guide](CLI_GUIDE.md)** - Command-line interface
- **[Free API Guide](docs/FREE_API_GUIDE.md)** - Setup free AI providers

---

## 🌐 Web Version Architecture

```
Frontend: Streamlit (Python-based web framework)
Backend: Shared Python codebase (src/)
Database: MongoDB Atlas (FREE tier - 512MB)
Hosting: Streamlit Cloud (FREE forever!)
AI: Groq/OpenRouter/Anthropic/OpenAI
Data: Yahoo Finance API (FREE unlimited)
```

### Web Features:
- ✅ Responsive design
- ✅ User authentication
- ✅ Admin dashboard
- ✅ Real-time generation
- ✅ File downloads
- ✅ Auto-deployment from Git

---

## 💡 FREE AI Options

**No credit card required!**

### Groq (Recommended - Fastest & Free)
```bash
# Get key from: https://console.groq.com
GROQ_API_KEY="gsk_..."
```

### OpenRouter (Multiple Free Models)
```bash
# Get key from: https://openrouter.ai
OPENROUTER_API_KEY="sk-or-..."
```

### HuggingFace (Open Source Models)
```bash
# Get key from: https://huggingface.co
HUGGINGFACE_API_KEY="hf_..."
```

See [FREE_API_GUIDE.md](docs/FREE_API_GUIDE.md) for detailed setup.

---

## 🗄️ Database Options

### For Web Version (MongoDB Atlas):
1. Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create FREE M0 cluster (512MB)
3. Get connection string
4. Add to Streamlit secrets

**FREE tier includes:**
- 512MB storage
- Shared RAM
- Supports thousands of users
- No credit card needed

### For Desktop Version:
- SQLite (included, no setup needed)

---

## 🎯 Example Use Cases

### Startup Founders
Generate investor-ready business plans with market data and financial projections.

### Students & Educators
Learn business planning with AI-guided templates and real market insights.

### Consultants
Create multiple client business plans quickly with consistent quality.

### Small Business Owners
Professional plans for loans, grants, and strategic planning.

---

## 📊 System Requirements

### Web Version:
- Modern web browser
- Internet connection
- (No installation required!)

### Desktop Version:
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 500MB disk space
- Internet for API access

---

## 🔒 Security

- ✅ Bcrypt password hashing
- ✅ Secure session management
- ✅ Environment variable protection
- ✅ MongoDB authentication
- ✅ HTTPS (Streamlit Cloud)
- ✅ No credit card storage

---

## 🚀 Deployment to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Connect Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Select repository
   - Add secrets (MongoDB URI, API keys)
   - Deploy!

3. **Your app is live!**
   - URL: `https://your-app.streamlit.app`
   - Auto-updates on git push
   - FREE hosting forever

See [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) for detailed guide.

---

## 📈 Roadmap

- [ ] Multi-language support
- [ ] More industry templates
- [ ] Collaboration features
- [ ] Version history
- [ ] Team workspaces
- [ ] API access
- [ ] White-label options

---

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/venkatashivabramha/Gen-AI/issues)
- **Discussions:** [GitHub Discussions](https://github.com/venkatashivabramha/Gen-AI/discussions)
- **Email:** support@yourdomain.com

---

## 🌟 Star History

If you find this project useful, please give it a star! ⭐

---

## 📸 Screenshots

### Desktop Version
![Desktop App](screenshots/desktop.png)

### Web Version
![Web App Home](screenshots/web-home.png)
![Web Generator](screenshots/web-generator.png)
![Admin Dashboard](screenshots/admin.png)

---

## 🎉 Acknowledgments

- **Streamlit** - Amazing web framework
- **MongoDB Atlas** - Free cloud database
- **Yahoo Finance** - Real market data
- **Groq** - Fast & free AI inference
- **Open source community**

---

**Made with ❤️ | Desktop + Web Versions Available**

[Desktop Download](https://github.com/venkatashivabramha/Gen-AI/releases) | [Web Demo](https://your-app.streamlit.app) | [Documentation](STREAMLIT_DEPLOYMENT.md)

# Free API Provider Guide 🎉

This guide shows you how to use **FREE AI APIs** with the Business Plan Generator, so you don't need to pay for OpenAI or Anthropic!

## 🚀 Recommended FREE Options

### 1. Groq (⭐ RECOMMENDED - FREE & FAST!)

**Why Groq?**
- ✅ Completely FREE
- ✅ Super FAST inference (fastest of all free options)
- ✅ No credit card required
- ✅ Generous free tier limits
- ✅ Easy setup

**How to Get Started:**

1. Visit: https://console.groq.com/keys
2. Sign up for a free account (no credit card needed!)
3. Click "Create API Key"
4. Copy your API key
5. Add to your `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
DEFAULT_LLM_PROVIDER=groq
```

**Available Models:**
- `llama-3.1-8b-instant` - Fast, general purpose (RECOMMENDED)
- `llama-3.1-70b-versatile` - More capable, slower
- `mixtral-8x7b-32768` - Great for long contexts
- `gemma2-9b-it` - Good balance of speed/quality

---

### 2. OpenRouter (⭐ FREE MODELS AVAILABLE)

**Why OpenRouter?**
- ✅ Access to MANY FREE models
- ✅ No credit card required for free models
- ✅ Unified API for multiple providers
- ✅ Good rate limits

**How to Get Started:**

1. Visit: https://openrouter.ai/keys
2. Sign up for a free account
3. Click "Create Key"
4. Copy your API key
5. Add to your `.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
DEFAULT_LLM_PROVIDER=openrouter
```

**FREE Models Available:**
- `meta-llama/llama-3.2-3b-instruct:free` - Fast & capable
- `meta-llama/llama-3.2-1b-instruct:free` - Ultra fast
- `google/gemma-2-9b-it:free` - Google's model
- `mistralai/mistral-7b-instruct:free` - Good quality

**See all free models:** https://openrouter.ai/models?order=newest&supported_parameters=tools&q=free

---

### 3. HuggingFace (FREE TIER)

**Why HuggingFace?**
- ✅ Large community
- ✅ Many models to choose from
- ✅ Free tier available
- ✅ No credit card needed

**How to Get Started:**

1. Visit: https://huggingface.co/settings/tokens
2. Create a free account or log in
3. Click "New token"
4. Give it a name and select "Read" access
5. Copy your token
6. Add to your `.env` file:

```env
HUGGINGFACE_API_KEY=your_huggingface_token_here
HUGGINGFACE_MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1
DEFAULT_LLM_PROVIDER=huggingface
```

**Popular FREE Models:**
- `mistralai/Mixtral-8x7B-Instruct-v0.1` - High quality
- `meta-llama/Meta-Llama-3-8B-Instruct` - Fast & good
- `google/gemma-2-9b-it` - Google's Gemma
- `microsoft/Phi-3-mini-4k-instruct` - Compact but capable

---

## 📊 Comparison Table

| Provider | Speed | Quality | Setup Difficulty | Rate Limits | Best For |
|----------|-------|---------|------------------|-------------|----------|
| **Groq** ⭐ | ⚡ Fastest | Good | Easy | Generous | Quick generations |
| **OpenRouter** | Fast | Variable | Easy | Good | Experimenting with models |
| **HuggingFace** | Medium | Good | Medium | Moderate | Open source enthusiasts |
| OpenAI 💰 | Fast | Excellent | Easy | Pay-per-use | Production (PAID) |
| Anthropic 💰 | Fast | Excellent | Easy | Pay-per-use | Production (PAID) |

---

## 🔧 Setup Instructions

### Step 1: Choose Your Provider

We recommend **Groq** for most users (free, fast, easy).

### Step 2: Get Your API Key

Follow the provider-specific instructions above.

### Step 3: Configure Your `.env` File

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```env
   # For Groq (recommended)
   GROQ_API_KEY=gsk_your_actual_key_here
   DEFAULT_LLM_PROVIDER=groq
   
   # OR for OpenRouter
   OPENROUTER_API_KEY=sk-or-your_actual_key_here
   DEFAULT_LLM_PROVIDER=openrouter
   
   # OR for HuggingFace
   HUGGINGFACE_API_KEY=hf_your_actual_key_here
   DEFAULT_LLM_PROVIDER=huggingface
   ```

### Step 4: Select Provider in GUI

When you run the app:
1. Look at the left sidebar under "Settings"
2. You'll see a dropdown with provider options
3. Select your configured provider
4. Generate your business plan!

---

## 💡 Tips & Best Practices

### Rate Limits

All free providers have rate limits:

- **Groq**: ~30 requests/minute (very generous)
- **OpenRouter**: Varies by model (check their docs)
- **HuggingFace**: ~1000 requests/day for free tier

**Tip**: If you hit a rate limit, wait a minute and try again, or switch providers!

### Model Selection

For business plan generation:
- **Fast & Good**: Groq's `llama-3.1-8b-instant`
- **Best Quality Free**: OpenRouter's free Llama 3.2 models
- **Most Tokens**: Groq's `mixtral-8x7b-32768` (32k context)

### Troubleshooting

**"API key not found" error:**
- Make sure you created a `.env` file (not just `.env.example`)
- Check that your API key is correctly copied
- Restart the application after changing `.env`

**"Rate limit exceeded":**
- Wait 60 seconds and try again
- Or switch to another provider in the GUI

**"Model not found":**
- Check the provider's documentation for current model names
- Some models may be temporarily unavailable
- Try the default model for that provider

**Slow generation:**
- Some free models are slower than paid options
- Groq is fastest for free tier
- Be patient - quality takes time!

---

## 🎯 Quick Start Commands

### For Groq (Recommended):
```powershell
# Get API key from: https://console.groq.com/keys
# Then add to .env:
GROQ_API_KEY=your_key_here
DEFAULT_LLM_PROVIDER=groq
```

### Test it:
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the GUI
python src/main.py

# Or test via CLI
python src/cli.py --name "TechCo" --description "A SaaS startup" --output-format html
```

---

## 📚 Additional Resources

### Provider Documentation:
- **Groq**: https://console.groq.com/docs
- **OpenRouter**: https://openrouter.ai/docs
- **HuggingFace**: https://huggingface.co/docs/api-inference

### Getting Help:
- Check the main [README.md](../README.md)
- See [USAGE_GUIDE.md](./USAGE_GUIDE.md) for detailed usage
- See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) if you have issues

---

## 🎉 You're Ready!

Now you can generate professional business plans **for FREE** using cutting-edge AI models!

**Remember**: 
1. Choose Groq for speed ⚡
2. Choose OpenRouter for variety 🎨  
3. Choose HuggingFace for open source ❤️

Happy business planning! 🚀

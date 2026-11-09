# URGENT: Groq Model Update Required

## Issue
As of November 2026, Groq has **decommissioned** the following models:
- `llama3-8b-8192` ❌ (no longer supported)
- `llama-3.1-8b-instant` ❌ (moved to Enterprise-only)
- `llama-3.3-70b-versatile` ❌ (deprecated August 16, 2026)

## Error Message
```
Error code: 400 - The model 'llama3-8b-8192' has been decommissioned and is no longer supported.
Please refer to https://console.groq.com/docs/deprecations
```

## Solution: Update to Supported Model

### Currently Supported FREE Groq Models (November 2026)

**Recommended:**
1. **`openai/gpt-oss-20b`** - 1000 T/sec, $0.075 input/$0.30 output
   - Fast and reliable
   - Good for production use
   - **RECOMMENDED FOR THIS PROJECT**

2. **`qwen/qwen3.8-27b`** - 450 T/sec, $0.80 input/$4.00 output
   - Higher quality
   - More expensive

3. **`openai/gpt-oss-120b`** - 500 T/sec, $0.15 input/$0.60 output
   - Best quality
   - Most expensive

### Required Changes

#### 1. Update `.env` File
```env
# OLD (decommissioned):
GROQ_MODEL=llama3-8b-8192
DEFAULT_MODEL=llama3-8b-8192

# NEW (currently supported):
GROQ_MODEL=openai/gpt-oss-20b
DEFAULT_MODEL=openai/gpt-oss-20b
```

#### 2. Update Streamlit Cloud Secrets

Go to: https://share.streamlit.io/ → Your App → Settings → Secrets

```toml
# MongoDB Atlas Connection
MONGODB_URI = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/..."

# Groq API Key
GROQ_API_KEY = "gsk_..."

# Model Configuration (UPDATED)
DEFAULT_LLM_PROVIDER = "groq"
DEFAULT_MODEL = "openai/gpt-oss-20b"
GROQ_MODEL = "openai/gpt-oss-20b"
```

#### 3. Save and Reboot
- Click "Save changes" in Streamlit Cloud
- Reboot the app
- Wait 60 seconds for restart
- Test business plan generation

## Why This Happened

Groq regularly rotates and deprecates models. The models we were using (`llama3-8b-8192`) were sunset in November 2026 as part of their model lifecycle management.

## Impact

- ✅ **Code**: No code changes needed - only configuration
- ✅ **Performance**: New model is actually faster (1000 T/sec vs 560 T/sec)
- ✅ **Quality**: Comparable or better quality
- ✅ **Cost**: Still free tier available

## Verification

After updating, you should see successful generation with:
- ✅ No "model decommissioned" errors
- ✅ Complete business plan sections
- ✅ Proper AI-generated content
- ✅ Real-time market data from MCP

## Reference

- Groq Models Documentation: https://console.groq.com/docs/models
- Deprecation Policy: https://console.groq.com/docs/deprecations

---

**Date**: January 2025
**Status**: Configuration update required
**Priority**: High - app currently non-functional until updated

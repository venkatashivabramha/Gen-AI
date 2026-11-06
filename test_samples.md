# Sample Inputs to Test Business Plan Generator

## 🎯 Quick Test Samples

---

## Option 1: TEMPLATE MODE (Easiest - 2 minutes)

### Steps:
1. Click **"📋 Template"** button in left sidebar
2. Fill in these exact values:

```
Template Selection: Technology Startup

Business Name: TechFlow AI Solutions

Location: San Francisco, California

Specific Focus: AI-powered project management tools for remote teams
```

3. Check **PDF** format
4. Click **"📋 Generate from Template"**
5. Wait 2-3 minutes
6. Check `D:\Project_Kiro\output\` folder for your PDF!

---

## Option 2: AI DESCRIPTION MODE (Fast - 3 minutes)

### Steps:
1. Click **"🤖 AI Description"** button
2. Delete the example text
3. Copy and paste this:

```
I want to start an e-commerce business called "EcoHome Essentials" 
that sells sustainable, eco-friendly home products. We'll target 
environmentally conscious consumers aged 25-45 with household incomes 
of $60,000+, primarily in urban areas across the United States.

Our product line includes biodegradable cleaning supplies, reusable 
kitchen items, sustainable personal care products, and eco-friendly 
home decor. We'll source from certified sustainable manufacturers 
and small businesses.

The business model is direct-to-consumer through our website, with 
plans to expand to Amazon and Etsy. Revenue comes from product sales 
with 40-50% profit margins. We'll start with $100,000 in initial 
funding for inventory, website development, and digital marketing.

Our unique value proposition is curated, high-quality eco-products 
with carbon-neutral shipping and a subscription box option for 
regular customers.
```

4. Check **PDF** format
5. Click **"🤖 Generate with AI"**
6. Wait 3-4 minutes (longer because it's analyzing the text)
7. Get your business plan!

---

## Option 3: FORM MODE (Most Detailed - 5 minutes)

### Steps:
1. Click **"📝 Form Input"** button (or it's already selected)
2. Fill in these fields:

```
Business Name: CloudSync Pro

Industry: Technology / SaaS

Business Type: Software as a Service (SaaS)

Location: Austin, Texas

Target Market: Small to medium-sized businesses (50-500 employees) 
in the United States that need cloud-based collaboration tools. 
Primary sectors include tech companies, marketing agencies, 
consulting firms, and remote-first organizations.

Products/Services: Cloud-based team collaboration platform featuring 
real-time document editing, video conferencing, project management, 
file storage, and integrated chat. Includes mobile apps for iOS and 
Android, desktop apps for Windows and Mac, and web access.

Revenue Model: Monthly subscription model with three tiers:
- Basic: $10/user/month (up to 25 users)
- Professional: $25/user/month (unlimited users, advanced features)
- Enterprise: Custom pricing (dedicated support, custom integrations)

Initial Investment: $500,000 covering:
- Product development: $250,000
- Marketing and sales: $150,000
- Operations and overhead: $100,000
- First 18 months runway

Innovation Focus: AI-powered smart scheduling that analyzes team 
patterns to suggest optimal meeting times, automatic task 
prioritization based on deadlines and dependencies, and predictive 
analytics for project completion dates. Integration with 50+ 
popular business tools via API.

Business Description: CloudSync Pro is a next-generation 
collaboration platform designed for the modern remote workforce. 
Unlike traditional tools that simply replicate in-person meetings 
online, we use artificial intelligence to make remote work more 
efficient than office work. Our platform learns from team behavior 
to proactively prevent bottlenecks, suggest improvements, and 
automate routine coordination tasks. We're targeting the $50 billion 
collaboration software market, which is growing 15% annually as 
remote work becomes permanent for millions of workers.
```

3. Select **PDF**, **HTML**, and **DOCX** (all three!)
4. Click **"🚀 Generate Business Plan"**
5. Wait 4-5 minutes (most comprehensive)
6. Get 3 files with complete business plan!

---

## 🧪 Quick CLI Test (Optional)

If you want to test without GUI, run this in PowerShell:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Test with AI description
python src/cli.py --mode ai --description "A mobile app for fitness tracking with AI-powered workout recommendations" --formats html

# Or test with template
python src/cli.py --mode template --template "Technology Startup" --name "FitAI" --location "Seattle, WA" --formats pdf
```

---

## ✅ How to Verify It Worked

### Success Indicators:

1. **During Generation:**
   - Progress dialog appears
   - Shows "Generating your business plan..."
   - Takes 2-5 minutes (this is normal!)

2. **After Generation:**
   - Success message appears
   - Shows file paths created
   - Asks if you want to open output folder

3. **Check Output:**
   ```powershell
   # Open output folder
   explorer D:\Project_Kiro\output
   ```
   
   You should see files like:
   - `techflow_ai_solutions_20261106_123456.pdf`
   - `ecohome_essentials_20261106_123456.pdf`
   - `cloudsync_pro_20261106_123456.pdf`

4. **Open the PDF:**
   - Should have professional cover page
   - Table of contents
   - Multiple sections:
     * Executive Summary
     * Business Description
     * Market Analysis
     * SWOT Analysis
     * Financial Projections
     * Innovation Strategy

---

## 🎯 Recommended Test Order

### Test 1: Template Mode (Fastest verification)
- Use sample above
- Should take 2-3 minutes
- Proves AI connection works

### Test 2: AI Description Mode (Test natural language)
- Use sample above
- Should take 3-4 minutes
- Proves AI can extract business info

### Test 3: Form Mode (Full features)
- Use sample above
- Should take 4-5 minutes
- Generates most comprehensive plan

---

## 📊 Expected Output Quality

### What You Should See in Generated Plans:

✅ **Executive Summary:**
- 2-3 paragraphs
- Business overview
- Market opportunity
- Key highlights
- Investment ask

✅ **Market Analysis:**
- Industry overview (2-3 paragraphs)
- Market size estimates
- Target market details
- Competitive landscape (3-5 competitors)
- Market trends (3-5 points)
- Entry strategy

✅ **SWOT Analysis:**
- 5-7 Strengths
- 5-7 Weaknesses
- 5-7 Opportunities
- 5-7 Threats

✅ **Financial Projections:**
- 3-year revenue forecast
- Cost breakdown
- Profit margins
- Break-even analysis
- Key assumptions

✅ **Innovation Strategy:**
- Unique differentiators
- Technology integration
- Implementation timeline
- Resource needs
- Success metrics

---

## ⚠️ If Generation Fails

### Common Issues:

1. **Takes too long (>10 minutes):**
   - Check internet connection
   - API might be slow (try again)

2. **Error about API key:**
   - Check .env file has your key
   - No quotes around the key
   - Key starts with `sk-ant-`

3. **Quality seems low:**
   - Try again with more detailed input
   - Use Form Mode for best results
   - Be specific about your business

4. **Empty sections:**
   - Regenerate (sometimes happens)
   - Provide more business details
   - Try different input mode

---

## 💡 Pro Testing Tips

1. **Start with Template Mode** - Quickest way to verify it works

2. **Try HTML first** - Opens faster than PDF, easier to preview

3. **Generate multiple formats** - Compare PDF, HTML, DOCX quality

4. **Test all three modes** - Each has different strengths

5. **Keep your first test simple** - Don't overthink it, just test!

---

## 🚀 Ready to Test!

**Pick ONE sample above and try it now!**

**Recommended:** Start with Template Mode sample (easiest)

The GUI is already running and waiting for you! 🎉

# Usage Guide - Business Plan Generator

## Getting Started

### Launching the Application

```powershell
# Activate virtual environment (if using one)
.\venv\Scripts\Activate.ps1

# Run the application
python src/main.py
```

## Input Modes

The Business Plan Generator offers three ways to create your business plan:

### 1. 📝 Form Input Mode

**Best for**: Detailed control and structured input

**How to use**:
1. Click "📝 Form Input" in the sidebar
2. Fill in all relevant fields:
   - Business Name (required)
   - Industry
   - Business Type
   - Location
   - Target Market
   - Products/Services
   - Revenue Model
   - Initial Investment
   - Innovation Focus
   - Business Description
3. Select output formats (PDF, HTML, DOCX)
4. Click "🚀 Generate Business Plan"

**Tips**:
- Be specific in your descriptions
- The more detail you provide, the better the AI-generated content
- All fields help the AI understand your business better

### 2. 🤖 AI Description Mode

**Best for**: Quick generation from a natural description

**How to use**:
1. Click "🤖 AI Description" in the sidebar
2. Clear the example text
3. Write a natural description of your business idea (2-3 paragraphs recommended)
4. Select output formats
5. Click "🤖 Generate with AI"

**Example Description**:
```
I want to start a technology startup that uses AI to help small businesses 
automate their customer service. We'll target small to medium businesses in 
the retail and hospitality sectors who struggle with 24/7 customer support. 

Our platform will integrate with existing systems and provide intelligent 
chatbots that can handle common queries, escalate complex issues, and learn 
from interactions. 

We plan to offer a subscription-based model with tiered pricing based on 
the number of interactions. Initial funding needed is around $200,000 for 
development and first-year operations.
```

### 3. 📋 Template Mode

**Best for**: Starting with industry-standard structures

**How to use**:
1. Click "📋 Template" in the sidebar
2. Select a business type from the dropdown:
   - Technology Startup
   - E-commerce
   - Restaurant/Food Service
   - Retail Store
   - Consulting Services
   - Manufacturing
   - Healthcare Services
   - Real Estate
   - Education/Training
   - Other
3. Fill in basic information:
   - Business Name (required)
   - Location
   - Specific Focus
4. Select output formats
5. Click "📋 Generate from Template"

## Understanding the Output

### Generated Sections

Each business plan includes:

1. **Executive Summary**
   - High-level overview
   - Key highlights
   - Investment ask

2. **Business Description**
   - Detailed company information
   - Mission and vision
   - Products/services overview

3. **Market Analysis**
   - Industry overview
   - Market size and trends
   - Target market demographics
   - Competitive landscape
   - Market entry strategy

4. **SWOT Analysis**
   - Strengths (internal positives)
   - Weaknesses (internal challenges)
   - Opportunities (external positives)
   - Threats (external challenges)

5. **Financial Projections**
   - Revenue projections (3-year)
   - Cost structure
   - Break-even analysis
   - Profit margins
   - Key financial assumptions

6. **Innovation & Implementation Strategy**
   - Innovative differentiators
   - Technology integration
   - Implementation timeline
   - Resource requirements
   - Success metrics

### Output Formats

#### PDF
- Professional, print-ready format
- Best for: Presentations, investor meetings, formal submissions
- Features: Cover page, table of contents, formatted sections

#### HTML
- Web-ready format
- Best for: Websites, online sharing, easy viewing
- Features: Responsive design, clickable navigation, modern styling

#### DOCX (Word)
- Editable format
- Best for: Further customization, collaborative editing
- Features: Standard Word formatting, easy to modify

## Advanced Features

### Settings

Access settings in the sidebar:

1. **LLM Provider Selection**
   - OpenAI (GPT-4)
   - Anthropic (Claude)
   - Choose based on your API key and preference

2. **Theme Toggle**
   - Switch between dark and light mode
   - Click "🌙 Dark/Light" button

### MCP Integration

If MCP (Model Context Protocol) is enabled:
- Enhanced market research data
- Real-time financial benchmarks
- Competitor analysis
- Regulatory information

To enable MCP:
1. Set `MCP_ENABLED=true` in `.env`
2. Configure MCP server URL
3. Ensure MCP server is running

## Tips for Best Results

### Form Input Mode
- **Be specific**: Instead of "target market: everyone", say "urban millennials aged 25-40 with disposable income"
- **Provide context**: Explain WHY your business is unique
- **Include numbers**: Estimated costs, prices, market size

### AI Description Mode
- **Write 3-5 paragraphs**: Cover what, who, how, and why
- **Include specifics**: Industry, target market, revenue model
- **Mention competition**: What makes you different
- **State funding needs**: If applicable

### Template Mode
- **Choose the right template**: Pick the closest match to your business
- **Customize the basics**: Add your unique focus areas
- **Review and edit**: Templates are starting points, customize the output

## Common Workflows

### Quick Prototype
1. Use AI Description Mode
2. Write 2-3 paragraphs
3. Generate PDF only
4. Review and iterate

### Detailed Business Plan
1. Use Form Input Mode
2. Fill all fields thoroughly
3. Generate all formats (PDF, HTML, DOCX)
4. Edit DOCX for final touches

### Investor Presentation
1. Use Template Mode (Technology Startup)
2. Provide detailed financial information
3. Generate PDF
4. Print or present digitally

## Troubleshooting

### Generation Taking Too Long
- AI generation typically takes 2-5 minutes
- Complex plans may take longer
- Check your internet connection
- Verify API keys are valid

### Content Quality Issues
- Provide more detailed input
- Be specific about your business
- Try different input modes
- Adjust LLM provider in settings

### Output File Issues
- Check `output/` folder for generated files
- Ensure you have write permissions
- Try different output formats
- Check disk space

## Keyboard Shortcuts

- **Ctrl+Q**: Quit application
- **Ctrl+N**: New business plan (clears form)
- **Ctrl+O**: Open output folder

## Next Steps After Generation

1. **Review the content**: Read through each section
2. **Edit as needed**: Use the DOCX format for editing
3. **Add custom details**: Financial specifics, team bios, etc.
4. **Validate numbers**: Review financial projections
5. **Get feedback**: Share with mentors or advisors
6. **Refine and iterate**: Generate multiple versions

## Support

For issues or questions:
- Check INSTALLATION.md for setup issues
- Review this guide for usage questions
- Check the console output for error messages

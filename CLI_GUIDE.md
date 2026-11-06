# Command-Line Interface Guide

For users who prefer the command line or want to automate business plan generation.

## Quick Start

### Interactive Mode (Easiest)

Just run without arguments:

```powershell
python src/cli.py
```

The script will guide you through the process step-by-step.

### Command-Line Mode (Fastest)

Provide all arguments at once:

```powershell
# AI Description Mode
python src/cli.py --mode ai --description "Your business idea here"

# Form Mode
python src/cli.py --mode form --name "MyBusiness" --industry "Technology"

# Template Mode
python src/cli.py --mode template --template "Technology Startup" --name "TechCorp"
```

## Usage Examples

### Example 1: Quick AI Generation

```powershell
python src/cli.py --mode ai --description "A SaaS platform for project management targeting remote teams. Monthly subscription model starting at $10/user. Need $500k initial investment." --formats pdf html
```

### Example 2: Detailed Form Input

```powershell
python src/cli.py --mode form `
  --name "EcoHome Products" `
  --industry "E-commerce" `
  --business-type "Retail" `
  --location "Seattle, WA" `
  --target-market "Environmentally conscious consumers aged 25-45" `
  --products "Eco-friendly home and personal care products" `
  --revenue-model "Product sales with 40-50% margins" `
  --investment "$100,000" `
  --innovation "Sustainable sourcing and carbon-neutral shipping" `
  --detailed-description "An e-commerce platform selling sustainable alternatives to common household products." `
  --formats pdf docx
```

### Example 3: Template-Based Generation

```powershell
python src/cli.py --mode template `
  --template "Technology Startup" `
  --name "DataFlow Solutions" `
  --location "Austin, TX" `
  --innovation "AI-powered analytics" `
  --formats pdf
```

### Example 4: Use Anthropic Claude

```powershell
python src/cli.py --mode ai `
  --description "Restaurant concept for modern Asian fusion cuisine" `
  --provider anthropic `
  --formats pdf html docx
```

## Command-Line Arguments

### Required Arguments

| Argument | Description | Modes |
|----------|-------------|-------|
| `--mode` | Input mode: `form`, `ai`, or `template` | All |

### Common Arguments

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--name` | Business name | Required for form/template | `"TechCorp Inc"` |
| `--formats` | Output formats | `pdf` | `pdf html docx` |
| `--provider` | LLM provider | `openai` | `anthropic` |

### AI Mode Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `--description` | Business description | ✅ Yes |

### Template Mode Arguments

| Argument | Description | Required | Options |
|----------|-------------|----------|---------|
| `--template` | Business type | ✅ Yes | See templates below |

### Form Mode Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `--name` | Business name | ✅ Yes |
| `--industry` | Industry/sector | No |
| `--business-type` | Type of business | No |
| `--location` | Location | No |
| `--target-market` | Target market | No |
| `--products` | Products/services | No |
| `--revenue-model` | Revenue model | No |
| `--investment` | Initial investment | No |
| `--innovation` | Innovation focus | No |
| `--detailed-description` | Full description | No |

## Available Templates

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

## Output

Generated files are saved in the `output/` directory:

```
output/
├── your_business_name_20261106_143025.pdf
├── your_business_name_20261106_143025.html
└── your_business_name_20261106_143025.docx
```

## Automation Examples

### Batch Generation Script

Create `generate_multiple.ps1`:

```powershell
# Generate plans for multiple business ideas

$businesses = @(
    @{
        name = "TechFlow"
        description = "AI project management for remote teams"
    },
    @{
        name = "EcoStore"
        description = "Sustainable home products e-commerce"
    },
    @{
        name = "HealthTrack"
        description = "Personal health monitoring app"
    }
)

foreach ($biz in $businesses) {
    Write-Host "Generating plan for $($biz.name)..."
    python src/cli.py --mode ai `
        --description $biz.description `
        --formats pdf html
}

Write-Host "All plans generated!"
```

Run: `.\generate_multiple.ps1`

### Integration with CI/CD

```yaml
# .github/workflows/generate-plan.yml
name: Generate Business Plan

on:
  workflow_dispatch:
    inputs:
      business_name:
        description: 'Business Name'
        required: true
      description:
        description: 'Business Description'
        required: true

jobs:
  generate:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Generate plan
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python src/cli.py --mode ai \
            --description "${{ github.event.inputs.description }}" \
            --formats pdf html
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: business-plans
          path: output/
```

## Tips & Tricks

### Long Descriptions

For multi-line descriptions, use quotes:

```powershell
python src/cli.py --mode ai --description "Line 1
Line 2
Line 3"
```

Or use a here-string (PowerShell):

```powershell
$description = @"
This is a detailed description
with multiple lines
and paragraphs.
"@

python src/cli.py --mode ai --description $description
```

### Environment Variables

Set default provider:

```powershell
$env:DEFAULT_LLM_PROVIDER = "anthropic"
python src/cli.py --mode ai --description "..."
```

### Quiet Mode

Redirect output to log:

```powershell
python src/cli.py --mode ai --description "..." > generation.log 2>&1
```

### Check Generation Status

```powershell
$result = python src/cli.py --mode ai --description "..."
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success!"
} else {
    Write-Host "Failed!"
}
```

## Troubleshooting

### "No API key found"

Set environment variable:

```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
python src/cli.py ...
```

Or add to `.env` file.

### "Module not found"

Activate virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
python src/cli.py ...
```

### Long generation times

Generation typically takes 2-5 minutes. Be patient!

### Encoding issues

If you see encoding errors with special characters:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python src/cli.py ...
```

## Advanced Usage

### Custom Output Directory

Edit `config/config.py`:

```python
OUTPUT_DIR = Path("D:/MyBusinessPlans")
```

### Scripting Multiple Formats

```powershell
# Generate all formats
python src/cli.py --mode ai --description "..." --formats pdf html docx

# Generate only PDF
python src/cli.py --mode ai --description "..." --formats pdf

# Generate HTML for preview, then PDF for final
python src/cli.py --mode ai --description "..." --formats html
# Review HTML, then:
python src/cli.py --mode ai --description "..." --formats pdf
```

### Parallel Generation

```powershell
# Generate multiple plans in parallel
Start-Job { python src/cli.py --mode ai --description "Business 1" }
Start-Job { python src/cli.py --mode ai --description "Business 2" }
Get-Job | Wait-Job
Get-Job | Receive-Job
```

## Help

Get help anytime:

```powershell
python src/cli.py --help
```

## Comparison: CLI vs GUI

| Feature | CLI | GUI |
|---------|-----|-----|
| **Speed** | ⚡ Fast | Normal |
| **Automation** | ✅ Yes | ❌ No |
| **User-friendly** | Technical | ✅ Very |
| **Batch processing** | ✅ Yes | ❌ No |
| **Visual feedback** | Text | ✅ Progress bar |
| **Editing** | Repeat command | ✅ Form fields |

Choose CLI for:
- Automation
- Batch generation
- CI/CD integration
- Scripting

Choose GUI for:
- First time use
- Interactive editing
- Visual feedback
- Easier input

---

Both interfaces use the same engine and produce identical results!

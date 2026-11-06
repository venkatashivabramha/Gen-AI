# MCP (Model Context Protocol) Setup Guide

## What is MCP?

MCP (Model Context Protocol) allows the Business Plan Generator to access additional tools and data sources for enhanced business intelligence, market research, and financial analysis.

## Benefits of MCP Integration

- **Enhanced Market Data**: Real-time market trends and statistics
- **Financial Benchmarks**: Industry-standard financial metrics
- **Competitive Intelligence**: Automated competitor analysis
- **Regulatory Information**: Industry-specific compliance requirements

## Configuration

### Option 1: Kiro IDE MCP Configuration

If you're using Kiro IDE, create or edit `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "business-research": {
      "command": "python",
      "args": ["-m", "mcp_servers.business_research"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      },
      "disabled": false
    },
    "market-data": {
      "command": "uvx",
      "args": ["market-data-mcp-server@latest"],
      "disabled": false
    },
    "financial-analysis": {
      "command": "node",
      "args": ["financial-mcp-server/index.js"],
      "disabled": true
    }
  }
}
```

### Option 2: Application-Level Configuration

Configure MCP in your `.env` file:

```env
# Enable MCP
MCP_ENABLED=true

# MCP Server URL (if using external server)
MCP_SERVER_URL=http://localhost:8080
```

## Available MCP Tools

### Market Research Tools

**Tool**: `market_research`
- Get market size, growth rates, and trends
- Industry-specific analysis
- Regional market data

**Parameters**:
```json
{
  "industry": "Technology",
  "region": "United States",
  "metrics": ["size", "growth_rate", "trends"]
}
```

### Financial Benchmarks

**Tool**: `financial_benchmarks`
- Industry-standard profit margins
- Operating cost benchmarks
- Revenue growth expectations

**Parameters**:
```json
{
  "industry": "E-commerce",
  "metrics": ["profit_margin", "revenue_growth", "operating_costs"]
}
```

### Competitor Analysis

**Tool**: `competitor_analysis`
- Identify key competitors
- Compare business models
- Market positioning

**Parameters**:
```json
{
  "industry": "Technology",
  "business_type": "SaaS",
  "analysis_depth": "comprehensive"
}
```

### Regulatory Information

**Tool**: `regulatory_info`
- Industry regulations
- Compliance requirements
- Licensing needs

**Parameters**:
```json
{
  "industry": "Healthcare",
  "location": "United States"
}
```

## Creating Custom MCP Servers

### Python MCP Server Example

Create `mcp_servers/business_research.py`:

```python
"""
Custom MCP Server for Business Research
"""
import json
import sys

def handle_request(request):
    """Handle MCP tool requests"""
    tool_name = request.get('tool')
    params = request.get('parameters', {})
    
    if tool_name == 'market_research':
        return get_market_research(params)
    elif tool_name == 'financial_benchmarks':
        return get_financial_benchmarks(params)
    
    return {'error': 'Unknown tool'}

def get_market_research(params):
    """Get market research data"""
    industry = params.get('industry')
    
    # In production, fetch from real data sources
    return {
        'market_size': '$100B',
        'growth_rate': '15% CAGR',
        'trends': [
            'Digital transformation',
            'AI adoption',
            'Cloud migration'
        ]
    }

def get_financial_benchmarks(params):
    """Get financial benchmarks"""
    industry = params.get('industry')
    
    return {
        'profit_margin': '15-25%',
        'revenue_growth': '20-30% YoY',
        'operating_costs': '60-70% of revenue'
    }

if __name__ == '__main__':
    # Read request from stdin
    request = json.load(sys.stdin)
    
    # Process request
    response = handle_request(request)
    
    # Write response to stdout
    print(json.dumps(response))
```

### Node.js MCP Server Example

Create `market-data-server/index.js`:

```javascript
const express = require('express');
const app = express();

app.use(express.json());

// Market research endpoint
app.post('/tools/market_research', (req, res) => {
  const { industry, region } = req.body;
  
  res.json({
    market_size: '$100B',
    growth_rate: '15% CAGR',
    trends: ['Digital transformation', 'AI adoption']
  });
});

// Financial benchmarks endpoint
app.post('/tools/financial_benchmarks', (req, res) => {
  const { industry } = req.body;
  
  res.json({
    profit_margin: '15-25%',
    revenue_growth: '20-30%',
    operating_costs: '60-70%'
  });
});

// Tools discovery endpoint
app.get('/tools', (req, res) => {
  res.json({
    tools: [
      'market_research',
      'financial_benchmarks',
      'competitor_analysis'
    ]
  });
});

app.listen(8080, () => {
  console.log('MCP server running on port 8080');
});
```

## Testing MCP Integration

### 1. Start MCP Server

```powershell
# Python server
python mcp_servers/business_research.py

# Node.js server
node market-data-server/index.js
```

### 2. Verify Connection

In the Business Plan Generator application:
1. Check console output for "MCP: Discovered X tools"
2. If MCP is connected, market data will be enhanced

### 3. Test Without MCP

MCP is optional. The application works perfectly without it, using only AI-generated content.

## Data Sources for MCP

To make your MCP server useful, integrate with:

### Market Research APIs
- Statista API
- IBISWorld API
- Bloomberg API
- Custom scrapers

### Financial Data
- Yahoo Finance
- Alpha Vantage
- Financial Modeling Prep
- SEC EDGAR

### Competitive Intelligence
- Crunchbase API
- PitchBook
- CB Insights
- Web scraping

## Security Considerations

1. **API Keys**: Store API keys securely, not in code
2. **Rate Limiting**: Implement rate limits on MCP endpoints
3. **Data Validation**: Validate all inputs
4. **Authentication**: Add authentication for production use

## Troubleshooting

### MCP Server Not Connecting

1. Check if server is running: `curl http://localhost:8080/tools`
2. Verify MCP_SERVER_URL in `.env`
3. Check firewall settings
4. Review server logs

### Tools Not Discovered

1. Ensure `/tools` endpoint returns tool list
2. Check tool name format (lowercase, underscores)
3. Verify server URL is correct

### Empty or Invalid Data

1. Check MCP server logs
2. Verify API keys for data sources
3. Test data source APIs directly
4. Add error handling in MCP server

## Benefits Without MCP

Even without MCP, the Business Plan Generator provides:
- AI-powered market analysis
- SWOT analysis
- Financial projections
- Innovation strategies
- Professional document generation

MCP simply **enhances** these capabilities with real-time data.

## Further Reading

- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Building MCP Servers](https://modelcontextprotocol.io/docs/servers)
- [MCP Tools Best Practices](https://modelcontextprotocol.io/docs/tools)

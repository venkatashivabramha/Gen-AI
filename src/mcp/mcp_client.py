"""
MCP (Model Context Protocol) Client Integration
Enables enhanced AI capabilities through MCP servers
"""
import json
import requests
from typing import Dict, Any, Optional, List
from config.config import MCP_SERVER_URL, MCP_ENABLED


class MCPClient:
    """Client for interacting with MCP servers"""
    
    def __init__(self, server_url: str = MCP_SERVER_URL, enabled: bool = MCP_ENABLED):
        self.server_url = server_url
        self.enabled = enabled
        self.available_tools = []
        
        if self.enabled:
            self._discover_tools()
    
    def _discover_tools(self):
        """Discover available tools from MCP server"""
        try:
            response = requests.get(f"{self.server_url}/tools")
            if response.status_code == 200:
                self.available_tools = response.json().get("tools", [])
                print(f"MCP: Discovered {len(self.available_tools)} tools")
        except Exception as e:
            print(f"MCP: Could not connect to server: {e}")
            self.enabled = False
    
    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call a specific MCP tool"""
        if not self.enabled:
            return None
        
        try:
            response = requests.post(
                f"{self.server_url}/tools/{tool_name}",
                json=parameters,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"MCP: Tool call failed: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"MCP: Error calling tool {tool_name}: {e}")
            return None
    
    def get_market_data(self, industry: str, region: str) -> Optional[Dict[str, Any]]:
        """Get market data using MCP tools"""
        return self.call_tool("market_research", {
            "industry": industry,
            "region": region,
            "metrics": ["size", "growth_rate", "trends"]
        })
    
    def get_financial_benchmarks(self, industry: str) -> Optional[Dict[str, Any]]:
        """Get financial benchmarks for an industry"""
        return self.call_tool("financial_benchmarks", {
            "industry": industry,
            "metrics": ["profit_margin", "revenue_growth", "operating_costs"]
        })
    
    def get_competitor_analysis(self, industry: str, business_type: str) -> Optional[Dict[str, Any]]:
        """Get competitor analysis data"""
        return self.call_tool("competitor_analysis", {
            "industry": industry,
            "business_type": business_type,
            "analysis_depth": "comprehensive"
        })
    
    def enhance_business_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance business plan with MCP data"""
        if not self.enabled:
            return plan_data
        
        enhanced = plan_data.copy()
        
        # Enhance with market data
        if "industry" in plan_data:
            market_data = self.get_market_data(
                plan_data["industry"],
                plan_data.get("location", "United States")
            )
            if market_data:
                enhanced["mcp_market_data"] = market_data
        
        # Enhance with financial benchmarks
        if "industry" in plan_data:
            benchmarks = self.get_financial_benchmarks(plan_data["industry"])
            if benchmarks:
                enhanced["mcp_financial_benchmarks"] = benchmarks
        
        return enhanced
    
    def is_available(self) -> bool:
        """Check if MCP is available"""
        return self.enabled and len(self.available_tools) > 0


class MCPBusinessTools:
    """Business-specific MCP tools wrapper"""
    
    def __init__(self):
        self.client = MCPClient()
    
    def analyze_market_trends(self, industry: str, timeframe: str = "5years") -> str:
        """Analyze market trends using MCP"""
        result = self.client.call_tool("trend_analysis", {
            "industry": industry,
            "timeframe": timeframe,
            "include_predictions": True
        })
        
        if result:
            return self._format_trend_analysis(result)
        return "MCP market trend analysis not available. Using AI-generated analysis."
    
    def get_regulatory_info(self, industry: str, location: str) -> str:
        """Get regulatory information"""
        result = self.client.call_tool("regulatory_info", {
            "industry": industry,
            "location": location
        })
        
        if result:
            return self._format_regulatory_info(result)
        return "Regulatory information not available through MCP."
    
    def _format_trend_analysis(self, data: Dict[str, Any]) -> str:
        """Format trend analysis data"""
        output = "Market Trends Analysis:\n\n"
        
        trends = data.get("trends", [])
        for trend in trends:
            output += f"• {trend.get('name', 'Unknown')}: {trend.get('description', '')}\n"
            output += f"  Impact: {trend.get('impact', 'N/A')}\n\n"
        
        return output
    
    def _format_regulatory_info(self, data: Dict[str, Any]) -> str:
        """Format regulatory information"""
        output = "Regulatory Requirements:\n\n"
        
        requirements = data.get("requirements", [])
        for req in requirements:
            output += f"• {req.get('name', 'Unknown')}\n"
            output += f"  Description: {req.get('description', '')}\n"
            output += f"  Compliance Level: {req.get('level', 'N/A')}\n\n"
        
        return output

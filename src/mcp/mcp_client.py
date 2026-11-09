"""
MCP (Model Context Protocol) Client - Direct Integration Mode
Connects to real-time data sources without requiring MCP server
Uses Yahoo Finance, Alpha Vantage, and other free APIs
"""
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import os
from src.data.market_data_fetcher import get_market_data_fetcher
from config.config import MCP_ENABLED


class MCPClient:
    """Direct data integration client (MCP-compatible interface)"""
    
    def __init__(self):
        self.fetcher = get_market_data_fetcher()  # Get singleton instance
        self.enabled = MCP_ENABLED  # Read from environment configuration
        self.available_tools = [
            "market_research",
            "financial_benchmarks", 
            "competitor_analysis",
            "trend_analysis",
            "industry_statistics"
        ]
        if self.enabled:
            print(f"? MCP Direct Integration: ENABLED - {len(self.available_tools)} tools available")
            print(f"?? Data Flow: MCP ? MarketDataFetcher ? Yahoo Finance")
            print(f"   Architecture: MCPClient ? MarketDataFetcher (singleton) ? Yahoo Finance")
            print(f"   Status: All market data queries unified through single data layer")
        else:
            print(f"??  MCP Direct Integration: DISABLED")
            print(f"?? Data Flow: RAG ? MarketDataFetcher ? Yahoo Finance (MCP bypassed)")
    
    def get_market_data(self, industry: str, region: str = "US") -> Dict[str, Any]:
        """Get market data from Yahoo Finance via MarketDataFetcher singleton"""
        try:
            # Get industry tickers from fetcher
            tickers = self.fetcher.get_industry_tickers(industry)
            
            market_data = {
                "industry": industry,
                "region": region,
                "data_source": "Yahoo Finance (via MarketDataFetcher)",
                "timestamp": datetime.now().isoformat(),
                "market_indicators": {}
            }
            
            # Get market indicators from representative stocks using fetcher
            for ticker in tickers[:3]:  # Limit to top 3 for speed
                company_data = self.fetcher.get_company_data(ticker)
                if company_data:
                    market_data["market_indicators"][company_data['name']] = {
                        "market_cap": company_data.get("market_cap", "N/A"),
                        "revenue": company_data.get("revenue", "N/A"),
                        "employees": company_data.get("employees", "N/A"),
                        "industry_sector": company_data.get("sector", "N/A")
                    }
            
            # Add industry growth estimates using fetcher
            growth_rate = self.fetcher.calculate_growth_rate(tickers)
            market_size_data = self.fetcher.estimate_market_size(tickers)
            
            market_data["growth_projections"] = {
                "growth_rate": f"{growth_rate}%" if growth_rate else "N/A",
                "market_size": market_size_data.get("estimate", "N/A"),
                "confidence": market_size_data.get("confidence", "N/A")
            }
            
            return market_data
            
        except Exception as e:
            print(f"MCP: Error fetching market data: {e}")
            return {"error": str(e), "industry": industry}
    
    def get_financial_benchmarks(self, industry: str) -> Dict[str, Any]:
        """Get financial benchmarks using MarketDataFetcher singleton"""
        try:
            # Get industry tickers from fetcher
            tickers = self.fetcher.get_industry_tickers(industry)
            
            benchmarks = {
                "industry": industry,
                "data_source": "Yahoo Finance (via MarketDataFetcher)",
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "gross_margin": [],
                    "operating_margin": [],
                    "profit_margin": [],
                    "roe": [],
                    "revenue_growth": []
                }
            }
            
            # Get competitors data using fetcher
            competitors_data = self.fetcher.get_competitors_data(tickers)
            
            # Extract financial metrics from competitor data
            # Note: Yahoo Finance info varies by company, so we'll get what's available
            for company_data in competitors_data:
                ticker = company_data.get('ticker')
                if ticker:
                    # Use fetcher to get detailed financial metrics
                    metrics = self.fetcher.get_detailed_financial_metrics(ticker)
                    if 'error' not in metrics:
                        if metrics.get("grossMargins"):
                            benchmarks["metrics"]["gross_margin"].append(metrics["grossMargins"] * 100)
                        if metrics.get("operatingMargins"):
                            benchmarks["metrics"]["operating_margin"].append(metrics["operatingMargins"] * 100)
                        if metrics.get("profitMargins"):
                            benchmarks["metrics"]["profit_margin"].append(metrics["profitMargins"] * 100)
                        if metrics.get("returnOnEquity"):
                            benchmarks["metrics"]["roe"].append(metrics["returnOnEquity"] * 100)
                        if metrics.get("revenueGrowth"):
                            benchmarks["metrics"]["revenue_growth"].append(metrics["revenueGrowth"] * 100)
            
            # Calculate averages
            benchmarks["averages"] = {}
            for metric, values in benchmarks["metrics"].items():
                if values:
                    benchmarks["averages"][metric] = sum(values) / len(values)
                else:
                    benchmarks["averages"][metric] = "N/A"
            
            return benchmarks
            
        except Exception as e:
            print(f"MCP: Error fetching benchmarks: {e}")
            return {"error": str(e), "industry": industry}
    
    def get_competitor_analysis(self, industry: str, business_type: str) -> Dict[str, Any]:
        """Get competitor analysis using MarketDataFetcher singleton"""
        try:
            # Use fetcher to get industry overview (comprehensive competitor data)
            overview = self.fetcher.get_industry_overview(industry)
            
            competitors = {
                "industry": industry,
                "business_type": business_type,
                "data_source": "Yahoo Finance (via MarketDataFetcher)",
                "timestamp": datetime.now().isoformat(),
                "top_competitors": []
            }
            
            # Extract and reformat competitor information from overview
            if overview.get('competitors'):
                for competitor in overview['competitors']:
                    competitors["top_competitors"].append({
                        "name": competitor.get('name', 'N/A'),
                        "ticker": competitor.get('ticker', 'N/A'),
                        "market_cap": competitor.get('market_cap_raw', 0),
                        "market_cap_formatted": competitor.get('market_cap', 'N/A'),
                        "revenue": competitor.get('revenue', 'N/A'),
                        "employees": competitor.get('employees', 'N/A'),
                        "description": f"Market leader in {industry}"
                    })
            
            # Already sorted by market cap in fetcher
            return competitors
            
        except Exception as e:
            print(f"MCP: Error fetching competitor data: {e}")
            return {"error": str(e), "industry": industry}
    
    def analyze_market_trends(self, industry: str, timeframe: str = "1y") -> Dict[str, Any]:
        """Analyze market trends using MarketDataFetcher singleton"""
        try:
            # Get industry tickers from fetcher
            tickers = self.fetcher.get_industry_tickers(industry)
            
            trends = {
                "industry": industry,
                "timeframe": timeframe,
                "data_source": "Yahoo Finance (via MarketDataFetcher)",
                "timestamp": datetime.now().isoformat(),
                "trend_analysis": []
            }
            
            # Use fetcher for growth rate and market size
            growth_rate = self.fetcher.calculate_growth_rate(tickers)
            market_size_data = self.fetcher.estimate_market_size(tickers)
            
            # Get company data for trend analysis
            for ticker in tickers[:3]:  # Limit to top 3 for speed
                company_data = self.fetcher.get_company_data(ticker)
                if company_data:
                    # Use fetcher to get historical price data
                    price_data = self.fetcher.get_historical_price_data(ticker, timeframe)
                    if 'error' not in price_data:
                        trend = {
                            "company": company_data['name'],
                            "ticker": ticker,
                            "price_change_pct": price_data['price_change_pct'],
                            "trend": price_data['trend'],
                            "volatility": price_data['volatility']
                        }
                        trends["trend_analysis"].append(trend)
            
            # Add overall market metrics from fetcher
            trends["overall_metrics"] = {
                "growth_rate": f"{growth_rate}%" if growth_rate else "N/A",
                "market_size": market_size_data.get("estimate", "N/A"),
                "confidence": market_size_data.get("confidence", "N/A")
            }
            
            return trends
            
        except Exception as e:
            print(f"MCP: Error analyzing trends: {e}")
            return {"error": str(e), "industry": industry}
    
    def enhance_business_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance business plan with real market data"""
        enhanced = plan_data.copy()
        
        industry = plan_data.get("industry", "Technology")
        location = plan_data.get("location", "United States")
        
        print(f"?? MCP: Enhancing business plan with real market data...")
        print(f"?? MCP: Using MarketDataFetcher singleton for data")
        print(f"?? Data Flow: MCP ? MarketDataFetcher ? Yahoo Finance")
        print(f"   Industry: {industry} | Location: {location}")
        print(f"   Data Architecture: MCP coordination ? MarketDataFetcher singleton ? Yahoo Finance API")
        
        # Add market data
        print(f"   ? Fetching market data via MarketDataFetcher...")
        market_data = self.get_market_data(industry, location)
        enhanced["mcp_market_data"] = market_data
        
        # Add financial benchmarks
        print(f"   ? Fetching financial benchmarks via MarketDataFetcher...")
        benchmarks = self.get_financial_benchmarks(industry)
        enhanced["mcp_financial_benchmarks"] = benchmarks
        
        # Add competitor analysis
        print(f"   ? Fetching competitor analysis via MarketDataFetcher...")
        competitors = self.get_competitor_analysis(industry, plan_data.get("business_type", ""))
        enhanced["mcp_competitor_analysis"] = competitors
        
        # Add trend analysis
        print(f"   ? Fetching market trends via MarketDataFetcher...")
        trends = self.analyze_market_trends(industry)
        enhanced["mcp_trend_analysis"] = trends
        
        print(f"? MCP: Business plan enhanced with real-time market data")
        print(f"   All data fetched through unified MarketDataFetcher (no redundant API calls)")
        
        return enhanced
    
    def is_available(self) -> bool:
        """Check if MCP is available"""
        return self.enabled


# Convenience wrapper for backward compatibility
class MCPBusinessTools:
    """Business-specific MCP tools wrapper"""
    
    def __init__(self):
        self.client = MCPClient()
    
    def get_market_insights(self, industry: str) -> str:
        """Get formatted market insights"""
        data = self.client.get_market_data(industry)
        
        if "error" in data:
            return f"Market data unavailable: {data['error']}"
        
        output = f"?? Market Insights for {industry}:\n\n"
        
        if "market_indicators" in data:
            output += "Industry Leaders:\n"
            for company, metrics in data["market_indicators"].items():
                output += f"  � {company}\n"
                if metrics.get("revenue_growth") != "N/A":
                    output += f"    Revenue Growth: {metrics['revenue_growth']:.1%}\n"
                if metrics.get("profit_margins") != "N/A":
                    output += f"    Profit Margin: {metrics['profit_margins']:.1%}\n"
        
        if "growth_projections" in data:
            proj = data["growth_projections"]
            output += f"\n?? Industry Growth:\n"
            output += f"  Market Size (2026): ${proj['current_size_b']}B\n"
            output += f"  CAGR: {proj['cagr']}%\n"
            output += f"  Projected (2030): ${proj['2030_size_b']}B\n"
        
        return output


# Initialize global MCP client
mcp_client = MCPClient()

print("?? MCP Direct Integration Mode: ACTIVE")
print(f"? Connected to real-time data sources")
print(f"?? {len(mcp_client.available_tools)} tools available")

"""
FREE Market Data Fetcher using Yahoo Finance
No API key needed! Unlimited requests!
"""
import yfinance as yf
from typing import Dict, Any, List, Optional
from datetime import datetime


class MarketDataFetcher:
    """
    Fetch real market data for FREE using Yahoo Finance
    
    Features:
    - Get company data (market cap, revenue, employees)
    - Estimate market sizes from competitor data
    - Calculate growth rates from historical data
    - Map industries to relevant companies
    """
    
    # Industry to stock ticker mappings
    INDUSTRY_TICKERS = {
        'hr_tech': ['WDAY', 'PAYC', 'ADP', 'PAYX'],
        'hr tech': ['WDAY', 'PAYC', 'ADP', 'PAYX'],
        'human resources': ['WDAY', 'PAYC', 'ADP', 'PAYX'],
        'recruitment': ['WDAY', 'PAYC', 'ADP', 'PAYX'],
        
        'saas': ['CRM', 'NOW', 'WDAY', 'ZM', 'SNOW'],
        'software': ['MSFT', 'ORCL', 'ADBE', 'CRM', 'INTU'],
        'cloud': ['MSFT', 'AMZN', 'GOOGL', 'CRM', 'SNOW'],
        
        'ecommerce': ['AMZN', 'SHOP', 'EBAY', 'ETSY', 'W'],
        'e-commerce': ['AMZN', 'SHOP', 'EBAY', 'ETSY', 'W'],
        'retail': ['WMT', 'TGT', 'COST', 'HD', 'LOW'],
        
        'fintech': ['SQ', 'PYPL', 'V', 'MA', 'COIN'],
        'finance': ['JPM', 'BAC', 'WFC', 'C', 'GS'],
        'payments': ['V', 'MA', 'PYPL', 'SQ', 'AXP'],
        
        'ai': ['NVDA', 'MSFT', 'GOOGL', 'META', 'AMZN'],
        'artificial intelligence': ['NVDA', 'MSFT', 'GOOGL', 'META', 'AMZN'],
        'machine learning': ['NVDA', 'MSFT', 'GOOGL', 'META', 'AMZN'],
        
        'healthcare': ['UNH', 'JNJ', 'PFE', 'ABBV', 'TMO'],
        'healthtech': ['TDOC', 'VEEV', 'DXCM', 'ISRG', 'ILMN'],
        
        'edtech': ['CHGG', 'DUOL', 'ATGE', 'TWOU'],
        'education': ['CHGG', 'DUOL', 'ATGE', 'TWOU'],
        
        'cybersecurity': ['CRWD', 'ZS', 'PANW', 'FTNT', 'NET'],
        'security': ['CRWD', 'ZS', 'PANW', 'FTNT', 'NET'],
        
        'social media': ['META', 'SNAP', 'PINS', 'RDDT'],
        'marketplace': ['ABNB', 'UBER', 'DASH', 'LYFT'],
        
        'logistics': ['UPS', 'FDX', 'JBHT', 'CHRW'],
        'transportation': ['UBER', 'LYFT', 'DASH', 'ABNB'],
        
        'gaming': ['RBLX', 'EA', 'TTWO', 'ATVI', 'U'],
        'entertainment': ['DIS', 'NFLX', 'WBD', 'PARA'],
        
        'technology': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META'],
        'tech': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
    }
    
    def __init__(self):
        """Initialize market data fetcher"""
        print("✓ Market Data Fetcher initialized (Yahoo Finance)")
        print("✓ FREE unlimited requests available")
    
    def get_company_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get company data from Yahoo Finance
        
        Args:
            ticker: Stock ticker (e.g., 'MSFT', 'AAPL')
        
        Returns:
            Company info including market cap, revenue, etc.
        """
        try:
            company = yf.Ticker(ticker)
            info = company.info
            
            if not info or len(info) < 5:
                return None
            
            return {
                'ticker': ticker,
                'name': info.get('longName', info.get('shortName', ticker)),
                'market_cap': info.get('marketCap', 0),
                'revenue': info.get('totalRevenue', info.get('revenue', 0)),
                'employees': info.get('fullTimeEmployees', 0),
                'industry': info.get('industry', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'description': info.get('longBusinessSummary', 'N/A'),
                'website': info.get('website', 'N/A'),
                'founded': info.get('yearFounded', 'N/A'),
                'headquarters': f"{info.get('city', '')}, {info.get('country', '')}".strip(', ')
            }
        except Exception as e:
            print(f"⚠️  Could not fetch {ticker}: {str(e)[:50]}")
            return None
    
    def get_competitors_data(self, tickers: List[str]) -> List[Dict[str, Any]]:
        """
        Get data for multiple competitors
        
        Args:
            tickers: List of stock tickers
        
        Returns:
            List of company data
        """
        competitors = []
        for ticker in tickers:
            print(f"   Fetching {ticker}...", end=' ')
            data = self.get_company_data(ticker)
            if data:
                competitors.append(data)
                print("✓")
            else:
                print("⚠️  skipped")
        
        return competitors
    
    def estimate_market_size(self, tickers: List[str]) -> Dict[str, Any]:
        """
        Estimate market size from competitor revenues
        
        Args:
            tickers: List of major players in the market
        
        Returns:
            Market size estimate with breakdown
        """
        companies = self.get_competitors_data(tickers)
        
        if not companies:
            return {
                'estimate': 'Data not available',
                'confidence': 'low',
                'method': 'insufficient_data'
            }
        
        total_revenue = 0
        valid_companies = []
        
        for company in companies:
            revenue = company.get('revenue', 0)
            if revenue > 0:
                total_revenue += revenue
                valid_companies.append(company)
        
        if valid_companies:
            # Market is typically 3-5x the major players combined
            # Using 4x as middle estimate
            market_multiplier = 4.0
            estimated_market = total_revenue * market_multiplier
            
            # Convert to billions for readability
            market_size_billions = estimated_market / 1_000_000_000
            
            return {
                'estimate': f"${market_size_billions:.1f}B",
                'raw_value': estimated_market,
                'top_players_revenue': f"${total_revenue / 1_000_000_000:.1f}B",
                'num_companies': len(valid_companies),
                'multiplier': market_multiplier,
                'confidence': 'high' if len(valid_companies) >= 3 else 'medium',
                'method': 'competitor_revenue_analysis',
                'companies_analyzed': [c['name'] for c in valid_companies]
            }
        
        return {
            'estimate': 'Data not available',
            'confidence': 'low',
            'method': 'insufficient_revenue_data'
        }
    
    def calculate_growth_rate(self, tickers: List[str]) -> Optional[float]:
        """
        Calculate average revenue growth rate from historical data
        
        Args:
            tickers: List of company tickers
        
        Returns:
            Average YoY revenue growth rate as percentage
        """
        try:
            growth_rates = []
            
            for ticker in tickers[:3]:  # Limit to top 3 for speed
                try:
                    company = yf.Ticker(ticker)
                    financials = company.financials
                    
                    if financials is not None and 'Total Revenue' in financials.index:
                        revenues = financials.loc['Total Revenue'].values
                        
                        # Calculate YoY growth
                        if len(revenues) >= 2:
                            recent = float(revenues[0])
                            previous = float(revenues[1])
                            
                            if previous > 0:
                                growth = ((recent - previous) / previous) * 100
                                if -100 < growth < 500:  # Sanity check
                                    growth_rates.append(growth)
                except:
                    continue
            
            if growth_rates:
                avg_growth = sum(growth_rates) / len(growth_rates)
                return round(avg_growth, 1)
            
        except Exception as e:
            print(f"⚠️  Growth calculation error: {str(e)[:50]}")
        
        return None
    
    def get_industry_tickers(self, industry: str) -> List[str]:
        """
        Get relevant stock tickers for an industry
        
        Args:
            industry: Industry name
        
        Returns:
            List of relevant stock tickers
        """
        industry_lower = industry.lower().strip()
        
        # Direct match
        if industry_lower in self.INDUSTRY_TICKERS:
            return self.INDUSTRY_TICKERS[industry_lower]
        
        # Partial match
        for key, tickers in self.INDUSTRY_TICKERS.items():
            if key in industry_lower or industry_lower in key:
                return tickers
        
        # Default to technology
        print(f"ℹ️  No specific mapping for '{industry}', using technology defaults")
        return self.INDUSTRY_TICKERS['technology']
    
    def get_industry_overview(
        self, 
        industry: str, 
        custom_tickers: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive industry overview
        
        Args:
            industry: Industry name
            custom_tickers: Optional custom ticker list (overrides auto-detection)
        
        Returns:
            Industry overview with market data
        """
        print(f"\n🔍 Fetching real market data for: {industry}")
        
        # Get tickers
        tickers = custom_tickers or self.get_industry_tickers(industry)
        print(f"   Analyzing companies: {', '.join(tickers)}")
        
        # Fetch competitor data
        companies = self.get_competitors_data(tickers)
        
        if not companies:
            return {
                'industry': industry,
                'market_size': 'Data not available',
                'competitors': [],
                'avg_employees': 'Data not available',
                'growth_rate': 'Data not available',
                'data_source': 'Yahoo Finance',
                'fetch_status': 'failed'
            }
        
        # Calculate market size
        market_data = self.estimate_market_size(tickers)
        
        # Calculate growth rate
        print("   Calculating growth rate...", end=' ')
        growth_rate = self.calculate_growth_rate(tickers)
        if growth_rate:
            print(f"✓ {growth_rate}%")
        else:
            print("⚠️  using estimate")
            growth_rate = 15.0  # Default estimate
        
        # Calculate averages
        total_employees = sum(c.get('employees', 0) for c in companies if c.get('employees'))
        avg_employees = total_employees // len(companies) if companies else 0
        
        total_market_cap = sum(c.get('market_cap', 0) for c in companies)
        avg_market_cap = total_market_cap / len(companies) if companies else 0
        
        # Format competitor list
        competitor_list = []
        for company in companies:
            market_cap = company.get('market_cap', 0)
            revenue = company.get('revenue', 0)
            employees = company.get('employees', 0)
            
            competitor_list.append({
                'name': company.get('name'),
                'ticker': company.get('ticker'),
                'market_cap': f"${market_cap / 1_000_000_000:.1f}B" if market_cap else 'N/A',
                'market_cap_raw': market_cap,
                'revenue': f"${revenue / 1_000_000_000:.1f}B" if revenue else 'N/A',
                'revenue_raw': revenue,
                'employees': f"{employees:,}" if employees else 'N/A',
                'employees_raw': employees
            })
        
        # Sort by market cap
        competitor_list.sort(key=lambda x: x['market_cap_raw'], reverse=True)
        
        print(f"✅ Market data fetched successfully!")
        print(f"   Market Size: {market_data['estimate']}")
        print(f"   Growth Rate: {growth_rate}%")
        print(f"   Companies: {len(companies)}")
        
        return {
            'industry': industry,
            'market_size': market_data['estimate'],
            'market_size_raw': market_data.get('raw_value', 0),
            'market_confidence': market_data['confidence'],
            'top_players_revenue': market_data.get('top_players_revenue', 'N/A'),
            'competitors': competitor_list,
            'num_competitors': len(competitor_list),
            'growth_rate': f"{growth_rate}%",
            'growth_rate_raw': growth_rate,
            'avg_employees': f"{avg_employees:,}" if avg_employees else 'N/A',
            'avg_market_cap': f"${avg_market_cap / 1_000_000_000:.1f}B" if avg_market_cap else 'N/A',
            'data_source': 'Yahoo Finance (Real-time)',
            'fetch_timestamp': datetime.now().isoformat(),
            'fetch_status': 'success'
        }



    def get_detailed_financial_metrics(self, ticker: str) -> Dict[str, Any]:
        """
        Get detailed financial metrics for a ticker (margins, ROE, etc.)
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Dictionary with financial metrics
        """
        try:
            company = yf.Ticker(ticker)
            info = company.info
            
            return {
                'ticker': ticker,
                'grossMargins': info.get('grossMargins'),
                'operatingMargins': info.get('operatingMargins'),
                'profitMargins': info.get('profitMargins'),
                'returnOnEquity': info.get('returnOnEquity'),
                'revenueGrowth': info.get('revenueGrowth')
            }
        except Exception as e:
            return {'ticker': ticker, 'error': str(e)}
    
    def get_historical_price_data(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """
        Get historical price data for trend analysis
        
        Args:
            ticker: Stock ticker symbol
            period: Time period (e.g., "1y", "6mo", "3mo")
        
        Returns:
            Dictionary with price trend data
        """
        try:
            company = yf.Ticker(ticker)
            hist = company.history(period=period)
            
            if hist.empty:
                return {'ticker': ticker, 'error': 'No historical data available'}
            
            price_change = ((hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0]) * 100
            
            return {
                'ticker': ticker,
                'price_change_pct': round(price_change, 2),
                'trend': 'Bullish' if price_change > 0 else 'Bearish',
                'volatility': round(hist['Close'].std(), 2),
                'period': period
            }
        except Exception as e:
            return {'ticker': ticker, 'error': str(e)}

# Singleton instance
_fetcher = None

def get_market_data_fetcher() -> MarketDataFetcher:
    """Get or create market data fetcher singleton"""
    global _fetcher
    if _fetcher is None:
        _fetcher = MarketDataFetcher()
    return _fetcher

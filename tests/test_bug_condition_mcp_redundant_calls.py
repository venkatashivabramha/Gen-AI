"""
Bug Condition Exploration Test for MCP Redundant Yahoo Finance API Calls

This test explores the bug condition where MCPClient makes redundant Yahoo Finance API calls
by using yf.Ticker() directly instead of leveraging the existing MarketDataFetcher singleton.

**CRITICAL**: This test MUST FAIL on unfixed code.
Test failure confirms the bug exists and demonstrates redundant API architecture.

**EXPECTED BEHAVIOR (encoded in this test)**:
- MCPClient should import and use get_market_data_fetcher() singleton
- MCPClient should delegate all market data fetching to MarketDataFetcher
- NO direct yf.Ticker() calls should exist in MCPClient method implementations
- MCPClient methods should call self.fetcher methods

**AFTER FIX**: This same test will PASS when MCPClient is refactored to use MarketDataFetcher,
confirming the expected behavior is satisfied.

**Validates: Requirements 2.2, 2.4**
"""

import pytest
import sys
import os
import ast
import inspect

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mcp.mcp_client import MCPClient
from src.data.market_data_fetcher import get_market_data_fetcher


class TestBugConditionExploration:
    """
    Bug Condition Exploration Tests
    
    These tests encode the EXPECTED behavior: MCPClient delegates to MarketDataFetcher.
    On UNFIXED code, these tests will FAIL, demonstrating the bug exists and documenting
    the counterexamples (direct yf.Ticker() calls, missing import, etc.).
    """
    
    def test_mcp_imports_market_data_fetcher(self):
        """
        Property 1: Bug Condition - MCPClient Imports MarketDataFetcher
        
        Test that MCPClient imports get_market_data_fetcher from src.data.market_data_fetcher.
        
        EXPECTED ON UNFIXED CODE:
        - FAILS: MCPClient source does not contain the import statement
        - COUNTEREXAMPLE: No 'from src.data.market_data_fetcher import get_market_data_fetcher'
        
        EXPECTED ON FIXED CODE:
        - PASSES: Import statement found in MCPClient source
        """
        # Get the source file path
        mcp_client_file = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'src', 
            'mcp', 
            'mcp_client.py'
        )
        
        # Read source code
        with open(mcp_client_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Check for import statement
        import_found = (
            'from src.data.market_data_fetcher import get_market_data_fetcher' in source_code or
            'from src.data.market_data_fetcher import MarketDataFetcher' in source_code
        )
        
        if not import_found:
            print("\n✗ MCPClient does NOT import get_market_data_fetcher (bug confirmed)")
            print("  - COUNTEREXAMPLE: Missing import statement")
            print("  - Expected: 'from src.data.market_data_fetcher import get_market_data_fetcher'")
            print("  - Actual: Import statement not found in source")
        
        assert import_found, (
            "MCPClient should import get_market_data_fetcher from src.data.market_data_fetcher. "
            "COUNTEREXAMPLE: Import statement missing in unfixed code."
        )
        
        print("\n✓ MCPClient imports get_market_data_fetcher")
    
    def test_mcp_initializes_fetcher_singleton(self):
        """
        Property 1: Bug Condition - MCPClient Initializes Fetcher Singleton
        
        Test that MCPClient.__init__ stores a reference to the MarketDataFetcher singleton.
        
        EXPECTED ON UNFIXED CODE:
        - FAILS: MCPClient instance has no 'fetcher' attribute
        - COUNTEREXAMPLE: self.fetcher is not initialized in __init__
        
        EXPECTED ON FIXED CODE:
        - PASSES: MCPClient.fetcher references the singleton
        """
        client = MCPClient()
        
        has_fetcher = hasattr(client, 'fetcher')
        
        if not has_fetcher:
            print("\n✗ MCPClient does NOT have 'fetcher' attribute (bug confirmed)")
            print("  - COUNTEREXAMPLE: self.fetcher not initialized")
            print("  - Expected: self.fetcher = get_market_data_fetcher()")
            print(f"  - Actual attributes: {[a for a in dir(client) if not a.startswith('_')]}")
        
        assert has_fetcher, (
            "MCPClient should have 'fetcher' attribute initialized in __init__. "
            "COUNTEREXAMPLE: self.fetcher not found in unfixed code."
        )
        
        # Verify it's the correct singleton
        fetcher = client.fetcher
        singleton = get_market_data_fetcher()
        
        is_singleton = fetcher is singleton
        
        if not is_singleton:
            print("\n✗ MCPClient.fetcher is NOT the singleton (bug confirmed)")
            print("  - COUNTEREXAMPLE: Different fetcher instance")
            print(f"  - client.fetcher: {type(fetcher)}")
            print(f"  - singleton: {type(singleton)}")
        
        assert is_singleton, (
            "MCPClient.fetcher should be the MarketDataFetcher singleton. "
            "COUNTEREXAMPLE: Different instance in unfixed code."
        )
        
        print("\n✓ MCPClient initializes fetcher singleton correctly")
        print(f"  - Fetcher type: {type(fetcher)}")
        print(f"  - Is singleton: {is_singleton}")
    
    def test_mcp_methods_no_direct_yf_calls(self):
        """
        Property 1: Bug Condition - MCPClient Methods Do NOT Use Direct yf.Ticker() Calls
        
        Test that MCPClient methods delegate to MarketDataFetcher instead of calling yf.Ticker() directly.
        
        EXPECTED ON UNFIXED CODE:
        - FAILS: Multiple direct yf.Ticker() calls found in method implementations
        - COUNTEREXAMPLE: Methods contain 'yf.Ticker(' in their source code
        
        EXPECTED ON FIXED CODE:
        - PASSES: No direct yf.Ticker() calls, all delegation to self.fetcher
        """
        # Get the source file path
        mcp_client_file = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'src', 
            'mcp', 
            'mcp_client.py'
        )
        
        # Read and parse source code
        with open(mcp_client_file, 'r', encoding='utf-8-sig') as f:
            source_code = f.read()
        
        # Parse AST to find methods
        tree = ast.parse(source_code)
        
        # Methods to check
        target_methods = [
            'get_market_data',
            'get_financial_benchmarks',
            'get_competitor_analysis',
            'analyze_market_trends'
        ]
        
        counterexamples = []
        
        # Find MCPClient class
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'MCPClient':
                for method_node in node.body:
                    if isinstance(method_node, ast.FunctionDef) and method_node.name in target_methods:
                        # Get method source
                        method_source = ast.get_source_segment(source_code, method_node)
                        
                        # Check for direct yf.Ticker() calls
                        if method_source and 'yf.Ticker(' in method_source:
                            counterexamples.append({
                                'method': method_node.name,
                                'has_direct_call': True,
                                'source_snippet': method_source[:200] + '...'
                            })
                            print(f"\n✗ {method_node.name}() contains direct yf.Ticker() call (bug confirmed)")
                        
                        # Check for self.fetcher usage
                        uses_fetcher = method_source and 'self.fetcher' in method_source
                        if not uses_fetcher:
                            print(f"\n✗ {method_node.name}() does NOT use self.fetcher (bug confirmed)")
        
        if counterexamples:
            print("\n" + "=" * 80)
            print("COUNTEREXAMPLES FOUND:")
            for ce in counterexamples:
                print(f"\n  Method: {ce['method']}")
                print(f"  Has direct yf.Ticker(): {ce['has_direct_call']}")
                print(f"  Source preview: {ce['source_snippet'][:150]}...")
            print("=" * 80)
        
        assert len(counterexamples) == 0, (
            f"MCPClient methods should NOT use direct yf.Ticker() calls. "
            f"COUNTEREXAMPLES: {len(counterexamples)} methods with direct calls found in unfixed code. "
            f"Methods: {[ce['method'] for ce in counterexamples]}"
        )
        
        print("\n✓ MCPClient methods delegate to self.fetcher (no direct yf.Ticker() calls)")
    
    def test_mcp_get_market_data_delegates_to_fetcher(self):
        """
        Property 1: Bug Condition - get_market_data() Delegates to Fetcher
        
        Test that get_market_data() uses self.fetcher methods.
        
        EXPECTED ON UNFIXED CODE:
        - FAILS: Method makes direct yf.Ticker() calls
        - COUNTEREXAMPLE: No self.fetcher method calls found
        
        EXPECTED ON FIXED CODE:
        - PASSES: Method calls self.fetcher.get_industry_tickers(), etc.
        """
        # Get method source
        method = MCPClient.get_market_data
        source = inspect.getsource(method)
        
        # Check for delegation to fetcher
        uses_fetcher = 'self.fetcher' in source
        has_direct_yf = 'yf.Ticker(' in source
        
        if not uses_fetcher:
            print("\n✗ get_market_data() does NOT use self.fetcher (bug confirmed)")
            print("  - COUNTEREXAMPLE: No self.fetcher method calls")
            print("  - Expected: self.fetcher.get_industry_tickers()")
        
        if has_direct_yf:
            print("\n✗ get_market_data() has direct yf.Ticker() call (bug confirmed)")
            print("  - COUNTEREXAMPLE: Direct Yahoo Finance API call")
            print("  - Should use: self.fetcher methods")
        
        assert uses_fetcher and not has_direct_yf, (
            "get_market_data() should delegate to self.fetcher, not make direct yf.Ticker() calls. "
            "COUNTEREXAMPLE: Direct calls found in unfixed code."
        )
        
        print("\n✓ get_market_data() delegates to self.fetcher")
    
    def test_mcp_get_financial_benchmarks_delegates_to_fetcher(self):
        """
        Property 1: Bug Condition - get_financial_benchmarks() Delegates to Fetcher
        
        EXPECTED ON UNFIXED CODE:
        - FAILS: Method makes direct yf.Ticker() calls
        
        EXPECTED ON FIXED CODE:
        - PASSES: Method calls self.fetcher.get_competitors_data()
        """
        method = MCPClient.get_financial_benchmarks
        source = inspect.getsource(method)
        
        uses_fetcher = 'self.fetcher' in source
        has_direct_yf = 'yf.Ticker(' in source
        
        if not uses_fetcher:
            print("\n✗ get_financial_benchmarks() does NOT use self.fetcher (bug confirmed)")
        
        if has_direct_yf:
            print("\n✗ get_financial_benchmarks() has direct yf.Ticker() call (bug confirmed)")
        
        assert uses_fetcher and not has_direct_yf, (
            "get_financial_benchmarks() should delegate to self.fetcher. "
            "COUNTEREXAMPLE: Direct calls found in unfixed code."
        )
        
        print("\n✓ get_financial_benchmarks() delegates to self.fetcher")
    
    def test_mcp_get_competitor_analysis_delegates_to_fetcher(self):
        """
        Property 1: Bug Condition - get_competitor_analysis() Delegates to Fetcher
        
        EXPECTED ON UNFIXED CODE:
        - FAILS: Method makes direct yf.Ticker() calls
        
        EXPECTED ON FIXED CODE:
        - PASSES: Method calls self.fetcher.get_industry_overview()
        """
        method = MCPClient.get_competitor_analysis
        source = inspect.getsource(method)
        
        uses_fetcher = 'self.fetcher' in source
        has_direct_yf = 'yf.Ticker(' in source
        
        if not uses_fetcher:
            print("\n✗ get_competitor_analysis() does NOT use self.fetcher (bug confirmed)")
        
        if has_direct_yf:
            print("\n✗ get_competitor_analysis() has direct yf.Ticker() call (bug confirmed)")
        
        assert uses_fetcher and not has_direct_yf, (
            "get_competitor_analysis() should delegate to self.fetcher. "
            "COUNTEREXAMPLE: Direct calls found in unfixed code."
        )
        
        print("\n✓ get_competitor_analysis() delegates to self.fetcher")
    
    def test_mcp_analyze_market_trends_delegates_to_fetcher(self):
        """
        Property 1: Bug Condition - analyze_market_trends() Delegates to Fetcher
        
        EXPECTED ON UNFIXED CODE:
        - FAILS: Method makes direct yf.Ticker() calls
        
        EXPECTED ON FIXED CODE:
        - PASSES: Method calls self.fetcher methods
        """
        method = MCPClient.analyze_market_trends
        source = inspect.getsource(method)
        
        uses_fetcher = 'self.fetcher' in source
        has_direct_yf = 'yf.Ticker(' in source
        
        if not uses_fetcher:
            print("\n✗ analyze_market_trends() does NOT use self.fetcher (bug confirmed)")
        
        if has_direct_yf:
            print("\n✗ analyze_market_trends() has direct yf.Ticker() call (bug confirmed)")
        
        assert uses_fetcher and not has_direct_yf, (
            "analyze_market_trends() should delegate to self.fetcher. "
            "COUNTEREXAMPLE: Direct calls found in unfixed code."
        )
        
        print("\n✓ analyze_market_trends() delegates to self.fetcher")
    
    def test_mcp_enhance_business_plan_shows_data_flow(self):
        """
        Property 1: Bug Condition - enhance_business_plan() Shows Clear Data Flow
        
        Test that enhance_business_plan() logs the data flow through MCP → MarketDataFetcher.
        
        EXPECTED ON UNFIXED CODE:
        - MAY FAIL: No logging about MarketDataFetcher delegation
        
        EXPECTED ON FIXED CODE:
        - PASSES: Clear logging shows "MCP → MarketDataFetcher → Yahoo Finance"
        """
        method = MCPClient.enhance_business_plan
        source = inspect.getsource(method)
        
        has_data_flow_logging = (
            'MarketDataFetcher' in source or
            'Data Flow:' in source or
            'fetcher' in source.lower()
        )
        
        if not has_data_flow_logging:
            print("\n⚠️  enhance_business_plan() lacks clear data flow logging")
            print("  - Suggestion: Add logging showing MCP → MarketDataFetcher path")
        
        # This is more of a suggestion than a hard requirement
        # but good to document
        print("\n✓ Checked enhance_business_plan() for data flow transparency")


class TestArchitectureValidation:
    """
    Validate the architectural expectations
    """
    
    def test_market_data_fetcher_singleton_exists(self):
        """
        Verify MarketDataFetcher singleton is available
        """
        fetcher = get_market_data_fetcher()
        assert fetcher is not None, "MarketDataFetcher singleton should exist"
        
        # Verify it's truly a singleton
        fetcher2 = get_market_data_fetcher()
        assert fetcher is fetcher2, "get_market_data_fetcher() should return same instance"
        
        print("\n✓ MarketDataFetcher singleton verified")
        print(f"  - Type: {type(fetcher)}")
        print(f"  - Is singleton: {fetcher is fetcher2}")
    
    def test_market_data_fetcher_has_required_methods(self):
        """
        Verify MarketDataFetcher has all required methods for MCPClient to use
        """
        fetcher = get_market_data_fetcher()
        
        required_methods = [
            'get_industry_tickers',
            'get_company_data',
            'get_competitors_data',
            'get_industry_overview',
            'calculate_growth_rate',
            'estimate_market_size'
        ]
        
        for method_name in required_methods:
            assert hasattr(fetcher, method_name), (
                f"MarketDataFetcher should have {method_name}() method"
            )
        
        print("\n✓ MarketDataFetcher has all required methods")
        print(f"  - Methods: {', '.join(required_methods)}")


if __name__ == "__main__":
    """
    Run tests directly with verbose output to see counterexamples
    """
    print("=" * 80)
    print("Bug Condition Exploration Test")
    print("Testing MCPClient Redundant Yahoo Finance API Calls")
    print("=" * 80)
    print("\nThis test SHOULD FAIL on unfixed code.")
    print("Failure confirms the bug exists and documents counterexamples.")
    print("=" * 80)
    
    pytest.main([__file__, "-v", "-s"])

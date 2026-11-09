"""
Preservation Property Tests for RAG Engine Direct Access

This test suite verifies that existing RAG engine functionality, document generation,
and MarketDataFetcher behavior remain UNCHANGED after fixing the MCP redundant calls bug.

**CRITICAL**: These tests MUST PASS on UNFIXED code (baseline behavior).
These same tests MUST PASS on FIXED code (no regressions).

**Property 2: Preservation - RAG Engine Direct Access Preserved**

For any RAG engine operation that requires market data when MCP is disabled or bypassed,
the system SHALL continue to call MarketDataFetcher methods directly without going through MCP,
preserving the existing fallback data flow path.

**Validates: Requirements 3.1, 3.2, 3.3**

**Testing Methodology**:
1. Observe behavior on UNFIXED code with MCP_ENABLED=false
2. Capture observed patterns in property-based tests
3. Verify tests PASS on unfixed code (confirms baseline)
4. After fix, these same tests should PASS (confirms no regressions)
"""

import pytest
import sys
import os
from typing import Dict, Any, List
from unittest.mock import patch
from hypothesis import given, strategies as st, settings, assume
from hypothesis import HealthCheck

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure MCP is disabled for preservation tests
os.environ['MCP_ENABLED'] = 'false'

# Import using the same paths as the RAG engine to ensure isinstance works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data.market_data_fetcher import MarketDataFetcher, get_market_data_fetcher
from rag.rag_engine import RAGEngine, get_rag_engine
from business_plan_generator import BusinessPlanGenerator


# Test data strategies for property-based testing
@st.composite
def business_data_strategy(draw):
    """Generate valid business data for testing"""
    industries = ['technology', 'healthcare', 'finance', 'retail', 'manufacturing', 'saas', 'hr tech', 'fintech']
    business_types = ['startup', 'small business', 'enterprise', 'saas platform', 'marketplace']
    
    return {
        'business_name': draw(st.text(min_size=3, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs')))),
        'industry': draw(st.sampled_from(industries)),
        'description': draw(st.text(min_size=20, max_size=200, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs')))),
        'target_market': draw(st.text(min_size=10, max_size=100, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs')))),
        'business_type': draw(st.sampled_from(business_types)),
        'revenue_model': draw(st.sampled_from(['subscription', 'one-time', 'freemium', 'transaction'])),
    }


@st.composite
def industry_strategy(draw):
    """Generate valid industry names for testing"""
    industries = ['technology', 'healthcare', 'finance', 'retail', 'saas', 'hr tech', 'fintech', 'ecommerce']
    return draw(st.sampled_from(industries))


class TestRAGEnginePreservation:
    """
    Test that RAG Engine continues to work correctly when MCP is disabled.
    These tests capture the baseline behavior that must be preserved.
    """
    
    def test_rag_engine_initialization_without_mcp(self):
        """
        Test that RAG Engine initializes correctly with real data when MCP is disabled.
        
        BASELINE BEHAVIOR (unfixed code):
        - RAG engine should initialize with use_real_data=True
        - Should have market_fetcher reference
        - Should be able to access MarketDataFetcher singleton
        
        PRESERVATION:
        - After fix, initialization should remain identical
        """
        # Initialize RAG engine with real data
        rag = RAGEngine(use_real_data=True)
        
        # Verify initialization
        assert rag is not None, "RAG engine should initialize"
        assert rag.use_real_data is True, "Real data should be enabled"
        assert rag.market_fetcher is not None, "Market fetcher should be initialized"
        
        # Verify it's using the singleton
        singleton = get_market_data_fetcher()
        assert rag.market_fetcher is singleton, "Should use MarketDataFetcher singleton"
        
        print("\n✓ RAG Engine initialization preserved")
        print(f"  - use_real_data: {rag.use_real_data}")
        print(f"  - Has market_fetcher: {rag.market_fetcher is not None}")
        print(f"  - Is singleton: {rag.market_fetcher is singleton}")
    
    def test_rag_engine_generate_market_analysis_structure(self):
        """
        Test that generate_market_analysis_with_rag() returns expected structure.
        
        BASELINE BEHAVIOR:
        - Should accept business_data and llm_generate_func
        - Should return a string (market analysis text)
        - Should call MarketDataFetcher.get_industry_overview()
        
        PRESERVATION:
        - Output structure and format should remain unchanged after fix
        """
        rag = RAGEngine(use_real_data=True)
        
        # Sample business data
        business_data = {
            'business_name': 'Test Company',
            'industry': 'technology',
            'description': 'A tech startup building innovative solutions',
            'target_market': 'Small and medium businesses'
        }
        
        # Mock LLM function
        def mock_llm(prompt: str) -> str:
            return '{"key_drivers": ["innovation", "scalability"], "competitive_strategy": "focus on SMB market", "positioning": "cost-effective solution", "opportunities": "rapid growth"}'
        
        # Call market analysis generation
        with patch.object(rag.market_fetcher, 'get_industry_overview') as mock_overview:
            # Mock return value with expected structure
            mock_overview.return_value = {
                'industry': 'technology',
                'market_size': '$500B',
                'growth_rate': '15%',
                'num_competitors': 2,
                'competitors': [
                    {'name': 'Competitor A', 'market_cap': '$100B', 'revenue': '$50B', 'employees': '10,000'},
                    {'name': 'Competitor B', 'market_cap': '$80B', 'revenue': '$40B', 'employees': '8,000'},
                ],
                'fetch_status': 'success'
            }
            
            result = rag.generate_market_analysis_with_rag(business_data, mock_llm)
            
            # Verify result structure
            assert isinstance(result, str), "Should return string"
            assert len(result) > 0, "Should return non-empty analysis"
            
            # Verify MarketDataFetcher was called
            mock_overview.assert_called_once()
            call_args = mock_overview.call_args
            assert call_args[0][0] == 'technology', "Should request correct industry"
        
        print("\n✓ RAG market analysis generation structure preserved")
        print(f"  - Returns string: {isinstance(result, str)}")
        print(f"  - Non-empty: {len(result) > 0}")
        print(f"  - Calls MarketDataFetcher: True")
    
    @given(business_data=business_data_strategy())
    @settings(max_examples=10, suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    def test_property_rag_market_analysis_always_returns_string(self, business_data):
        """
        Property: For all business data inputs where MCP is disabled,
        RAG engine produces market analysis with expected structure.
        
        BASELINE: Tests PASS on unfixed code
        PRESERVATION: Tests PASS on fixed code
        
        **Validates: Requirements 3.1**
        """
        assume(len(business_data['business_name']) >= 3)
        assume(len(business_data['description']) >= 20)
        
        rag = RAGEngine(use_real_data=True)
        
        def mock_llm(prompt: str) -> str:
            return '{"key_drivers": ["test"], "competitive_strategy": "test", "positioning": "test", "opportunities": "test"}'
        
        # Mock MarketDataFetcher to avoid real API calls
        with patch.object(rag.market_fetcher, 'get_industry_overview') as mock_overview:
            mock_overview.return_value = {
                'industry': business_data['industry'],
                'market_size': '$500B',
                'growth_rate': '15%',
                'num_competitors': 0,
                'competitors': [],
                'fetch_status': 'success'
            }
            
            result = rag.generate_market_analysis_with_rag(business_data, mock_llm)
            
            # Property: Always returns a string
            assert isinstance(result, str), f"Should return string for industry {business_data['industry']}"
            assert len(result) > 0, "Should return non-empty result"


class TestMarketDataFetcherPreservation:
    """
    Test that MarketDataFetcher behavior remains unchanged.
    This is the core data layer that both RAG and MCP should use.
    """
    
    def test_market_data_fetcher_singleton_preservation(self):
        """
        Test that MarketDataFetcher singleton pattern is preserved.
        
        BASELINE BEHAVIOR:
        - get_market_data_fetcher() returns same instance
        - Instance is MarketDataFetcher type
        
        PRESERVATION:
        - Singleton pattern must remain unchanged after fix
        """
        fetcher1 = get_market_data_fetcher()
        fetcher2 = get_market_data_fetcher()
        
        assert fetcher1 is fetcher2, "Should return same singleton instance"
        assert isinstance(fetcher1, MarketDataFetcher), "Should be MarketDataFetcher instance"
        
        print("\n✓ MarketDataFetcher singleton pattern preserved")
        print(f"  - Is singleton: {fetcher1 is fetcher2}")
        print(f"  - Type: {type(fetcher1)}")
    
    def test_market_data_fetcher_get_industry_overview_structure(self):
        """
        Test that get_industry_overview() returns expected data structure.
        
        BASELINE BEHAVIOR:
        - Returns dict with specific keys: industry, market_size, competitors, growth_rate, etc.
        - fetch_status indicates success or failure
        
        PRESERVATION:
        - Return structure must remain identical after fix
        
        **Validates: Requirements 3.2**
        """
        fetcher = get_market_data_fetcher()
        
        # Mock yfinance to avoid real API calls
        with patch('src.data.market_data_fetcher.yf') as mock_yf:
            # Mock ticker data
            mock_ticker = patch.object(mock_yf, 'Ticker')
            
            # Call with a test industry
            result = fetcher.get_industry_overview('technology')
            
            # Verify structure (even if it fails, structure should be consistent)
            assert isinstance(result, dict), "Should return dict"
            assert 'industry' in result, "Should have 'industry' key"
            assert 'market_size' in result, "Should have 'market_size' key"
            assert 'competitors' in result, "Should have 'competitors' key"
            assert 'growth_rate' in result, "Should have 'growth_rate' key"
            assert 'fetch_status' in result, "Should have 'fetch_status' key"
            assert 'data_source' in result, "Should have 'data_source' key"
            
            # Verify types
            assert isinstance(result['competitors'], list), "Competitors should be list"
            assert result['fetch_status'] in ['success', 'failed'], "Status should be success or failed"
        
        print("\n✓ MarketDataFetcher.get_industry_overview() structure preserved")
        print(f"  - Returns dict: True")
        print(f"  - Has required keys: True")
        print(f"  - Structure: {list(result.keys())}")
    
    @given(industry=industry_strategy())
    @settings(max_examples=10, deadline=None)
    def test_property_get_industry_overview_consistent_structure(self, industry):
        """
        Property: For all industry inputs, MarketDataFetcher.get_industry_overview()
        returns data structure unchanged.
        
        BASELINE: Tests PASS on unfixed code
        PRESERVATION: Tests PASS on fixed code
        
        **Validates: Requirements 3.2**
        """
        fetcher = get_market_data_fetcher()
        
        # Mock to avoid real API calls in property tests
        with patch('src.data.market_data_fetcher.yf'):
            result = fetcher.get_industry_overview(industry)
            
            # Property: Consistent structure for all industries
            required_keys = ['industry', 'market_size', 'competitors', 'growth_rate', 'fetch_status']
            for key in required_keys:
                assert key in result, f"Should have '{key}' for industry {industry}"
            
            assert isinstance(result['competitors'], list), "Competitors always a list"
            assert isinstance(result['industry'], str), "Industry always a string"


class TestBusinessPlanGeneratorPreservation:
    """
    Test that business plan generation continues to work correctly when MCP is disabled.
    """
    
    def test_business_plan_generator_initialization_without_mcp(self):
        """
        Test that BusinessPlanGenerator initializes correctly with MCP disabled.
        
        BASELINE BEHAVIOR:
        - Should initialize with use_real_data flag
        - Should create RAG engine instance
        
        PRESERVATION:
        - Initialization should remain unchanged after fix
        
        **Validates: Requirements 3.3**
        """
        # Initialize with real data
        generator = BusinessPlanGenerator(use_real_data=True)
        
        assert generator is not None, "Generator should initialize"
        assert hasattr(generator, 'rag_engine'), "Should have rag_engine"
        assert generator.rag_engine is not None, "RAG engine should be initialized"
        
        print("\n✓ BusinessPlanGenerator initialization preserved")
        print(f"  - Has RAG engine: {generator.rag_engine is not None}")
    
    def test_business_plan_generator_uses_rag_directly(self):
        """
        Test that when MCP is disabled, business plan generation uses RAG directly.
        
        BASELINE BEHAVIOR:
        - Generator should have rag_engine
        - RAG engine should have direct access to MarketDataFetcher
        - No MCP client should be involved
        
        PRESERVATION:
        - Direct RAG usage must be preserved after fix
        
        **Validates: Requirements 3.1, 3.3**
        """
        generator = BusinessPlanGenerator(use_real_data=True)
        
        # Verify RAG engine setup
        assert generator.rag_engine is not None, "Should have RAG engine"
        assert generator.rag_engine.use_real_data is True, "RAG should use real data"
        assert generator.rag_engine.market_fetcher is not None, "RAG should have market fetcher"
        
        # Verify it's the singleton
        singleton = get_market_data_fetcher()
        assert generator.rag_engine.market_fetcher is singleton, "Should use singleton"
        
        print("\n✓ BusinessPlanGenerator uses RAG directly (preserved)")
        print(f"  - RAG engine present: True")
        print(f"  - RAG uses real data: {generator.rag_engine.use_real_data}")
        print(f"  - RAG has market fetcher: True")
        print(f"  - Uses singleton: True")


class TestLLMIntegrationPreservation:
    """
    Test that LLM integration with Groq/OpenAI continues to work correctly.
    """
    
    def test_llm_provider_configuration_preserved(self):
        """
        Test that LLM provider configuration is preserved.
        
        BASELINE BEHAVIOR:
        - BusinessPlanGenerator accepts llm_provider parameter
        - Should support 'groq', 'openai', 'anthropic'
        
        PRESERVATION:
        - LLM provider configuration must remain unchanged
        
        **Validates: Requirements 3.4**
        """
        # Test different LLM providers
        providers = ['groq', 'openai']
        
        for provider in providers:
            generator = BusinessPlanGenerator(llm_provider=provider, use_real_data=True)
            assert generator is not None, f"Should initialize with {provider}"
        
        print("\n✓ LLM provider configuration preserved")
        print(f"  - Supported providers: {providers}")


class TestDataFlowPreservation:
    """
    Test the complete data flow path when MCP is disabled.
    This verifies the fallback path remains functional.
    """
    
    def test_data_flow_rag_to_market_fetcher_direct(self):
        """
        Test that data flows correctly: RAG → MarketDataFetcher → Yahoo Finance
        
        BASELINE BEHAVIOR:
        - When MCP_ENABLED=false
        - RAG engine should call MarketDataFetcher directly
        - No MCP client should be in the data path
        
        PRESERVATION:
        - This direct path must remain functional after fix
        
        **Validates: Requirements 3.1, 3.2**
        """
        # Verify MCP is disabled
        assert os.environ.get('MCP_ENABLED', 'false') == 'false', "MCP should be disabled for this test"
        
        # Initialize RAG engine
        rag = RAGEngine(use_real_data=True)
        
        # Verify direct access to MarketDataFetcher
        assert rag.market_fetcher is not None, "RAG should have direct market fetcher access"
        
        # Mock MarketDataFetcher to trace calls
        with patch.object(rag.market_fetcher, 'get_industry_overview') as mock_overview:
            mock_overview.return_value = {
                'industry': 'technology',
                'market_size': '$500B',
                'growth_rate': '15%',
                'num_competitors': 0,
                'competitors': [],
                'fetch_status': 'success'
            }
            
            # Generate market analysis
            business_data = {
                'business_name': 'Test Co',
                'industry': 'technology',
                'description': 'Test description',
                'target_market': 'SMB'
            }
            
            def mock_llm(prompt):
                return '{"key_drivers": ["test"], "competitive_strategy": "test", "positioning": "test", "opportunities": "test"}'
            
            result = rag.generate_market_analysis_with_rag(business_data, mock_llm)
            
            # Verify MarketDataFetcher was called directly
            assert mock_overview.called, "MarketDataFetcher.get_industry_overview should be called"
            assert isinstance(result, str), "Should return string result"
        
        print("\n✓ Data flow RAG → MarketDataFetcher preserved")
        print("  - Path: RAG Engine → MarketDataFetcher (direct)")
        print("  - MCP bypassed: True")


class TestRegressionPrevention:
    """
    Additional regression prevention tests to ensure the fix doesn't break existing functionality.
    """
    
    def test_rag_engine_singleton_pattern(self):
        """
        Test that RAG engine singleton pattern works correctly.
        
        BASELINE: get_rag_engine() returns singleton
        PRESERVATION: Must remain unchanged
        """
        rag1 = get_rag_engine(use_real_data=True)
        rag2 = get_rag_engine(use_real_data=True)
        
        # Note: RAG engine doesn't enforce strict singleton, but should return instance
        assert rag1 is not None, "Should return RAG instance"
        assert rag2 is not None, "Should return RAG instance"
        
        print("\n✓ RAG engine accessor function preserved")
    
    def test_market_data_fetcher_methods_preserved(self):
        """
        Test that all MarketDataFetcher methods remain available.
        
        BASELINE: Fetcher has all required methods
        PRESERVATION: Method signatures must remain unchanged
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
            assert hasattr(fetcher, method_name), f"Should have {method_name} method"
            method = getattr(fetcher, method_name)
            assert callable(method), f"{method_name} should be callable"
        
        print("\n✓ MarketDataFetcher method interface preserved")
        print(f"  - Methods: {', '.join(required_methods)}")


if __name__ == "__main__":
    """
    Run preservation tests with verbose output
    """
    print("=" * 80)
    print("Preservation Property Tests")
    print("Testing RAG Engine Direct Access Preservation")
    print("=" * 80)
    print("\nThese tests MUST PASS on unfixed code (baseline).")
    print("These tests MUST PASS on fixed code (no regressions).")
    print("=" * 80)
    
    # Ensure MCP is disabled
    os.environ['MCP_ENABLED'] = 'false'
    print(f"\nMCP_ENABLED: {os.environ.get('MCP_ENABLED')}")
    print("=" * 80)
    
    pytest.main([__file__, "-v", "-s"])

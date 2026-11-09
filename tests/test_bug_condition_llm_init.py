"""
Bug Condition Exploration Test for LLM Initialization Proxy Error

This test explores the bug condition where OpenAI client initialization fails with httpx 0.28.0+
due to incompatibility between OpenAI SDK 1.54.0 and the updated httpx library.

**CRITICAL**: This test MUST FAIL on unfixed code (with openai==1.54.0 and httpx>=0.28.0).
Test failure confirms the bug exists and demonstrates the TypeError about 'proxies' parameter.

**EXPECTED BEHAVIOR (encoded in this test)**:
- All OpenAI-based providers should initialize successfully WITHOUT TypeError
- The client objects should be usable for API calls
- Anthropic provider should be unaffected (control test)

**AFTER FIX**: This same test will PASS when OpenAI SDK is upgraded to 1.55.3+,
confirming the expected behavior is satisfied.

**Validates: Requirements 2.1, 2.2**
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai.llm_manager import (
    GroqProvider,
    OpenAIProvider,
    OpenRouterProvider,
    HuggingFaceProvider,
    AnthropicProvider
)


# Dummy API keys for initialization testing (no actual API calls will be made)
DUMMY_GROQ_KEY = "gsk_test_dummy_key_for_initialization_testing"
DUMMY_OPENAI_KEY = "sk-test-dummy-key-for-initialization-testing"
DUMMY_OPENROUTER_KEY = "sk-or-test-dummy-key-for-initialization"
DUMMY_HUGGINGFACE_KEY = "hf_test_dummy_key_for_initialization"
DUMMY_ANTHROPIC_KEY = "sk-ant-test-dummy-key-for-initialization"


class TestBugConditionExploration:
    """
    Bug Condition Exploration Tests
    
    These tests encode the EXPECTED behavior: successful initialization without errors.
    On UNFIXED code (openai==1.54.0 with httpx>=0.28.0), these tests will FAIL,
    demonstrating the bug exists and documenting the counterexamples.
    """
    
    def test_groq_provider_initialization(self):
        """
        Property 1: Bug Condition - Groq Provider Initialization
        
        Test that GroqProvider initializes successfully without raising
        TypeError about 'proxies' parameter.
        
        EXPECTED ON UNFIXED CODE: 
        - FAILS with TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
        - Error originates from openai/_base_client.py line 755 in SyncHttpxClientWrapper.__init__
        
        EXPECTED ON FIXED CODE:
        - PASSES with successful client initialization
        """
        try:
            provider = GroqProvider(
                api_key=DUMMY_GROQ_KEY,
                model="llama-3.1-8b-instant"
            )
            
            # Verify client object is created
            assert provider is not None, "GroqProvider instance should not be None"
            assert hasattr(provider, 'client'), "GroqProvider should have client attribute"
            assert provider.client is not None, "GroqProvider.client should not be None"
            
            # Verify client is usable (has expected methods)
            assert hasattr(provider.client, 'chat'), "Client should have chat attribute"
            assert hasattr(provider.client.chat, 'completions'), "Client.chat should have completions"
            
            print("\n✓ GroqProvider initialized successfully")
            print(f"  - Client type: {type(provider.client)}")
            print(f"  - Model: {provider.model}")
            
        except TypeError as e:
            # This is the EXPECTED failure on unfixed code
            error_msg = str(e)
            print("\n✗ GroqProvider initialization FAILED (this confirms bug exists)")
            print(f"  - Error: {error_msg}")
            print(f"  - Error type: {type(e).__name__}")
            
            # Document the counterexample
            if "'proxies'" in error_msg or "proxies" in error_msg:
                print("  - COUNTEREXAMPLE FOUND: 'proxies' parameter error")
                print("  - Root cause: OpenAI SDK 1.54.0 incompatible with httpx 0.28.0+")
            
            # Re-raise to fail the test (expected on unfixed code)
            raise
    
    def test_openai_provider_initialization(self):
        """
        Property 1: Bug Condition - OpenAI Provider Initialization
        
        Test that OpenAIProvider initializes successfully without raising
        TypeError about 'proxies' parameter.
        """
        try:
            provider = OpenAIProvider(
                api_key=DUMMY_OPENAI_KEY,
                model="gpt-4-turbo-preview"
            )
            
            # Verify client object is created
            assert provider is not None, "OpenAIProvider instance should not be None"
            assert hasattr(provider, 'client'), "OpenAIProvider should have client attribute"
            assert provider.client is not None, "OpenAIProvider.client should not be None"
            
            # Verify client is usable
            assert hasattr(provider.client, 'chat'), "Client should have chat attribute"
            assert hasattr(provider.client.chat, 'completions'), "Client.chat should have completions"
            
            print("\n✓ OpenAIProvider initialized successfully")
            print(f"  - Client type: {type(provider.client)}")
            print(f"  - Model: {provider.model}")
            
        except TypeError as e:
            error_msg = str(e)
            print("\n✗ OpenAIProvider initialization FAILED (this confirms bug exists)")
            print(f"  - Error: {error_msg}")
            
            if "'proxies'" in error_msg or "proxies" in error_msg:
                print("  - COUNTEREXAMPLE FOUND: 'proxies' parameter error")
            
            raise
    
    def test_openrouter_provider_initialization(self):
        """
        Property 1: Bug Condition - OpenRouter Provider Initialization
        
        Test that OpenRouterProvider initializes successfully without raising
        TypeError about 'proxies' parameter.
        """
        try:
            provider = OpenRouterProvider(
                api_key=DUMMY_OPENROUTER_KEY,
                model="meta-llama/llama-3.2-3b-instruct:free"
            )
            
            # Verify client object is created
            assert provider is not None, "OpenRouterProvider instance should not be None"
            assert hasattr(provider, 'client'), "OpenRouterProvider should have client attribute"
            assert provider.client is not None, "OpenRouterProvider.client should not be None"
            
            # Verify client is usable
            assert hasattr(provider.client, 'chat'), "Client should have chat attribute"
            assert hasattr(provider.client.chat, 'completions'), "Client.chat should have completions"
            
            print("\n✓ OpenRouterProvider initialized successfully")
            print(f"  - Client type: {type(provider.client)}")
            print(f"  - Model: {provider.model}")
            
        except TypeError as e:
            error_msg = str(e)
            print("\n✗ OpenRouterProvider initialization FAILED (this confirms bug exists)")
            print(f"  - Error: {error_msg}")
            
            if "'proxies'" in error_msg or "proxies" in error_msg:
                print("  - COUNTEREXAMPLE FOUND: 'proxies' parameter error")
            
            raise
    
    def test_huggingface_provider_initialization(self):
        """
        Property 1: Bug Condition - HuggingFace Provider Initialization
        
        Test that HuggingFaceProvider initializes successfully without raising
        TypeError about 'proxies' parameter.
        """
        try:
            provider = HuggingFaceProvider(
                api_key=DUMMY_HUGGINGFACE_KEY,
                model="mistralai/Mixtral-8x7B-Instruct-v0.1"
            )
            
            # Verify client object is created
            assert provider is not None, "HuggingFaceProvider instance should not be None"
            assert hasattr(provider, 'client'), "HuggingFaceProvider should have client attribute"
            assert provider.client is not None, "HuggingFaceProvider.client should not be None"
            
            # Verify client is usable
            assert hasattr(provider.client, 'chat'), "Client should have chat attribute"
            assert hasattr(provider.client.chat, 'completions'), "Client.chat should have completions"
            
            print("\n✓ HuggingFaceProvider initialized successfully")
            print(f"  - Client type: {type(provider.client)}")
            print(f"  - Model: {provider.model}")
            
        except TypeError as e:
            error_msg = str(e)
            print("\n✗ HuggingFaceProvider initialization FAILED (this confirms bug exists)")
            print(f"  - Error: {error_msg}")
            
            if "'proxies'" in error_msg or "proxies" in error_msg:
                print("  - COUNTEREXAMPLE FOUND: 'proxies' parameter error")
            
            raise
    
    def test_anthropic_provider_initialization_control(self):
        """
        Control Test: Anthropic Provider Initialization (Unaffected)
        
        Test that AnthropicProvider initializes successfully.
        This provider uses a separate SDK and should be UNAFFECTED by the OpenAI/httpx bug.
        
        EXPECTED ON BOTH UNFIXED AND FIXED CODE:
        - PASSES with successful client initialization
        - This confirms the bug is isolated to OpenAI SDK-based providers
        """
        try:
            provider = AnthropicProvider(
                api_key=DUMMY_ANTHROPIC_KEY,
                model="claude-3-5-sonnet-20241022"
            )
            
            # Verify client object is created
            assert provider is not None, "AnthropicProvider instance should not be None"
            assert hasattr(provider, 'client'), "AnthropicProvider should have client attribute"
            assert provider.client is not None, "AnthropicProvider.client should not be None"
            
            # Verify client has expected Anthropic SDK methods
            assert hasattr(provider.client, 'messages'), "Anthropic client should have messages attribute"
            
            print("\n✓ AnthropicProvider initialized successfully (CONTROL TEST - unaffected)")
            print(f"  - Client type: {type(provider.client)}")
            print(f"  - Model: {provider.model}")
            print("  - This confirms the bug is isolated to OpenAI SDK-based providers")
            
        except Exception as e:
            print("\n✗ AnthropicProvider initialization FAILED (unexpected - should work)")
            print(f"  - Error: {str(e)}")
            raise


class TestEnvironmentValidation:
    """
    Validate test environment matches bug conditions
    """
    
    def test_openai_version_check(self):
        """
        Document the OpenAI SDK version being tested
        
        Bug condition: openai_version < "1.55.3" AND httpx_version >= "0.28.0"
        """
        try:
            import openai
            openai_version = openai.__version__
            print(f"\n📦 OpenAI SDK version: {openai_version}")
            
            # Parse version
            major, minor, patch = openai_version.split('.')
            version_tuple = (int(major), int(minor), int(patch))
            
            if version_tuple < (1, 55, 3):
                print("  ⚠️  OpenAI SDK < 1.55.3 (bug condition met)")
            else:
                print("  ✓ OpenAI SDK >= 1.55.3 (fix should be applied)")
                
        except ImportError:
            pytest.skip("OpenAI package not installed")
    
    def test_httpx_version_check(self):
        """
        Document the httpx version being tested
        
        Bug condition: httpx_version >= "0.28.0"
        """
        try:
            import httpx
            httpx_version = httpx.__version__
            print(f"\n📦 httpx version: {httpx_version}")
            
            # Parse version
            parts = httpx_version.split('.')
            major, minor = int(parts[0]), int(parts[1])
            version_tuple = (major, minor)
            
            if version_tuple >= (0, 28):
                print("  ⚠️  httpx >= 0.28.0 (bug condition met)")
            else:
                print("  ℹ️  httpx < 0.28.0 (bug may not manifest)")
                
        except ImportError:
            pytest.skip("httpx package not installed")


if __name__ == "__main__":
    """
    Run tests directly with verbose output to see counterexamples
    """
    print("=" * 80)
    print("Bug Condition Exploration Test")
    print("Testing LLM Provider Initialization with OpenAI SDK 1.54.0 + httpx 0.28.0+")
    print("=" * 80)
    
    pytest.main([__file__, "-v", "-s"])

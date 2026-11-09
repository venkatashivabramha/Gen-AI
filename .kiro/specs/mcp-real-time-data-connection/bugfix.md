# Bugfix Requirements Document

## Introduction

The business plan generator application has integrated real-time market data capabilities through Yahoo Finance API and RAG engine, but the MCP (Model Context Protocol) layer appears disconnected to users due to the `MCP_ENABLED=false` flag in the environment configuration. While the system successfully fetches real market data through `MarketDataFetcher` and the RAG engine, the MCP integration layer is not properly connected to this data flow, creating confusion about whether real-time data is actually being used.

The bug affects user confidence in the system's data accuracy and creates architectural inconsistency where MCP exists as a parallel enhancement layer that doesn't contribute to the actual data pipeline. This needs to be fixed to ensure MCP properly integrates with the existing Yahoo Finance data fetcher and provides transparent, verifiable market data to business plan generation.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN the environment variable MCP_ENABLED is set to false THEN the MCP system appears disconnected even though real market data flows through MarketDataFetcher

1.2 WHEN business_plan_generator.py instantiates MCPClient THEN it creates a separate data enhancement layer that duplicates functionality already provided by MarketDataFetcher

1.3 WHEN users generate business plans with "Use Real Market Data" enabled THEN the real data comes from RAG engine → MarketDataFetcher but MCP shows as inactive, creating confusion about data sources

1.4 WHEN MCPClient.enhance_business_plan() is called THEN it fetches redundant market data using its own Yahoo Finance calls instead of leveraging the existing MarketDataFetcher singleton

1.5 WHEN the system logs show "MCP Direct Integration: X tools available" THEN users believe MCP is providing data, but the actual data path bypasses MCP through the RAG engine

### Expected Behavior (Correct)

2.1 WHEN the environment variable MCP_ENABLED is set to true THEN the MCP system SHALL be properly connected and integrated with the Yahoo Finance data pipeline

2.2 WHEN business_plan_generator.py instantiates MCPClient THEN it SHALL use the existing MarketDataFetcher singleton to avoid duplicate API calls and maintain a single data source

2.3 WHEN users generate business plans with "Use Real Market Data" enabled THEN the data path SHALL flow transparently through MCP → MarketDataFetcher → Yahoo Finance, providing verifiable real-time data

2.4 WHEN MCPClient.enhance_business_plan() is called THEN it SHALL delegate to MarketDataFetcher.get_industry_overview() and format the results for business plan enhancement

2.5 WHEN the system shows MCP as active THEN it SHALL accurately reflect that MCP is the integration layer coordinating market data from Yahoo Finance through MarketDataFetcher

2.6 WHEN MCP is disabled (MCP_ENABLED=false) THEN the system SHALL still provide real-time market data through direct RAG → MarketDataFetcher calls with clear logging that MCP is bypassed

### Unchanged Behavior (Regression Prevention)

3.1 WHEN RAG engine is initialized with use_real_data=True THEN the system SHALL CONTINUE TO fetch real-time market data from Yahoo Finance through MarketDataFetcher

3.2 WHEN MarketDataFetcher.get_industry_overview() is called THEN it SHALL CONTINUE TO return comprehensive market data including market size, competitors, growth rates, and employee statistics

3.3 WHEN business plans are generated with existing form data THEN they SHALL CONTINUE TO include accurate market analysis, SWOT analysis, and financial projections

3.4 WHEN the .env file contains valid GROQ_API_KEY THEN the LLM integration SHALL CONTINUE TO function correctly for content generation

3.5 WHEN users select output formats (PDF, DOCX, HTML) THEN the document generators SHALL CONTINUE TO produce properly formatted business plans

3.6 WHEN the system operates on Streamlit Cloud THEN it SHALL CONTINUE TO work without requiring external MCP server processes

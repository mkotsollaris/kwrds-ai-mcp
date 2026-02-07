# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for the [kwrds.ai](https://www.kwrds.ai) keyword research and SEO API. It exposes kwrds.ai functionality as MCP tools that can be used by Claude Desktop and other MCP clients.

## Development Commands

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the server (for testing)
KWRDS_AI_API_KEY=your-key python run_server.py
```

## Architecture

The server uses stdio transport for MCP communication:

- **Entry point**: `run_server.py` → `stdio_server.py`
- **Tool definitions**: `tools/definitions.py` - All MCP tool schemas are defined here
- **Handlers**: Three handler classes route tool calls to the kwrds.ai API:
  - `handlers/keyword_handlers.py` - Keyword research, search volume, LSI, topic research
  - `handlers/analysis_handlers.py` - SERP analysis, URL rankings, PAA questions
  - `handlers/ai_handlers.py` - AI-powered keyword research and content generation
- **Utilities**: `utils/http_client.py` handles API requests, `utils/response_utils.py` limits response sizes for MCP

## API Endpoints

The server connects to three kwrds.ai API domains:
- `keywordresearch.api.kwrds.ai` - Main keyword research endpoints
- `paa.api.kwrds.ai` - People Also Ask data
- `workflow.api.kwrds.ai` - Topic research workflows

## Key Implementation Details

- All tool handlers receive `api_key` from tool arguments or fall back to `KWRDS_AI_API_KEY` env var
- Response arrays are capped at 10 items via `limit_response_size()` to prevent oversized MCP responses
- Country codes use format like `en-US`, `es-ES` for most tools; PAA uses separate country/language codes

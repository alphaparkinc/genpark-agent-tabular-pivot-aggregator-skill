# Tabular Pivot Aggregator Skill for Autonomous Agents

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue.svg)](https://modelcontextprotocol.io)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](requirements.txt)

Provides autonomous data analysis and spreadsheet agents with high-speed in-memory pivot tables, grouping calculations, and rollup aggregations without pandas.

## Features
- **Flexible Aggregations**: Supports sum, average, min, max, and count.
- **Schema-less JSON/CSV Row Handling**: Gracefully handles missing values and dirty data types.
- **Zero Heavy Dependencies**: Pure standard library execution with zero installation overhead.

## MCP Server Integration
```bash
python mcp_server.py
```

### Available MCP Tools
- `pivot_records`: Compute grouped aggregations across tabular dictionaries.

# Agent Demos

This directory contains example agents that demonstrate various capabilities of the agent system.

## Available Demos

### 1. Echo Agent
A simple agent that demonstrates basic message handling and formatting.
- Text transformation (uppercase, lowercase, title case)
- Message repetition
- Formatted output

```bash
python3 echo_agent.py
```

### 2. Weather Agent
Demonstrates API integration and data processing capabilities.
- HTTP request handling
- Data transformation
- Unit conversion
- Formatted weather reports

```bash
python3 weather_agent.py
```

### 3. Stock Agent
Shows real-time data handling and technical analysis capabilities.
- Historical data processing
- Technical indicators calculation:
  - Simple Moving Averages (SMA)
  - Relative Strength Index (RSI)
  - Bollinger Bands
- Trend analysis and signals
- Formatted market reports

```bash
python3 stock_agent.py
```

### 4. News Agent
Demonstrates text processing and sentiment analysis capabilities.
- News article generation
- Sentiment analysis
- Topic extraction
- Trend analysis
- Formatted news reports

```bash
python3 news_agent.py
```

## Common Features

Each agent demonstrates these core capabilities:
- Async/await pattern
- Error handling
- Logging
- Data validation
- Formatted output
- Progress tracking

## Output Formatting

All agents use a consistent output format with:
- Box-style headers
- Clear section organization
- Emoji indicators
- Color-coded status
- Timestamp information

## Running the Demos

1. Make sure you have the required dependencies:
```bash
pip install aiohttp
```

2. Run any demo directly:
```bash
python3 demos/[agent_name].py
```

## Example Output

### Echo Agent
```
╔══════════════════════════════════════════════════════════════════╗
║  Echo Agent Demo - Style: uppercase
╚══════════════════════════════════════════════════════════════════╝

Original: Hello, World!
Formatted:
HELLO, WORLD!
```

### Weather Agent
```
╔══════════════════════════════════════════════════════════════════╗
║  🌤️  Weather Report - London, UK
╚══════════════════════════════════════════════════════════════════╝

📍 Location:
  • Coordinates: 51.5074°N, 0.1278°E
...
```

### Stock Agent
```
╔══════════════════════════════════════════════════════════════════╗
║  📊 Stock Analysis - AAPL
╚══════════════════════════════════════════════════════════════════╝

💰 Price Information:
  • Current Price: $150.25
  • 24h Change: +2.35%
...
```

### News Agent
```
╔══════════════════════════════════════════════════════════════════╗
║  📰 News Analysis - GOOGL
╚══════════════════════════════════════════════════════════════════╝

📊 Summary:
  • Period: Last 7 days
  • Articles Analyzed: 10
...
```

## Notes

- These demos use mock data and simulated APIs for demonstration purposes
- In a production environment, replace mock data with real API calls
- API keys in the demos are placeholders
- Error handling demonstrates best practices for production use
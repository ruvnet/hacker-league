# Insider Trading Mirror System

A sophisticated system for monitoring and mirroring publicly disclosed insider trades using ReACT methodology and intelligent agents.

## Features

- **Real-Time Data Ingestion**: Fetch insider trading data from multiple sources (Finnhub, Tradefeeds)
- **Intelligent Analysis**: Filter and identify significant trades using configurable criteria
- **Automated Trading**: Execute trades with comprehensive risk management
- **Performance Monitoring**: Real-time metrics and alerting via Prometheus/Grafana
- **Detailed Reporting**: Generate HTML and CSV reports with trade analytics
- **CLI Interface**: Command-line tools for all system operations
- **Docker Support**: Containerized deployment with monitoring stack

## Architecture

The system uses a multi-agent architecture with ReACT (Reasoning and Acting) methodology:

1. **Data Agent**: Fetches and validates insider trading data
2. **Analysis Agent**: Identifies significant trades worth mirroring
3. **Trading Agent**: Executes trades with risk management
4. **Reporting Agent**: Generates performance reports and analytics

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (for containerized deployment)
- API keys for data sources (Finnhub, Tradefeeds)
- Redis (for caching)
- Prometheus/Grafana (for monitoring)

## Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/insider-mirror.git
   cd insider-mirror
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # for development
   ```

4. Set up environment variables:
   ```bash
   cp env.sample .env
   # Edit .env with your configuration
   ```

5. Install pre-commit hooks:
   ```bash
   make dev-setup
   ```

### Docker Deployment

1. Build and start services:
   ```bash
   docker-compose up -d
   ```

2. Monitor logs:
   ```bash
   docker-compose logs -f
   ```

## Usage

### CLI Commands

1. Fetch insider trading data:
   ```bash
   insider-mirror data fetch --limit 100
   ```

2. Analyze trades:
   ```bash
   insider-mirror analyze trades --min-value 100000
   ```

3. Execute trades:
   ```bash
   insider-mirror trade execute --mode paper
   ```

4. Generate reports:
   ```bash
   insider-mirror report generate --format html
   ```

5. Run the complete system:
   ```bash
   insider-mirror run --interval 3600
   ```

### Development Commands

```bash
# Run tests
make test

# Run tests with coverage
make coverage

# Format code
make format

# Run linting
make lint

# Build documentation
make docs
```

## Configuration

### Agent Configuration

Edit `src/insider_mirror/config/agents.yaml` to configure agent behavior:
- Role definitions
- LLM models
- Validation rules
- Progress tracking

### Task Configuration

Edit `src/insider_mirror/config/tasks.yaml` to configure tasks:
- Data validation rules
- Analysis filters
- Trading parameters
- Report settings

### Analysis Configuration

Edit `src/insider_mirror/config/analysis.yaml` to configure:
- Performance metrics
- Risk thresholds
- Optimization rules
- Reporting formats

## Monitoring

### Metrics

Access metrics and dashboards:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Alertmanager: http://localhost:9093

### Alerts

Configure alerts in `alertmanager.yml`:
- Slack notifications
- Email alerts
- Custom alert rules

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_data_agent.py

# Run with coverage
pytest --cov=insider_mirror

# Run performance tests
pytest -m "slow"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Security

- All API keys should be stored in environment variables
- Use paper trading mode for testing
- Monitor system logs for suspicious activity
- Regular security audits recommended

## License

MIT License - see LICENSE file for details

## Disclaimer

This system is for educational purposes only. Always consult with legal and compliance experts before deploying any trading system. Trading based on insider information that is not publicly disclosed is illegal in most jurisdictions.

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Authors

- Your Name (@yourusername)

## Acknowledgments

- LangGraph and LangChain for agent orchestration
- Finnhub and Tradefeeds for market data
- OpenRouter for LLM capabilities

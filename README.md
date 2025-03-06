# cron-agent

Convert a schedule in natural language to a cron schedule using agentic programming.

The Cron Agent is built on [Pydantic AI](https://ai.pydantic.dev/).

## Setup

### Set up the project

1. Clone the clone-agent repository

2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

2. Create venv and install dependencies
```bash
cd cron-agent
uv sync
```

3. Activate the virtual environment
```bash
source .venv/bin/activate
```

### Configure API keys
1. Create .env file with your API keys

OPENAI_API_KEY=...

ANTHROPIC_API_KEY=...

2. Run the following command to load the API keys

```bash
set -a; source .env; set +a
```

## Try it out
Convert a schedule in natural language to a cron schedule

```bash
python main.py
```

## Testing
The following script will test two cron agents using LLMs from Anthropic and OpenAI.

```bash
PYTHONPATH=. pytest -vs tests/test_cron_agent.py
```

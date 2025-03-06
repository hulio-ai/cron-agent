import logging
from typing import Any

from pydantic_ai.agent import AgentRunResult

logger = logging.getLogger(__name__)


def log_agent_result(
    logger: logging.Logger, agent_name: str, result: AgentRunResult[Any]
):
    usage = result.usage()
    logger.info(
        f"{agent_name} - usage: {usage.total_tokens} tokens, {usage.requests} requests"
    )
    logger.debug(f"{agent_name} - result: {result.data}")
    if not result.data:
        logger.error(f"{agent_name} - all agent messages: {result.all_messages_json()}")

import os

import pytest
from pydantic_ai.usage import UsageLimits

from cron_agent import CronAgent
from logger_setup import get_logger
from schedule import Schedule
from utils import log_agent_result

logger = get_logger(__name__)

agent_config_names = [
    "anthropic_cron_agent_config.yaml",
    "openai_cron_agent_config.yaml",
]


@pytest.fixture
def agent(request):
    agent_config_name = request.param
    agent_config_path = os.path.join("cron_agent", agent_config_name)
    return CronAgent.from_configfile(agent_config_path)


@pytest.mark.asyncio
@pytest.mark.parametrize("agent", agent_config_names, indirect=True)
@pytest.mark.parametrize(
    "schedule_input, schedule_cron, schedule_natural",
    [
        (
            "every 1 minutes at 10 AM",
            ["* 10 * * *", "*/1 10 * * *"],
            "Every 1 minutes at 10 AM",
        ),
        (
            "Monday to Friday at 10 AM",
            ["0 10 * * 1-5"],
            "Every weekday at 10 AM",
        ),
        (
            "every week on Sunday",
            ["0 0 * * 0"],
            "Weekly on Sunday at midnight",
        ),
        ("every day", ["0 0 * * *"], "Daily at midnight"),
        ("every day at 6AM", ["0 6 * * *"], "Daily at 6AM"),
        ("every 6 hours", ["0 */6 * * *"], "Every 6 hours"),
        ("every 1 minute", ["* * * * *", "*/1 * * * *"], "Every minute"),
    ],
)
async def test_valid_schedules(agent, schedule_input, schedule_cron, schedule_natural):
    for _ in range(3):
        logger.info(f"Running test case: {schedule_input}")
        result = await agent.run(
            schedule_input,
            usage_limits=UsageLimits(
                request_limit=agent.request_limit,
                total_tokens_limit=agent.total_tokens_limit,
            ),
        )
        log_agent_result(logger, "Cron agent", result)
        logger.info(f"Result: {result.data}")
        assert result.data is not None
        assert isinstance(result.data, Schedule)
        assert result.data.cron in schedule_cron


@pytest.mark.asyncio
@pytest.mark.parametrize("agent", agent_config_names, indirect=True)
@pytest.mark.parametrize(
    "invalid_schedule",
    [
        "invalid schedule format",
        "every morning",
        "every 30 seconds",
    ],
)
async def test_invalid_schedule(agent, invalid_schedule):
    for _ in range(3):
        logger.info(f"Running test case: {invalid_schedule}")
        result = await agent.run(
            invalid_schedule,
            usage_limits=UsageLimits(
                request_limit=agent.request_limit,
                total_tokens_limit=agent.total_tokens_limit,
            ),
        )
        log_agent_result(logger, "Cron agent", result)
        assert not result.data or not isinstance(result.data, Schedule)


@pytest.mark.asyncio
@pytest.mark.parametrize("agent", agent_config_names, indirect=True)
@pytest.mark.parametrize(
    "invalid_schedule",
    [
        None,
    ],
)
async def test_schedule_exception(agent, invalid_schedule):
    with pytest.raises(Exception):
        await agent.run(
            invalid_schedule,
            usage_limits=UsageLimits(
                request_limit=agent.request_limit,
                total_tokens_limit=agent.total_tokens_limit,
            ),
        )

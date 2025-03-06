import os

from cron_agent import CronAgent
from logger_setup import get_logger
from schedule import Schedule

logger = get_logger(__name__)


async def get_schedule(cron_agent_config_path: str, schedule_natural: str) -> Schedule:
    cron_agent = CronAgent.from_configfile(cron_agent_config_path)
    try:
        agent_result = await cron_agent.run(schedule_natural)
        schedule = agent_result.data
        if schedule is None or not isinstance(schedule, Schedule):
            logger.info(
                f"Agent {cron_agent.agent_config_name} returned invalid result: {agent_result}"
            )
            return None
    except Exception:
        logger.exception(
            f"Error in parsing schedule {schedule_natural} by using agent {cron_agent.agent_config_name}"
        )
        return None
    return schedule


if __name__ == "__main__":
    import asyncio

    cron_agent_config_name = "anthropic_cron_agent_config.yaml"
    schedule_natural = "every 10 minutes"

    cron_agent_config_path = os.path.join("cron_agent", cron_agent_config_name)
    schedule = asyncio.run(get_schedule(cron_agent_config_path, schedule_natural))
    print(schedule)
    # expected output: cron='*/10 * * * *' natural='Every 10 minutes'

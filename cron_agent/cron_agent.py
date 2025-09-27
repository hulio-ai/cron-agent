import os
from typing import Union

import yaml
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from schedule import Schedule

_DEFAULT_REQUEST_LIMIT = 1
_DEFAULT_TOTAL_TOKENS_LIMIT = 1000


class CronAgent:
    """
    A cron agent that converts a cron in natural language to a Schedule object
    """

    OutputType = Union[Schedule, None]

    def __init__(
        self,
        agent_config_name: str,
        request_limit: int = _DEFAULT_REQUEST_LIMIT,
        total_tokens_limit: int = _DEFAULT_TOTAL_TOKENS_LIMIT,
        **kwargs,
    ):
        self.agent_config_name = agent_config_name
        self.request_limit = request_limit
        self.total_tokens_limit = total_tokens_limit
        self.agent = Agent(**kwargs)

    @classmethod
    def from_configfile(cls, agent_config_filepath: str) -> "CronAgent":
        with open(agent_config_filepath, "r") as file:
            agent_config = yaml.safe_load(file)
        return cls(
            agent_config_name=os.path.basename(agent_config_filepath),
            request_limit=agent_config["usage_limits"]["request_limit"],
            total_tokens_limit=agent_config["usage_limits"]["total_tokens_limit"],
            model=agent_config["model_id"],
            system_prompt=agent_config["system_prompt"],
            output_type=cls.OutputType,  # type: ignore
            model_settings=ModelSettings(**agent_config["model_settings"]),
        )

    def run(self, *args, **kwargs):
        """Delegate to the internal agent's run method"""
        return self.agent.run(*args, **kwargs)

    def run_sync(self, *args, **kwargs):
        """Delegate to the internal agent's run_sync method"""
        return self.agent.run_sync(*args, **kwargs)


if __name__ == "__main__":
    import json
    import os

    agent_config_name = "openai_cron_agent_config.yaml"
    agent_config_path = os.path.join(os.path.dirname(__file__), agent_config_name)
    agent = CronAgent.from_configfile(agent_config_path)
    agent_result = agent.run_sync("every week on Sunday")
    print(json.dumps(json.loads(agent_result.all_messages_json()), indent=4))
    print(agent_result.output)

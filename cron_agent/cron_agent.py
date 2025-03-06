import os
from typing import Optional, Union

import yaml
from pydantic_ai import Agent
from pydantic_ai.models import ModelSettings

from schedule import Schedule

_DEFAULT_REQUEST_LIMIT = 1
_DEFAULT_TOTAL_TOKENS_LIMIT = 1000


class CronAgent(Agent):
    """
    A cron agent that converts a cron in natural language to a Schedule object
    """

    ResultType = Union[Schedule, None]

    def __init__(
        self,
        agent_config_name: Optional[str] = None,
        request_limit: int = _DEFAULT_REQUEST_LIMIT,
        total_tokens_limit: int = _DEFAULT_TOTAL_TOKENS_LIMIT,
        **kwargs,
    ):
        self.agent_config_name = agent_config_name
        self.request_limit = request_limit
        self.total_tokens_limit = total_tokens_limit
        super().__init__(**kwargs)

    @classmethod
    def from_configfile(cls, agent_config_filepath: str) -> "CronAgent":
        with open(agent_config_filepath, "r") as file:
            agent_config = yaml.safe_load(file)
        return CronAgent(
            agent_config_name=os.path.basename(agent_config_filepath),
            request_limit=agent_config["usage_limits"]["request_limit"],
            total_tokens_limit=agent_config["usage_limits"]["total_tokens_limit"],
            model=agent_config["model_id"],
            system_prompt=agent_config["system_prompt"],
            result_type=cls.ResultType,  # type: ignore
            model_settings=ModelSettings(**agent_config["model_settings"]),
        )


if __name__ == "__main__":
    import json
    import os

    agent_config_name = "openai_cron_agent_config.yaml"
    agent_config_path = os.path.join(os.path.dirname(__file__), agent_config_name)
    agent = CronAgent.from_configfile(agent_config_path)
    agent_result = agent.run_sync("every week on Sunday")
    print(json.dumps(json.loads(agent_result.all_messages_json()), indent=4))
    print(agent_result.data)

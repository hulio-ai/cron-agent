import re

from pydantic import BaseModel, Field, field_validator


def validate_cron_format(cron_str: str) -> bool:
    """Regex pattern for standard cron format (minute hour day month weekday)
    >>> validate_cron_format("* * * * *")
    True
    >>> validate_cron_format("0 10 * * 1-5")
    True
    >>> validate_cron_format("1 * * * *")
    True
    >>> validate_cron_format("in valid cron")
    False
    """
    pattern = r"^(\*|[0-9]|[1-5]?[0-9]|\*/[0-9]+|(?:[0-9]|[1-5]?[0-9])(,(?:[0-9]|[1-5]?[0-9]))*|(?:[0-9]|[1-5]?[0-9])-(?:[0-9]|[1-5]?[0-9]))\s+"  # minute (0-59)
    pattern += r"(\*|[0-9]|1[0-9]|2[0-3]|\*/[0-9]+|(?:[0-9]|1[0-9]|2[0-3])(,(?:[0-9]|1[0-9]|2[0-3]))*|(?:[0-9]|1[0-9]|2[0-3])-(?:[0-9]|1[0-9]|2[0-3]))\s+"  # hour (0-23)
    pattern += r"(\*|[1-9]|[12][0-9]|3[01]|\*/[0-9]+|(?:[1-9]|[12][0-9]|3[01])(,(?:[1-9]|[12][0-9]|3[01]))*|(?:[1-9]|[12][0-9]|3[01])-(?:[1-9]|[12][0-9]|3[01]))\s+"  # day of month (1-31)
    pattern += r"(\*|[1-9]|1[0-2]|\*/[0-9]+|(?:[1-9]|1[0-2])(,(?:[1-9]|1[0-2]))*|(?:[1-9]|1[0-2])-(?:[1-9]|1[0-2]))\s+"  # month (1-12)
    pattern += (
        r"(\*|[0-6]|\*/[0-9]+|(?:[0-6])(,(?:[0-6]))*|[0-6]-[0-6])$"  # day of week (0-6)
    )

    return bool(re.match(pattern, cron_str))


class Schedule(BaseModel):
    cron: str = Field(
        description="The cron schedule in cron format",
        examples=["* * * * *", "0 10 * * *"],
    )
    natural: str = Field(
        description="A very short, unambiguous schedule in human readable format"
    )

    @field_validator("cron")
    def validate_cron(cls, v):
        if not validate_cron_format(v):
            raise ValueError("Invalid cron format")
        return v

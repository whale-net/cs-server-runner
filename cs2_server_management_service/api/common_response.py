from dataclasses import dataclass


# using dataclasses because i cba with pydantic
@dataclass
class CommonResponse:
    message: str

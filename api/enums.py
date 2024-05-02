import enum


class UserDomainEnum(enum.Enum):
    canary = "canary"
    regular = "regular"


class EnvModeEnum(enum.Enum):
    stage = "stage"
    preprod = "preprod"
    prod = "prod"
import enum


class UserDomain(enum.Enum):
    canary = "canary"
    regular = "regular"


class EnvMode(enum.Enum):
    stage = "stage"
    preprod = "preprod"
    prod = "prod"
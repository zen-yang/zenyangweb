import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()
    admin = auto()


class ENUMEncoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, obj):
        if isinstance(obj, UserRole):
            return {self.prefix: obj.name}
        else:
            return super().default(obj)


def enum_decode(d):
    if ENUMEncoder.prefix in d:
        name = d[ENUMEncoder.prefix]
        return UserRole[name]
    else:
        return d

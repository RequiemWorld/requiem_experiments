import enum
from typing import Type


class FieldType(enum.Enum):
    LONG = enum.auto()


class Field:
    def __init__(self, type_: FieldType, size: int):
        self.type = type_
        self.size = size
        self.name: str | None = None


class LongField(Field):

    def __init__(self):
        super().__init__(FieldType.LONG, 8)


def read_fields_from_class(class_: Type) -> list[Field]:
    fields: list[Field] = list()
    for attribute_name in dir(class_):
        attribute_value = getattr(class_, attribute_name)
        if not isinstance(attribute_value, Field):
            continue
        attribute_value.name = attribute_name
        fields.append(attribute_value)

    return fields
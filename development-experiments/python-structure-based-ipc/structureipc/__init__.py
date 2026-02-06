import abc
from dataclasses import dataclass
from ._fields import Field
from ._fields import FieldType
from ._fields import LongField
from ._fields import read_fields_from_class

class Structure:
    _filled_in_fields: list[Field] = list()
    size: int
    def __init__(self, *args, **kwargs):
        for field in self._filled_in_fields:
            attribute_name = field.name
            setattr(self, attribute_name, kwargs[attribute_name])

    def __init_subclass__(cls, **kwargs):
        cls._filled_in_fields = read_fields_from_class(cls)
        structure_size = 0
        for field in cls._filled_in_fields:
            structure_size += field.size
        cls.size = structure_size

    def write_into(self, buffer: bytearray):
        for field in self._filled_in_fields:
            offset = 0
            attribute_value = getattr(self, field.name)
            if field.type == FieldType.LONG:
                buffer[offset:field.size] = attribute_value.to_bytes(16, "little")
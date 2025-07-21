from typing import List
from backend.models import ValueTable
from backend.models import Attribute
from backend.models import  SafetyFunction
from backend.models import NetworkNode
class Signal:
    def __init__(self, name: str, id: int, receivers: List['NetworkNode'],
                 factor: float, offset: float, minimum: float, maximum: float,
                 byte_order: str, type: str, unit: str, safety_function: SafetyFunction,
                 value_table: ValueTable = None,
                 attributes: [List[Attribute]] = None):
        self.name = name
        self.id = id
        self.receivers = receivers
        self.factor = factor
        self.offset = offset
        self.minimum = minimum
        self.maximum = maximum
        self.byte_order = byte_order
        self.type = type
        self.unit = unit
        self.safety_function = safety_function
        self.value_table = value_table
        self.attributes = attributes if attributes is not None else []
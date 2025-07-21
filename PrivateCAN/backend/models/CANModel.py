from typing import List, Dict

from backend.models.Message import Message
from backend.models.Attribute import Attribute
from backend.models.ValueTable import ValueTable
from backend.models import NetworkNode
from backend.models import Signal

class CANModel:
    def __init__(self, network_nodes: List[NetworkNode], messages: List[Message],
                 signals: List[Signal], value_tables: Dict[str, ValueTable]):
        self.network_nodes = network_nodes
        self.messages = messages
        self.signals = signals
        self.value_tables = value_tables
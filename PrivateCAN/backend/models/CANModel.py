from typing import List, Dict

from .Message import Message
from .Attribute import Attribute
from .ValueTable import ValueTable
from .NetworkNode import NetworkNode
from .Signal import Signal

class CANModel:
    def __init__(self, network_nodes: List[NetworkNode], messages: List[Message],
                 signals: List[Signal], value_tables: Dict[str, ValueTable]):
        self.network_nodes = network_nodes
        self.messages = messages
        self.signals = signals
        self.value_tables = value_tables

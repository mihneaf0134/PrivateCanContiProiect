from typing import List
from backend.models import Attribute
from backend.models import Signal
from backend.models import NetworkNode
class Message:
    def __init__(self, name: str, type: str, id: int, signals: List[Signal],
                 transmitters: List[NetworkNode], receivers: List[NetworkNode],
                 layout: dict, attributes: [List[Attribute]] = None):
        self.name = name
        self.type = type
        self.id = id
        self.signals = signals
        self.transmitters = transmitters
        self.receivers = receivers
        self.layout = layout
        self.attributes = attributes if attributes is not None else []
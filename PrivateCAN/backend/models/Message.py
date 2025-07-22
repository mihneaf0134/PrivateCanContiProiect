from typing import List

from PrivateCAN.backend.models import NetworkNode, Signal, Attribute


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
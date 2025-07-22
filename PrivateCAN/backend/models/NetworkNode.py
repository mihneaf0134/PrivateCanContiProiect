from typing import List

from PrivateCAN.backend.models import Attribute, Signal


class NetworkNode:
    def __init__(self, name: str, id: int, type: str, signals: List[Signal],
                 transmitters: List['NetworkNode'], receivers: List['NetworkNode'],
                 layout: dict, baud_rate: int = 500000,
                 attributes: [List[Attribute]] = None):
        self.name = name
        self.id = id
        self.type = type
        self.signals = signals
        self.transmitters = transmitters if transmitters is not None else []
        self.receivers = receivers if receivers is not None else []
        self.layout = layout
        self.baud_rate = baud_rate
        self.attributes = attributes if attributes is not None else []

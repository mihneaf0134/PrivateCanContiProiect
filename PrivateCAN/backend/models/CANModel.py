from backend.models.Message import Message
from backend.models.Attribute import Attribute
from backend.models.ValueTable import ValueTable

class CANModel:
    def __init__(self):
        self.network_nodes = []
        self.messages = []
        self.signals = []
        self.attributes = []
        self.value_tables = []

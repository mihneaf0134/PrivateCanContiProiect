class CanController:
    def __init__(self, name: str):
        self.name = name
        self.tx_messages = []  # IDs of transmitted messages

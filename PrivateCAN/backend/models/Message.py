class Message:
    def __init__(self, name, frame_id, length, cycle_time, msg_type):
        self.name = name
        self.frame_id = frame_id
        self.length = length
        self.cycle_time = cycle_time
        self.type = msg_type
        self.signals = []
        self.attributes = []
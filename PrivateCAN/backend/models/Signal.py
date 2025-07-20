class Signal:
    def __init__(self, name, start_bit, length, byte_order, value_type, unit, minimum, maximum, comment):
        self.name = name
        self.start_bit = start_bit
        self.length = length
        self.byte_order = byte_order
        self.value_type = value_type
        self.unit = unit
        self.minimum = minimum
        self.maximum = maximum
        self.comment = comment
        self.attributes = []
        self.value_table = None

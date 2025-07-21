class Attribute:
    def __init__(self, object_type: str, value_type: str, default_value: object,
                 minimum: object, maximum: object, comment: str):
        self.object_type = object_type
        self.value_type = value_type
        self.default_value = default_value
        self.minimum = minimum
        self.maximum = maximum
        self.comment = comment
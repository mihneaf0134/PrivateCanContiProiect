from enum import Enum

class SafetyFunction(Enum):
    OM = "Operational Mode"
    ASIL_A = "ASIL A"
    ASIL_B = "ASIL B"
    ASIL_C = "ASIL C"
    ASIL_D = "ASIL D"
    QM = "Quality Managed"
import re

from PrivateCAN.backend.models import Message, NetworkNode, CANModel, Signal, SafetyFunction, Attribute


class DBCParser:
    bo_pattern = re.compile(r'^BO_\s*(0{1}|(?:[1-9]\d*))\s*([^-\s]*)\s*:\s*(?:0{1}|(?:[1-9]\d*))\s*([^-\s]+)$', re.MULTILINE)
    sg_pattern = re.compile(
        r'\s*SG_\s*([^-\s]*)\s*([^-\s]*)?\s*:\s*(?:0{1}|(?:[1-9]\d*))\|(?:0{1}|(?:[1-9]\d*))\@[01][+-]\s*'
        r'\(((?:0{1}|(?:[1-9]\d*))(?:\.\d+)?(?:[eE][-+]?\d*)?),\s*(-?(?:0{1}|(?:[1-9]\d*))(?:\.\d+)?(?:[eE][-+]?\d*)?)\)\s*'
        r'\[(0{1}|-?\d*\.?\d*|\d*[eE][-+]?\d*)\|\s*(0{1}|-?\d*\.?\d*|-?\d*\.?\d*[eE][-+]?\d*)\]\s*".*"\s*([^-\s]+)',
        re.MULTILINE)
    ba_bo_pattern = re.compile(r'BA_ \"(\S+)\" BO_ (\d+) (\d+);', re.MULTILINE)
    ba_sg_pattern = re.compile(r'BA_ \"(\S+)\" SG_ (\d+) (\S+) (-{0,1}(?:\d+|\d+\.\d*));', re.MULTILINE)

    @staticmethod
    def parse_dbc_to_model(file_path: str) -> CANModel:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        messages = []
        network_nodes = {}
        signals = []
        value_tables = {}

        for line in content.splitlines():
            bo_match = DBCParser.bo_pattern.match(line)
            if bo_match:
                msg_id = int(bo_match.group(1))
                msg_name = bo_match.group(2)
                transmitter = bo_match.group(3)

                if transmitter not in network_nodes:
                    network_nodes[transmitter] = NetworkNode(
                        name=transmitter,
                        id=len(network_nodes) + 1,
                        type="ECU",
                        signals=[],
                        transmitters=[],
                        receivers=[],
                        layout={},
                        baud_rate=500000
                    )

                message = Message(
                    name=msg_name,
                    type="CAN",
                    id=msg_id,
                    signals=[],
                    transmitters=[network_nodes[transmitter]],
                    receivers=[],
                    layout={}
                )
                messages.append(message)

            sg_match = DBCParser.sg_pattern.match(line)
            if sg_match and messages:
                signal = Signal(
                    name=sg_match.group(1),
                    id=len(signals) + 1,
                    receivers=[],
                    factor=float(sg_match.group(3)),
                    offset=float(sg_match.group(4)),
                    minimum=float(sg_match.group(5)),
                    maximum=float(sg_match.group(6)),
                    byte_order="little" if sg_match.group(0).split('@')[1][0] == '1' else "big",
                    type="unsigned" if sg_match.group(0).split('@')[1][1] == '+' else "signed",
                    unit=sg_match.group(7),
                    safety_function=SafetyFunction.SafetyFunction.OM,
                    value_table=None,
                )
                messages[-1].signals.append(signal)
                signals.append(signal)

        for m in DBCParser.ba_bo_pattern.finditer(content):
            attr_name = m.group(1)
            msg_id = int(m.group(2))
            value = int(m.group(3))
            for msg in messages:
                if msg.id == msg_id:
                    attr = Attribute(
                        object_type="Message",
                        value_type="int",
                        default_value=value,
                        minimum=None,
                        maximum=None,
                        comment=f"Attribute {attr_name} for message {msg_id}"
                    )
                    msg.attributes.append(attr)

        for m in DBCParser.ba_sg_pattern.finditer(content):
            attr_name = m.group(1)
            msg_id = int(m.group(2))
            signal_name = m.group(3)
            value_str = m.group(4)
            value = float(value_str) if '.' in value_str else int(value_str)
            for msg in messages:
                if msg.id == msg_id:
                    for sig in msg.signals:
                        if sig.name == signal_name:
                            attr = Attribute(
                                object_type="Signal",
                                value_type="float" if '.' in value_str else "int",
                                default_value=value,
                                minimum=None,
                                maximum=None,
                                comment=f"Attribute {attr_name} for signal {signal_name}"
                            )
                            sig.attributes.append(attr)

        return CANModel(
            network_nodes=list(network_nodes.values()),
            messages=messages,
            signals=signals,
            value_tables=value_tables
        )
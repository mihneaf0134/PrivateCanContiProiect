from PrivateCAN.backend.models import ValueTable, Attribute
from PrivateCAN.backend.models import CANModel, Message, Signal, NetworkNode
import json
from typing import Dict, Any

class CANModelSerializer:
    @staticmethod
    def to_dict(can_model: CANModel) -> Dict[str, Any]:
        return {
            "network_nodes": [CANModelSerializer._serialize_node(node) for node in can_model.network_nodes],
            "messages": [CANModelSerializer._serialize_message(msg) for msg in can_model.messages],
            "signals": [CANModelSerializer._serialize_signal(sig) for sig in can_model.signals],
            "value_tables": {name: CANModelSerializer._serialize_value_table(vt)
                           for name, vt in can_model.value_tables.items()}
        }

    @staticmethod
    def _serialize_node(node: NetworkNode) -> Dict[str, Any]:
        return {
            "name": node.name,
            "id": node.id,
            "type": node.type,
            "baud_rate": node.baud_rate
        }

    @staticmethod
    def _serialize_message(msg: Message) -> Dict[str, Any]:
        return {
            "name": msg.name,
            "id": msg.id,
            "type": msg.type,
            "transmitter": msg.transmitters[0].name if msg.transmitters else None,
            "signals": [CANModelSerializer._serialize_signal(sig) for sig in msg.signals],
            "attributes": [CANModelSerializer._serialize_attr(attr) for attr in msg.attributes]
        }

    @staticmethod
    def _serialize_signal(sig: Signal) -> Dict[str, Any]:
        return {
            "name": sig.name,
            "id": sig.id,
            "factor": sig.factor,
            "offset": sig.offset,
            "min": sig.minimum,
            "max": sig.maximum,
            "unit": sig.unit,
            "byte_order": sig.byte_order,
            "type": sig.type,
            "attributes": [CANModelSerializer._serialize_attr(attr) for attr in sig.attributes]
        }

    @staticmethod
    def _serialize_value_table(vt: ValueTable) -> Dict[str, Any]:
        return {
            "name": vt.name,
            "values": vt.value,
            "comment": vt.comment
        }

    @staticmethod
    def _serialize_attr(attr: Attribute) -> Dict[str, Any]:
        return {
            "name": attr.object_type,
            "value": attr.default_value,
            "comment": attr.comment
        }

    @staticmethod
    def to_json(can_model: CANModel) -> str:
        return json.dumps(CANModelSerializer.to_dict(can_model), indent=2)

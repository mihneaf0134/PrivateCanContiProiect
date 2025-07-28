import cantools
from cantools.database import Database
from cantools.database.can.message import Message
from cantools.database.can.signal import Signal

def optimize_dbc(dbc_content: str, pack=True, prioritize=True, simplify=True):
    original_db = cantools.database.load_string(dbc_content, strict=False)
    new_db = Database()
    change_log = {"removed_empty_messages": [], "reassigned_ids": [], "packed_signals": []}

    messages = original_db.messages

    if simplify:
        before = len(messages)
        messages = [msg for msg in messages if msg.signals]
        removed = before - len(messages)
        change_log["removed_empty_messages"] = [msg.name for msg in original_db.messages if not msg.signals]

    if prioritize:
        messages.sort(key=lambda msg: (-len(msg.signals), msg.frame_id))
        base_id = 0x100
        for msg in messages:
            change_log["reassigned_ids"].append((msg.name, hex(msg.frame_id), hex(base_id)))
            msg.frame_id = base_id
            base_id += 1

    if pack:
        packed_signals = []
        other_msgs = []
        max_bits = 64
        current_bit = 0

        for msg in messages:
            for sig in msg.signals:
                if current_bit + sig.length <= max_bits:
                    new_sig = Signal(
                        name=sig.name,
                        start=current_bit,
                        length=sig.length,
                        byte_order='little',
                        is_signed=sig.is_signed
                    )
                    packed_signals.append(new_sig)
                    change_log["packed_signals"].append(sig.name)
                    current_bit += sig.length
                else:
                    other_msgs.append(msg)
                    break

        if packed_signals:
            packed_msg = Message(
                name="PackedMessage",
                frame_id=0x200,
                signals=packed_signals,
                length=8,
                senders=[],
                is_extended_frame=False
            )
            other_msgs.append(packed_msg)

        messages = other_msgs

    for msg in messages:
        new_db.messages.append(msg)

    for bus in original_db.buses:
        new_db.buses.append(bus)

    for node in original_db.nodes:
        new_db.nodes.append(node)

    return new_db, change_log

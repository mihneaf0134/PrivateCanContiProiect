import cantools
from cantools.database import Database
from cantools.database.can.message import Message
from cantools.database.can.signal import Signal

def optimize_dbc(dbc_content: str, pack=True, prioritize=True, simplify=True):
    original_db = cantools.database.load_string(dbc_content, strict=False)
    new_db = Database()

    messages = original_db.messages
    if simplify:
        messages = [msg for msg in messages if msg.signals]

    if prioritize:
        messages.sort(key=lambda msg: (-len(msg.signals), msg.frame_id))
        base_id = 0x100
        for msg in messages:
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
                    current_bit += sig.length
                else:

                    other_msgs.append(Message(
                        name=msg.name,
                        frame_id=msg.frame_id,
                        signals=msg.signals,
                        length=msg.length,
                        senders=msg.senders,
                        is_extended_frame=msg.is_extended_frame
                    ))
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

    return new_db

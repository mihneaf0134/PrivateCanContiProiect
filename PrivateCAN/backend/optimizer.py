import cantools
from cantools.database import Database
from cantools.database.can.message import Message
from cantools.database.can.signal import Signal

def optimize_dbc(dbc_content: str, pack=True, prioritize=True, simplify=True):
    original_db = cantools.database.load_string(dbc_content, strict=False)
    new_db = Database()
    change_log = {"removed_empty_messages": [], "reassigned_ids": [], "packed_signals": [], "removed_duplicate_signals": []}

    messages = original_db.messages

    if simplify:
        # Remove messages with no signals
        before = len(messages)
        messages = [msg for msg in messages if msg.signals]
        removed = before - len(messages)
        change_log["removed_empty_messages"] = [msg.name for msg in original_db.messages if not msg.signals]

    new_messages = []
    for msg in messages:
        seen_signals = {}
        unique_signals = []
        for sig in msg.signals:
            sig_key = (sig.name, sig.start, sig.length, sig.byte_order, sig.is_signed, sig.is_float,
                       sig.is_multiplexer, tuple(sig.multiplexer_ids) if sig.multiplexer_ids else None)
            if sig_key not in seen_signals:
                seen_signals[sig_key] = sig
                unique_signals.append(sig)
            else:
                change_log["removed_duplicate_signals"].append((msg.name, sig.name))

        # Create a new Message object with unique signals
        new_msg = Message(
            name=msg.name,
            frame_id=msg.frame_id,
            length=msg.length,
            senders=msg.senders,
            signals=unique_signals,
            is_extended_frame=msg.is_extended_frame,
            comment=msg.comment,
            cycle_time=msg.cycle_time,
            bus_name=msg.bus_name
        )
        new_messages.append(new_msg)
    messages = new_messages

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

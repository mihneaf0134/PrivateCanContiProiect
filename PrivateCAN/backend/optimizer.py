import copy
import cantools
from cantools.database import Database
from cantools.database.can.message import Message
from cantools.database.can.signal import Signal

FS_ATTRIBUTE_KEY = "FunctionalSafetyLevel"
SAFETY_LEVEL_PREFIX = "ASIL"


def _is_safety_critical(sig: Signal) -> bool:
    try:
        level = sig.attributes.get(FS_ATTRIBUTE_KEY, "QM") if sig.attributes else "QM"
    except AttributeError:
        level = "QM"
    return isinstance(level, str) and level.upper().startswith(SAFETY_LEVEL_PREFIX)


def _remove_duplicate_signals(messages, change_log):
    new_messages = []
    for msg in messages:
        seen = {}
        unique = []
        for sig in msg.signals:
            sig_key = (
                sig.name,
                sig.length,
                sig.byte_order,
                sig.is_signed,
                getattr(sig, "is_float", False),
            )
            if sig_key not in seen:
                seen[sig_key] = True
                unique.append(sig)
            else:
                change_log["removed_duplicate_signals"].append((msg.name, sig.name))
        new_msg = Message(
            name=msg.name,
            frame_id=msg.frame_id,
            length=msg.length,
            senders=msg.senders,
            signals=unique,
            is_extended_frame=msg.is_extended_frame,
            comment=msg.comment,
            cycle_time=msg.cycle_time,
            bus_name=msg.bus_name,
        )
        new_messages.append(new_msg)
    return new_messages


def _repack_layout(messages, change_log):
    max_bits = 64

    for msg in messages:
        safety_sigs = [s for s in msg.signals if _is_safety_critical(s)]
        normal_sigs = [s for s in msg.signals if not _is_safety_critical(s)]

        occupied = [False] * max_bits
        for s in safety_sigs:
            for b in range(s.start, min(max_bits, s.start + s.length)):
                occupied[b] = True

        normal_sigs.sort(key=lambda s: -s.length)

        for sig in normal_sigs:
            new_start = None
            for bit in range(0, max_bits - sig.length + 1):
                if all(not occupied[b] for b in range(bit, bit + sig.length)):
                    new_start = bit
                    break
            if new_start is None:
                continue
            if new_start != sig.start:
                change_log["repacked_signals"].append((msg.name, sig.name, sig.start, new_start))
                sig.start = new_start
            for b in range(sig.start, sig.start + sig.length):
                occupied[b] = True

        msg.signals.sort(key=lambda s: s.start)

    return messages


def optimize_dbc(
    dbc_content: str,
    prioritize: bool = True,
    simplify: bool = True,
    repack: bool = True,
):

    original_db = cantools.database.load_string(dbc_content, strict=False)
    new_db = Database()

    change_log = {
        "removed_empty_messages": [],
        "reassigned_ids": [],
        "removed_duplicate_signals": [],
        "repacked_signals": [],
    }

    messages = list(original_db.messages)
    if simplify:
        change_log["removed_empty_messages"] = [m.name for m in messages if not m.signals]
        messages = [m for m in messages if m.signals]

    messages = _remove_duplicate_signals(messages, change_log)

    if prioritize:
        messages.sort(key=lambda m: (-len(m.signals), m.frame_id))
        base_id = 0x100
        for m in messages:
            if m.frame_id != base_id:
                change_log["reassigned_ids"].append((m.name, hex(m.frame_id), hex(base_id)))
                m.frame_id = base_id
            base_id += 1

    if repack:
        messages = _repack_layout(messages, change_log)

    for m in messages:
        new_db.messages.append(m)

    for b in original_db.buses:
        new_db.buses.append(b)

    for n in original_db.nodes:
        new_db.nodes.append(n)

    return new_db, change_log

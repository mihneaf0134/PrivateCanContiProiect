import re
import os
import sys

# Mesaj
bo_pattern = re.compile(r'^BO_\s*(0{1}|(?:[1-9]\d*))\s*([^-\s]*)\s*:\s*(?:0{1}|(?:[1-9]\d*))\s*([^-\s]+)$', re.MULTILINE)
# Semanl
sg_pattern = re.compile(
    r'\s*SG_\s*([^-\s]*)\s*([^-\s]*)?\s*:\s*(?:0{1}|(?:[1-9]\d*))\|(?:0{1}|(?:[1-9]\d*))\@[01][+-]\s*'
    r'\(((?:0{1}|(?:[1-9]\d*))(?:\.\d+)?(?:[eE][-+]?\d*)?),\s*(-?(?:0{1}|(?:[1-9]\d*))(?:\.\d+)?(?:[eE][-+]?\d*)?)\)\s*'
    r'\[(0{1}|-?\d*\.?\d*|\d*[eE][-+]?\d*)\|\s*(0{1}|-?\d*\.?\d*|-?\d*\.?\d*[eE][-+]?\d*)\]\s*".*"\s*([^-\s]+)',
    re.MULTILINE)
# Atribut mesaj
ba_bo_pattern = re.compile(r'BA_ \"(\S+)\" BO_ (\d+) (\d+);', re.MULTILINE)
# Atribut semanl
ba_sg_pattern = re.compile(r'BA_ \"(\S+)\" SG_ (\d+) (\S+) (-{0,1}(?:\d+|\d+\.\d*));', re.MULTILINE)

def parse_dbc_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
        
    messages = []
    current_message = None

    for line in lines:
        bo_match = bo_pattern.match(line)
        if bo_match:
            if current_message:
                messages.append(current_message)
            current_message = {
                'MESSAGE_ID': int(bo_match.group(1)),
                'MESSAGE_NAME': bo_match.group(2),
                'TRANSMITTER': bo_match.group(3),
                'SIGNALS': [],
                'ATTRIBUTES': {},
            }
            continue

        sg_match = sg_pattern.match(line)
        if sg_match and current_message:
            signal = {
                'SIGNAL_NAME': sg_match.group(1),
                'MULTIPLEX': sg_match.group(2) or None,
                'FACTOR': float(sg_match.group(3)),
                'OFFSET': float(sg_match.group(4)),
                'MIN': float(sg_match.group(5)),
                'MAX': float(sg_match.group(6)),
                'UNIT': sg_match.group(7),
                'ATTRIBUTES': {},
            }
            current_message['SIGNALS'].append(signal)

    if current_message:
        messages.append(current_message)

    for m in ba_bo_pattern.finditer(content):
        attr_name = m.group(1)
        msg_id = int(m.group(2))
        value = int(m.group(3))
        for msg in messages:
            if msg['MESSAGE_ID'] == msg_id:
                msg['ATTRIBUTES'][attr_name] = value

    for m in ba_sg_pattern.finditer(content):
        attr_name = m.group(1)
        msg_id = int(m.group(2))
        signal_name = m.group(3)
        value_str = m.group(4)
        value = float(value_str) if '.' in value_str else int(value_str)
        for msg in messages:
            if msg['MESSAGE_ID'] == msg_id:
                for sig in msg['SIGNALS']:
                    if sig['SIGNAL_NAME'] == signal_name:
                        sig['ATTRIBUTES'][attr_name] = value

    return messages


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Mod folosire: python3 parser.py <calea_catre_dbc>")
        sys.exit(1)

    dbc_path = sys.argv[1]

    if not os.path.exists(dbc_path):
        print(f"Eroare: Fisierul '{dbc_path}' nu a fost gasit!")
        sys.exit(1)

    messages = parse_dbc_file(dbc_path)

    for msg in messages:
        print(f"\nMessage: {msg['MESSAGE_NAME']} (ID: {msg['MESSAGE_ID']}, Transmitter: {msg['TRANSMITTER']})")
        if msg['ATTRIBUTES']:
            print("  Message Attributes:")
            for k, v in msg['ATTRIBUTES'].items():
                print(f"    {k}: {v}")
        print("  Signals:")
        for sig in msg['SIGNALS']:
            print(f"    - {sig['SIGNAL_NAME']} (Factor: {sig['FACTOR']}, Offset: {sig['OFFSET']}, Min: {sig['MIN']}, Max: {sig['MAX']}, Unit: {sig['UNIT']})")
            if sig['ATTRIBUTES']:
                print("      Signal Attributes:")
                for k, v in sig['ATTRIBUTES'].items():
                    print(f"        {k}: {v}")

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

# Functiile de parsare

def parse_bo(text):
    results = []
    for m in bo_pattern.finditer(text):
        # regex-ul de la mesaj are 3 grupuri
        message_id = int(m.group(1))
        message_name = m.group(2)
        transmitter = m.group(3)
        results.append({
            'MESSAGE_ID': message_id,
            'MESSAGE_NAME': message_name,
            'TRANSMITTER': transmitter,
            })
    return results

def parse_sg(text):
    results = []
    for m in sg_pattern.finditer(text):
        # regex-ul de la semnal are 7 grupuri
        signal_name = m.group(1)
        multiplex = m.group(2) or None
        factor = float(m.group(3))
        offset = float(m.group(4))
        min_val = float(m.group(5))
        max_val = float(m.group(6))
        unit = m.group(7)
        results.append({
            'SIGNAL_NAME': signal_name,
            'MULTIPLEX': multiplex,
            'FACTOR': factor,
            'OFFSET': offset,
            'MIN': min_val,
            'MAX': max_val,
            'UNIT': unit,
        })
    return results

def parse_ba_bo(text):
    results = []
    for m in ba_bo_pattern.finditer(text):
        # regex-ul de la atribute mesaj are 3 grupuri
        attribute_name = m.group(1)
        message_id = int(m.group(2))
        value = int(m.group(3))
        results.append({
            'ATTRIBUTE_NAME': attribute_name,
            'MESSAGE_ID': message_id,
            'VALUE': value,
        })
    return results

def parse_ba_sg(text):
    results = []
    for m in ba_sg_pattern.finditer(text):
        # regex-ul de la atribute semnal are 4 grupuri
        attribute_name = m.group(1)
        signal_id = int(m.group(2))
        signal_name = m.group(3)
        value_str = m.group(4)
        value = float(value_str) if '.' in value_str else int(value_str)
        results.append({
            'ATTRIBUTE_NAME': attribute_name,
            'SIGNAL_ID': signal_id,
            'SIGNAL_NAME': signal_name,
            'VALUE': value,
        })
    return results

# Functia de parsare unui fisier DBC
def parse_dbc_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    messages = parse_bo(content)
    signals = parse_sg(content)
    ba_bo_attrs = parse_ba_bo(content)
    ba_sg_attrs = parse_ba_sg(content)

    return {
        'messages': messages,
        'signals': signals,
        'ba_bo_attributes': ba_bo_attrs,
        'ba_sg_attributes': ba_sg_attrs,
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Mod folosire: python3 parser.py <calea_catre_dbc>")
        sys.exit(1)

    dbc_path = sys.argv[1]

    if not os.path.exists(dbc_path):
        print(f"Eroare: Fisierul '{dbc_path}' nu a fost gasit!")
        sys.exit(1)

    data = parse_dbc_file(dbc_path)

    print("Messages:")
    for m in data['messages']:
        print(m)

    print("\nSignals:")
    for s in data['signals']:
        print(s)

    print("\nBA_ attributes for messages:")
    for a in data['ba_bo_attributes']:
        print(a)

    print("\nBA_ attributes for signals:")
    for a in data['ba_sg_attributes']:
        print(a)

import json


def stringify(obj):
    return json.dumps(obj, ensure_ascii=False)


def jsonify(string):
    return json.loads(string.decode())

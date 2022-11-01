import json
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "html": {"type": "string"}
    }
}

with open("hotel_1_test.json", "r") as f:
    data = f.read()

my_json = json.loads(data)

validate(instance=my_json, schema=schema)

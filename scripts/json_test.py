import json

with open('projects/section_map.json') as f:
    section_map = json.load(f)

# Accessing values:
print(section_map["cosplay"])
print(section_map["cosplay"]["header"])
print(section_map["cosplay"]["description"])
print(section_map["miniatures"]["description"])
try:
    print(section_map["sadfsadsF"])
except KeyError as e:
    print(f"*** KEY not found: {e}")

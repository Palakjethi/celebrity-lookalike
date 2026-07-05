import json

with open('models/meta.json', 'r') as f:
    metadata = json.load(f)

male = sum(1 for c in metadata if c.get('gender') == 'male')
female = sum(1 for c in metadata if c.get('gender') == 'female')
unknown = sum(1 for c in metadata if c.get('gender') == 'unknown')

print(f'Total: {len(metadata)}')
print(f'Male:    {male}')
print(f'Female:  {female}')
print(f'Unknown: {unknown}')

print('\nSample:')
for c in metadata[:5]:
    print(f'  {c["name"]} -> {c.get("gender", "missing")}')
    
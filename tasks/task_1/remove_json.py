import os

for name in os.scandir('./'):
    if name.name.endswith('.json'):
        os.remove(name.name)

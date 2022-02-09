"""Генерация json-файла."""
import json

settings = {
    'input': r'input.jpg',
    'output': r'output.png',
    'mode': 'mirror',
    'size': [3, 3, 3]
}

# пишем в файл
with open('settings.json', 'w') as fp:
    json.dump(settings, fp)



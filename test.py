import re

text = 'Еда, я еду к еди'

match = re.findall("[е+Е]д[а+у]", text)

print(match)
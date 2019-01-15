#Not the prettiest thing ever written, I just considered this purely cosmetic and pretty non-essential to the actual functionality
def json_pretty(json):
    indentSize = 4
    indentPos = 0
    jsonString = str(json)
    for char in jsonString:
        if char in ['{', '[']:
            indentPos += indentSize
            print(char)
            print(end = ' ' * indentPos)

        elif char in ['}', ']']:
            indentPos -= indentSize
            print()
            print(' ' * indentPos, end = char)

        elif char == ',':
            print(char)
            print(end = ' ' * indentPos)

        elif char == ':':
            print(end = ': ')

        elif char == ' ':
            pass

        else:
            print(end = char)

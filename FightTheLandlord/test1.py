def convertToList(msg):
    new = []
    for value in msg.split(','):
        new.append(int(value))
    return new
keys = {"mesh":[[0, 'a', 1],[2, 0, 2],[2, 1, 1]], 'b':'string', 'thid_key':7}

def check(items):
    for point in items.get('mesh'):
        for coordinate in point:
            print(coordinate)
            try:
                float(coordinate)
            except ValueError:
                return False
    return True
print(check(keys) is True)
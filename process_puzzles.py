

def get_puzzle_sets_by_type(data):
    type_field = 3
    name_field = 0
    designer_field = 2
    producer_field = 1

    types = [row[type_field] for row in data]
    types = sorted(set(types))

    type_sets = {typed: [] for typed in types}

    for row in data:
        type_sets[row[type_field]].append(
            f"{row[name_field]} by {row[designer_field]} (prod. {row[producer_field]})"
        )

    return type_sets


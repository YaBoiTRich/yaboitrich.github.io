import csv
import json
import re

from process_puzzles import get_puzzle_sets_by_type
from process_records import get_record_sets_by_type


def process_collection_type(collection_type):
    # TODO: Go based off of headers versus the order in which the columns appear
    headers = []
    data = []
    sort_order = []

    if collection_type == "puzzles":
        sort_order = [3, 0]
        # Import simple data name,prod,des,type and format to type: []
        with open("./simplepuzzleinfo.tsv", "r") as file:
            csv_reader = csv.reader(file, delimiter="\t")
            headers = next(csv_reader)
            data = list(csv_reader)

    elif collection_type == "records":
        sort_order = [4, 2, 1]
        with open("./collection.csv", "r") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            data = list(csv_reader)
    else:
        print("Nothing to do")
        return

    # Sort by secondary column first, then primary (because sort is stable)
    for sort in sort_order:
        data.sort(key=lambda row: str.lower(row[sort]))

    if collection_type == "puzzles":
        type_sets = get_puzzle_sets_by_type(data)

    elif collection_type == "records":
        type_sets = get_record_sets_by_type(data)

    else:
        return

    # pprint(type_sets)
    collection_formatted = type_sets

    # Start the format of the main page
    collection_index_json = {
        "format": "particle",
        "title": str.upper(collection_type),
        "content": [],
    }

    collection_index_json["content"].append(
        {
            "type": "paragraph",
            "text": "Take a GANDER",
            "style": {
                "text-align": "center",
            },
        }
    )

    for item_type, items in collection_formatted.items():
        item_type_file_name = re.sub(r"[^\w]", "_", item_type)

        collection_index_json["content"].append(
            {
                "type": "button",
                "label": item_type,
                "action": f"/{collection_type}/{item_type_file_name}",
            }
        )

        item_type_index_json = {
            "format": "particle",
            "title": item_type,
            "content": [],
        }

        # Process chunks of 50
        chunk_size = 50
        for chunk in range(0, len(items), chunk_size):
            item_type_index_json["content"].append(
                {
                    "type": "paragraph",
                    "style": {"margin-top": 0, "margin-bottom": 0},
                    "text": "\n".join(
                        ["- " + item for item in items[chunk : chunk + chunk_size]]
                    ),
                }
            )

        item_type_index_json["content"].append(
            {"type": "button", "label": "Back", "action": f"/{collection_type}/"}
        )

        with open(f"./{collection_type}/{item_type_file_name}.json", "w") as file:
            json.dump(item_type_index_json, file, indent=4)

    with open(f"./{collection_type}/index.json", "w") as file:
        json.dump(collection_index_json, file, indent=4)


if __name__ == "__main__":
    for collection_type in ["puzzles", "records"]:
        process_collection_type(collection_type)

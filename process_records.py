import re
from kanjiconv import KanjiConv
from korean_romanizer.romanizer import Romanizer

KOR = re.compile(
    "[\uac00-\ud7a3|\u1100-\u11ff|\u3130-\u318f|\ua960-\ua97f|\ud7b0-\ud7ff]+"
)

kanji_conv = KanjiConv(separator="")
hiragana = re.compile("[\u3041-\u3096]")
katakana = re.compile("[\u30a0-\u30ff]")
CJK = re.compile("[\u4300-\u9faf]+[\u30a0-\u30ff|\u3041-\u3096]*")


def match_concise_format(full_format):
    vinyl_types = ["LP", '12"', '7"', '10"', '11"']
    other_types = ["CD"]
    novelty_types = ['1"', "Floppy"]

    match = re.search("Laserdisc", full_format)
    if match:
        return "Laserdisc"

    for typed in vinyl_types:
        match = re.search(typed, full_format)
        if match:
            return "Vinyl"

    match = re.search("MD", full_format)
    if match:
        return "MiniDisc"

    match = re.search("Cass", full_format)
    if match:
        return "Cassette"

    for typed in other_types:
        match = re.search(typed, full_format)
        if match:
            return typed

    for typed in novelty_types:
        match = re.search(typed, full_format)
        if match:
            return "Novelty"

    return None


def get_record_sets_by_type(data):
    type_field = 4
    artist_field = 1
    album_field = 2

    types = []
    for row in data:
        matched_type = match_concise_format(row[type_field])
        if matched_type:
            types.append(matched_type)

    types = sorted(set(types))

    type_sets = {typed: [] for typed in types}

    for row in data:
        matched_type = match_concise_format(row[type_field])
        if matched_type:
            artist = row[artist_field]
            artist = re.sub(r" \(\d*\)", "", artist)
            album = row[album_field]
            japanese_artist = CJK.findall(artist)
            japanese_album = CJK.findall(album)
            korean_artist = KOR.findall(artist)
            korean_album = KOR.findall(album)

            if japanese_artist:
                for match in japanese_artist:
                    hiragana = kanji_conv.to_hiragana(match)
                    artist = artist.replace(match, hiragana, 1)

            if japanese_album:
                for match in japanese_album:
                    hiragana = kanji_conv.to_hiragana(match)
                    album = album.replace(match, hiragana, 1)

            if korean_artist:
                for match in korean_artist:
                    artist = artist.replace(match, Romanizer(match).romanize(), 1)

            if korean_album:
                for match in korean_album:
                    album = album.replace(match, Romanizer(match).romanize(), 1)

            append_string = f"{artist} - {album}\n  // {row[type_field]}"
            type_sets[matched_type].append(append_string)

    return type_sets

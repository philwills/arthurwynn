from xml.etree.ElementTree import fromstring

from typing import Dict, Optional, Tuple

from dataclasses import dataclass
from enum import Enum, unique


@unique
class CrosswordType(Enum):
    QUICK = "quick"
    CRYPTIC = "cryptic"


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


@dataclass(frozen=True)
class Crossword:
    title: str
    type: Optional[CrosswordType]
    identifier: int
    creator: str
    height: int
    width: int
    letters: Dict[Coordinate, str]
    across_clues: Dict[str, str]
    down_clues: Dict[str, str]


_ns = "{http://crossword.info/xml/rectangular-puzzle}"


def parse(xml_string: str) -> Optional[Crossword]:
    root = fromstring(xml_string)
    puzzle = root.find(f"./{_ns}rectangular-puzzle")
    if puzzle:
        grid = puzzle.find(f"./{_ns}crossword/{_ns}grid")
        (across_clues, down_clues) = _extract_clues(puzzle)

        return Crossword(
            title=_title(puzzle),
            type=_type(puzzle),
            identifier=_identifier(puzzle),
            creator=_creator(puzzle),
            height=_height(grid),
            width=_width(grid),
            letters=_letters(grid),
            across_clues=across_clues,
            down_clues=down_clues,
        )
    else:
        return None


def _title(puzzle) -> str:
    type = _type(puzzle)
    type_name = type._value_.capitalize() if type else ""
    return f"{type_name} Crossword No. {_identifier(puzzle)}"


def _type(puzzle) -> Optional[CrosswordType]:
    titleText = puzzle.find(f"./{_ns}metadata/{_ns}title").text
    if titleText[0:4] == "gdn.":
        return CrosswordType(titleText[4:])
    else:
        return None


def _creator(puzzle) -> str:
    return puzzle.find(f"./{_ns}metadata/{_ns}creator").text


def _identifier(puzzle) -> int:
    return int(puzzle.find(f"./{_ns}metadata/{_ns}identifier").text)


def _width(grid) -> int:
    return int(grid.get("width"))


def _height(grid) -> int:
    return int(grid.get("height"))


def _letters(grid) -> Dict[Coordinate, str]:
    letters = {}
    for cell in grid.findall(f"./{_ns}cell"):
        if cell.get("solution"):
            letters[
                Coordinate(int(cell.get("x")) - 1, int(cell.get("y")) - 1)
            ] = cell.get("solution")
        else:
            letters[Coordinate(int(cell.get("x")) - 1, int(cell.get("y")) - 1)] = ""
    return letters


def _extract_clues(puzzle) -> Tuple[Dict[str, str], Dict[str, str]]:
    across_clue_dict: Dict[str, str] = {}
    down_clue_dict: Dict[str, str] = {}
    for clues in puzzle.findall(f"./{_ns}crossword/{_ns}clues"):
        if clues.find(f"./{_ns}title/{_ns}b").text == "Across":
            for clue in clues.findall(f"./{_ns}clue"):
                _add_clue(across_clue_dict, clue)
        else:
            for clue in clues.findall(f"./{_ns}clue"):
                _add_clue(down_clue_dict, clue)
    return (across_clue_dict, down_clue_dict)


def _add_clue(clue_dict, clue):
    clue_numbers = clue.get("number").split(",")
    clue_dict[clue_numbers[0]] = _get_clue_text(clue)
    if (
        len(clue_numbers) > 1
        and clue_numbers[1] not in clue_dict
        and not clue_numbers[1].endswith("down")
    ):
        clue_dict[clue_numbers[1]] = f"See {clue_numbers[0]}"


def _get_clue_text(clue):
    format = clue.get("format")
    if format:
        return f"{clue.text} ({format})"
    else:
        return clue.text

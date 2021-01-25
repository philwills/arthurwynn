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

class CrosswordDotInfoXmlExtractor:
    ns = "{http://crossword.info/xml/rectangular-puzzle}"

    def parse(self, xml_string) -> Crossword:
        self.root = fromstring(xml_string)
        self.puzzle = self.root.find(f"./{self.ns}rectangular-puzzle")
        self.grid = self.puzzle.find(f"./{self.ns}crossword/{self.ns}grid")
        self.across_clue_dict = {}
        self.down_clue_dict = {}
        self._extract_clues()
        return Crossword(
            title=self.title(),
            type = self.type(),
            identifier = self.identifier(),
            creator = self.creator(),
            height = self.height,
            width = self.width,
            letters = self.letters(),
            across_clues = self.across_clues(),
            down_clues = self.down_clues(),
        )

    def title(self) -> str:
        return f"{self.type()._value_.capitalize()} Crossword No. {self.identifier()}"

    def type(self) -> Optional[CrosswordType]:
        titleText = self.puzzle.find(f"./{self.ns}metadata/{self.ns}title").text
        if titleText[0:4] == "gdn.":
            return CrosswordType(titleText[4:])
        else:
            return None

    def creator(self) -> str:
        return self.puzzle.find(f"./{self.ns}metadata/{self.ns}creator").text

    def identifier(self) -> int:
        return int(self.puzzle.find(f"./{self.ns}metadata/{self.ns}identifier").text)

    def width(self) -> int:
        return int(self.grid.get("width"))

    def height(self) -> int:
        return int(self.grid.get("height"))

    def letters(self) -> Dict[Coordinate, str]:
        letters = {}
        for cell in self.grid.findall(f"./{self.ns}cell"):
            if cell.get("solution"):
                letters[
                    Coordinate(int(cell.get("x")) - 1, int(cell.get("y")) - 1)
                ] = cell.get("solution")
            else:
                letters[Coordinate(int(cell.get("x")) - 1, int(cell.get("y")) - 1)] = ""
        return letters

    def across_clues(self) -> Dict[int, str]:
        return self.across_clue_dict

    def down_clues(self) -> Dict[int, str]:
        return self.down_clue_dict

    def _extract_clues(self):
        for clues in self.puzzle.findall(f"./{self.ns}crossword/{self.ns}clues"):
            if clues.find(f"./{self.ns}title/{self.ns}b").text == "Across":
                for clue in clues.findall(f"./{self.ns}clue"):
                    self._add_clue(self.across_clue_dict, clue)
            else:
                for clue in clues.findall(f"./{self.ns}clue"):
                    self._add_clue(self.down_clue_dict, clue)

    def _add_clue(self, clue_dict, clue):
        clue_numbers = clue.get("number").split(",")
        clue_dict[clue_numbers[0]] = self._get_clue_text(clue)
        if (
            len(clue_numbers) > 1
            and clue_numbers[1] not in clue_dict
            and not clue_numbers[1].endswith("down")
        ):
            clue_dict[clue_numbers[1]] = f"See {clue_numbers[0]}"

    def _get_clue_text(self, clue):
        format = clue.get("format")
        if format:
            return f"{clue.text} ({format})"
        else:
            return clue.text

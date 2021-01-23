from xml.etree.ElementTree import fromstring


class CrosswordDotInfoXmlExtractor:
    ns = "{http://crossword.info/xml/rectangular-puzzle}"

    def parse(self, xml_string):
        self.root = fromstring(xml_string)
        self.puzzle = self.root.find(f"./{self.ns}rectangular-puzzle")
        self.grid = self.puzzle.find(f"./{self.ns}crossword/{self.ns}grid")
        self.across_clue_dict = {}
        self.down_clue_dict = {}
        self.extract_clues()

    def title(self):
        return f"{self.type().capitalize()} Crossword No. {self.identifier()}"

    def type(self):
        titleText = self.puzzle.find(f"./{self.ns}metadata/{self.ns}title").text
        if titleText[0:4] == "gdn.":
            return titleText[4:]

    def creator(self):
        return self.puzzle.find(f"./{self.ns}metadata/{self.ns}creator").text

    def identifier(self):
        return int(self.puzzle.find(f"./{self.ns}metadata/{self.ns}identifier").text)

    def width(self):
        return int(self.grid.get("width"))

    def height(self):
        return int(self.grid.get("height"))

    def letters(self):
        letters = {}
        for cell in self.grid.findall(f"./{self.ns}cell"):
            if cell.get("solution"):
                letters[int(cell.get("x")) - 1, int(cell.get("y")) - 1] = cell.get(
                    "solution"
                )
            else:
                letters[int(cell.get("x")) - 1, int(cell.get("y")) - 1] = ""
        return letters

    def across_clues(self):
        return self.across_clue_dict

    def down_clues(self):
        return self.down_clue_dict

    def extract_clues(self):
        for clues in self.puzzle.findall(f"./{self.ns}crossword/{self.ns}clues"):
            if clues.find(f"./{self.ns}title/{self.ns}b").text == "Across":
                for clue in clues.findall(f"./{self.ns}clue"):
                    self.add_clue(self.across_clue_dict, clue)
            else:
                for clue in clues.findall(f"./{self.ns}clue"):
                    self.add_clue(self.down_clue_dict, clue)

    def add_clue(self, clue_dict, clue):
        clue_numbers = clue.get("number").split(",")
        clue_dict[clue_numbers[0]] = self.get_clue_text(clue)
        if (
            len(clue_numbers) > 1
            and clue_numbers[1] not in clue_dict
            and not clue_numbers[1].endswith("down")
        ):
            clue_dict[clue_numbers[1]] = f"See {clue_numbers[0]}"

    def get_clue_text(self, clue):
        format = clue.get("format")
        if format:
            return f"{clue.text} ({format})"
        else:
            return clue.text

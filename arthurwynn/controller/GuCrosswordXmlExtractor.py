from xml.etree.ElementTree import fromstring


class GuCrosswordXmlExtractor:
    def parse(self, xml_string):
        self.root = fromstring(xml_string)
        self.words = self.root.findall("./body/word")

    def title(self):
        return self.root.find("./header/title").text

    def type(self):
        return self.root.attrib["type"]

    def creator(self):
        return self.root.find("./header/author").text

    def identifier(self):
        return int(self.root.attrib["serial"])

    def width(self):
        return int(self.root.find("./header/grid").attrib["cols"])

    def height(self):
        return int(self.root.find("./header/grid").attrib["rows"])

    def across_words(self):
        return [word for word in self.words if word.attrib["direction"] == "across"]

    def down_words(self):
        return [word for word in self.words if word.attrib["direction"] == "down"]

    def nums(self, words):
        return [int(word.attrib["number"]) for word in words]

    def x(self, words):
        return [int(word.attrib["x"]) for word in words]

    def y(self, words):
        return [int(word.attrib["y"]) for word in words]

    def clue(self, words):
        return [word.find("clue").text for word in words]

    def solution(self, words):
        return [word.find("solution").text for word in words]

    def across_nums(self):
        return self.nums(self.across_words())

    def down_nums(self):
        return self.nums(self.down_words())

    def across_x(self):
        return self.x(self.across_words())

    def down_x(self):
        return self.x(self.down_words())

    def across_y(self):
        return self.y(self.across_words())

    def down_y(self):
        return self.y(self.down_words())

    def across_clues(self):
        return self.clue(self.across_words())

    def down_clues(self):
        return self.clue(self.down_words())

    def across_solutions(self):
        return self.solution(self.across_words())

    def down_solutions(self):
        return self.solution(self.down_words())

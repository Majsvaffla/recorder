from mistune import Markdown, preprocessing


class ParserWithoutBody(Markdown):
    def parse(self, text):
        return self.output(preprocessing(text))

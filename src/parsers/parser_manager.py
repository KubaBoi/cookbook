
from src.parsers.top_recepty_parser import TopReceptyParser
from src.parsers.apetit_parser import ApetitParser

class ParserManager:

    PARSERS = [
        TopReceptyParser,
        ApetitParser
    ]

    @staticmethod
    def parse(url: str) -> str:
        for parser in ParserManager.PARSERS:
            if (parser.match(url)):
                return parser.parse(url)
        return None
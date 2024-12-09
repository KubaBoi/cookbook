from src.parsers.parser_manager import ParserManager
from src.tools.downloader import Downloader

Downloader.save("https://www.apetitonline.cz/recept/bleskovy-ovocny-kolac-s-drobenkou")

print(
    ParserManager.parse(
        "https://www.apetitonline.cz/recept/bleskovy-ovocny-kolac-s-drobenkou"
    )
)
#parser.parse("https://www.toprecepty.cz/recept/12390-nadychana-piskotova-rolada/")
import os
import json
import uuid
from bs4 import BeautifulSoup

from Cheese.resourceManager import ResMan

from src.tools.downloader import Downloader

class IParser:

    @staticmethod
    def get_body(url: str) -> BeautifulSoup:
        return IParser.get_site(url).body
    
    @staticmethod
    def get_head(url: str) -> BeautifulSoup:
        return IParser.get_site(url).head
    
    @staticmethod
    def get_site(url: str) -> BeautifulSoup:
        html = Downloader.download(url)
        return BeautifulSoup(html, features="html.parser")
    
    @staticmethod
    def save_json(recipe: dict) -> str:
        id = str(uuid.uuid4())
        path = ResMan.web("files", f"{id}.json")
        while (os.path.exists(path)):
            id = str(uuid.uuid4())

        recipe["id"] = id
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(recipe, ensure_ascii=False))
        return recipe["id"]
    
    @staticmethod
    def parse_amount(amount_str: str) -> float:
        try:
            if (amount_str is None):
                return None
            
            if (amount_str == "½"):
                return 0.5
            
            if ("/" in amount_str):
                vals = amount_str.split("/")
                return float(vals[0]) / float(vals[1])

            amount_str = amount_str.replace(",", ".")

            return float(amount_str)
        except Exception as e:
            print(e)
            return None

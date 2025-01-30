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
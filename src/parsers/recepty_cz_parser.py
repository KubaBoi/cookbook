import re
import json
from bs4 import BeautifulSoup

from src.parsers.iparser import IParser

class ReceptyCzParser:

    @staticmethod
    def match(url: str) -> bool:
        return url.startswith("https://www.recepty.cz")
    
    @staticmethod
    def parse(url: str) -> str:
        site = IParser.get_site(url)
        head = site.head
        body = site.body

        script = head.find("script", attrs={"type": "application/ld+json"})
        dc = json.loads(script.text)

        ingredients = ReceptyCzParser.parse_ingredients(dc)
        steps = ReceptyCzParser.parse_steps(dc)
        header = ReceptyCzParser.parse_header(dc, body)

        recipe = ingredients
        recipe["name"] = dc["name"]
        recipe["header"] = header
        recipe["steps"] = steps
        recipe["source"] = url
        
        return IParser.save_json(recipe)
    
    @staticmethod
    def parse_ingredients(parsed_json: dict) -> dict:
        ingredients = parsed_json["recipeIngredient"]

        res = {"ingredients": []}

        for ing in ingredients:
            vals = ing.split(" ")
            if (vals[0].isnumeric()): # 1 ks kukurice na spizu 
                res["ingredients"].append({
                "name": " ".join(vals[2:]), 
                "amount": int(vals[0]),
                "unit": vals[1]})
            else: # "pepr mlety"
                res["ingredients"].append({
                    "name": ing, 
                    "amount": None,
                    "unit": None})
        return res
    
    @staticmethod
    def parse_steps(parsed_json: dict) -> list:
        steps = parsed_json["recipeInstructions"]
        res = []

        splt = re.search(r"\.\S", steps)
        while splt is not None:
            part = steps[0:splt.start() + 1]
            res.append(part)
            steps = steps[splt.end() - 1:]
            splt = re.search(r"\.\S", steps)
        res.append(steps)
        return res
    
    @staticmethod
    def parse_header(parsed_json: dict, parsed_html: BeautifulSoup) -> dict:
        duration_div = parsed_html.find("div", attrs={"class": "recipe-header__time"})
        difficulty_div = parsed_html.find("div", attrs={"class": "recipe-header__nutritional-value"})

        header = {}
        header["duration"] = duration_div.find_all("span")[1].text
        header["difficulty"] = difficulty_div.find_all("span")[1].text
        header["portions"] = None
        header["portion_unit"] = None

        portions = parsed_json["recipeYield"].split(" ")
        if (len(portions) > 0):
            header["portions"] = int(portions[0])
        if (len(portions) > 1):
            header["portion_unit"] = portions[1]

        return header
import re
import json

from src.parsers.iparser import IParser

class ReceptyCzParser:

    @staticmethod
    def match(url: str) -> bool:
        return url.startswith("https://www.recepty.cz")
    
    @staticmethod
    def parse(url: str) -> str:
        head = IParser.get_head(url)

        script = head.find("script", attrs={"type": "application/ld+json"})
        dc = json.loads(script.text)

        ingredients = ReceptyCzParser.parse_ingredients(dc)
        steps = ReceptyCzParser.parse_steps(dc)

        recipe = ingredients
        recipe["name"] = dc["name"]
        recipe["steps"] = steps
        recipe["source"] = url
        
        return IParser.save_json(recipe)
    
    @staticmethod
    def parse_ingredients(parsed_json: dict) -> dict:
        portions = re.findall(r"\d+", parsed_json["recipeYield"])
        if (len(portions) > 0):
            portions = portions[0]
        else:
            portions = None

        ingredients = parsed_json["recipeIngredient"]

        res = {"portions": portions, "ingredients": []}

        for ing in ingredients:
            vals = ing.split(" ")
            name = " ".join(vals[2:])
            quant = " ".join(vals[:2])
            res["ingredients"].append((name, quant))
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
    def parse_header(parsed_json: dict) -> dict:
        pass
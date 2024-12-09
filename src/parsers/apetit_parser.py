import json
from bs4 import BeautifulSoup

from src.parsers.iparser import IParser

class ApetitParser:

    @staticmethod
    def match(url: str) -> bool:
        return url.startswith("https://www.apetitonline.cz")
    
    @staticmethod
    def parse(url: str) -> str:
        body = IParser.get_body(url)

        name = ApetitParser.parse_name(body)
        ingredients = ApetitParser.parse_ingredients(body)
        steps = ApetitParser.parse_steps(body)

        recipe = ingredients
        recipe["name"] = name
        recipe["steps"] = steps
        return IParser.save_json(recipe)

    @staticmethod
    def parse_name(parsed_html: BeautifulSoup) -> str:
        header = parsed_html.find("h1", attrs={"class": "s-recipe-header__title"})
        return header.text.strip()
    
    @staticmethod
    def parse_ingredients(parsed_html: BeautifulSoup) -> dict:
        """
        Seznam ingredienci je v <div> s class="s-recipe__ingredients-items".

        Uvnitr je seznam <div> s class="s-recipe__ingredients-item". 
        Pokud je zaroven pritomna trida s-recipe__ingredients-item--subtitle"
        pak je div nadpis

        Nenadpisove divy, maji v sobe <strong> a dva <span> s prisluslnymi classami

        Vraci slovnik
        """
        main_div = parsed_html.find("div", attrs={"class": "s-recipe__ingredients-items"})
        divs = main_div.find_all("div", attrs={"class": "s-recipe__ingredients-item"})

        res = {"portions": None, "ingredients": []}
        for div in divs:
            if ("s-recipe__ingredients-item--subtitle" in div["class"]):
                res["ingredients"].append((div.text.strip(), None))
                continue
            
            name = div.find("strong").text
            quant = div.find("span", attrs={"class": "s-recipe__ingredients-quantity"}).text
            unit = div.find("span", attrs={"class": "s-recipe__ingredients-unit"}).text
            res["ingredients"].append((name, f"{quant} {unit}"))

        return res
    
    @staticmethod
    def parse_steps(parsed_html: BeautifulSoup) -> list:
        """
        Seznam kroků je v <div>

        Uvnitr jednotlicych divu je 1-n <p> a v tech jsou texty.
        Parser vnima kazde <p> jako samostatny krok.
        """
        main_div = parsed_html.find("div", attrs={"class": "s-recipe__process-steps"})
        steps = main_div.find_all("div", attrs={"class": "s-recipe__process-step"})

        res = []
        for step in steps:
            ps = step.find_all("p")
            for p in ps:
                res.append(p.text.strip().replace("\n", "<br>"))
        return res
    
ApetitParser.parse("https://www.apetitonline.cz/recept/bleskovy-ovocny-kolac-s-drobenkou")
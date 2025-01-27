import re
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
        header = ApetitParser.parse_header(body)

        recipe = ingredients
        recipe["name"] = name
        recipe["header"] = header
        recipe["steps"] = steps
        recipe["source"] = url
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

        res = {"ingredients": []}
        for div in divs:
            if ("s-recipe__ingredients-item--subtitle" in div["class"]):
                res["ingredients"].append((div.text.strip(), None))
                continue
            
            name = div.find("strong").text
            quant = None
            unit = None

            quant_span = div.find("span", attrs={"class": "s-recipe__ingredients-quantity"})
            if (quant_span is not None):
                quant = quant_span.text
            
            unit_span = div.find("span", attrs={"class": "s-recipe__ingredients-unit"})
            if (unit_span is not None):
                unit = unit_span.text
            
            res["ingredients"].append((name, f"{quant} {unit}".strip()))

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
    
    @staticmethod
    def parse_header(parsed_html: BeautifulSoup) -> dict:
        header_div = parsed_html.find("div", attrs={"class": "s-recipe-header__info-items"})
        spans = header_div.find_all("span")

        header = {}
        header["duration"] = spans[0].text.strip()
        header["difficulty"] = spans[1].text.strip()
        header["portions"] = None
        header["portion_unit"] = None
        port_text = spans[2].text.strip()

        portions = port_text.split(" ")
        if (len(portions) > 1):
            header["portions"] = int(portions[1])
        if (len(portions) > 2):
            header["portion_unit"] = portions[2]

        return header
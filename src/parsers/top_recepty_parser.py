import re
from bs4 import BeautifulSoup

from src.parsers.iparser import IParser

class TopReceptyParser:

    @staticmethod
    def match(url: str) -> bool:
        return url.startswith("https://www.toprecepty.cz")

    @staticmethod
    def parse(url: str) -> str:
        body = IParser.get_body(url)

        name = TopReceptyParser.parse_name(body)
        ingredients = TopReceptyParser.parse_ingredients(body)
        steps = TopReceptyParser.parse_steps(body)
        header = TopReceptyParser.parse_header(body)

        recipe = ingredients
        recipe["name"] = name
        recipe["header"] = header
        recipe["steps"] = steps
        recipe["source"] = url

        return IParser.save_json(recipe)

    @staticmethod
    def parse_name(parsed_html: BeautifulSoup) -> str:
        header = parsed_html.find("h1", attrs={"class": "b-recipe-info__title"})
        return header.text.strip()

    @staticmethod
    def parse_ingredients(parsed_html: BeautifulSoup) -> dict:
        """
        Seznam ingrediencí je v <div> s id="ingredients". 
        Pocet porci je v <h2 class="b-ingredients__title"><span>.

        Seznam je za sebou v <div class="u-mb-last-0"><p>. 
        Tento seznam se pak prochazi a pokud dane <p> obsahuje tridu "b-ingredients__item--title"
        pak je to popisek sekce ingredienci.

        Pokud <p> tu tridu neobsahuje, pak je to prisada. 
        Toto <p> se potom prevede na text a rozdeli podle \\n.
        
        Ingredience se bud sklada z jednoho stringu a nebo 3 stringu,
        kde prvni dva jsou stejne a jsou to pocty a posledni string je nazev prisady.

        Vraci slovnik
        """
        ingredients = parsed_html.find("div", attrs={"id": "ingredients"})

        ps = ingredients.find("div", attrs={"class": "u-mb-last-0"}).find_all("p")

        res = {"ingredients": []}
        for p in ps:
            if ("b-ingredients__item--title" in p["class"]):
                # title (napr Testicko: )
                res["ingredients"].append((p.text.strip(), None))
            else:
                ings = p.text.strip().split("\n")
                if (len(ings) > 1):
                    # ingredience s poctem
                    # (ingredience, pocet)
                    res["ingredients"].append((ings[-1].strip(), ings[0]))
                else:
                    # ingredience bez poctu
                    # (ingredience, "")
                    res["ingredients"].append((ings[0].strip(), ""))
        return res
    
    @staticmethod
    def parse_steps(parsed_html: BeautifulSoup) -> list:
        """
        Kroky postupu jsou zapsany v <div> s id="steps". Uvnitr tohoto divu
        je <ol> a kazdy <li> uvnitr ma v sobe <label><span><span> ve kterem
        je jeden krok.

        Vraci seznam textu
        """
        steps = parsed_html.find("div", attrs={"id": "steps"})
        lis = steps.find("ol").find_all("li")

        res = []
        for li in lis:
            res.append(li.find("label").find("span").find("span").text.strip())
        return res
            
    @staticmethod
    def parse_header(parsed_html: BeautifulSoup) -> list:
        duration_p = parsed_html.find("p", attrs={"class": "b-recipe-info__time"})
        difficulty_p = parsed_html.find("p", attrs={"class": "b-recipe-info__difficulty"})

        header = {}
        header["duration"] = duration_p.find_all("span")[1].text.strip().split("\t")[-1]
        header["difficulty"] = difficulty_p.find_all("span")[1].text.strip()
        header["portions"] = None
        header["portion_unit"] = None

        ingredients = parsed_html.find("div", attrs={"id": "ingredients"})
        portions_text = ingredients.find("h2", attrs={"class": "b-ingredients__title"}).find("span").text.strip()
        portions = portions_text.split(" ")
        if (len(portions) > 1):
            header["portions"] = int(portions[1])
        if (len(portions) > 2):
            header["portion_unit"] = portions[2]

        return header

    
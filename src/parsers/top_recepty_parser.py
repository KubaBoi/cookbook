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

        recipe = ingredients
        recipe["name"] = name
        recipe["steps"] = steps
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

        portions_text = ingredients.find("h2", attrs={"class": "b-ingredients__title"}).find("span").text.strip()
        portions = re.findall(r"\d+", portions_text)
        if (len(portions) > 0):
            portions = portions[0]

        ps = ingredients.find("div", attrs={"class": "u-mb-last-0"}).find_all("p")

        res = {"portions": portions, "ingredients": []}
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
            


    
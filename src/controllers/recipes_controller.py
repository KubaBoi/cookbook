import os
import json
import requests

from Cheese.httpClientErrors import *
from Cheese.cheeseController import CheeseController as cc
from Cheese.resourceManager import ResMan

from src.parsers.parser_manager import ParserManager
from src.tools.downloader import Downloader

#@controller /recipes;
class RecipesController(cc):

    #@get /get;
    @staticmethod
    def get_recipes(server, path, auth):
        """
        Return list of names of saved recipes.
        """
        fls = ResMan.web("files")
        r = []
        for root, dir, files in os.walk(fls):
            for file in files:
                r.append(".".join(file.split(".")[:-1]))
        return cc.createResponse({"recipes_names": r}, 200, {"Content-type": "application/json"})
    
    #@get /get_recipe;
    @staticmethod
    def get_recipe(server, path, auth):
        """
        Return details one recipe.

        /recipes/get_recipe?name=jmeno
        """
        args = cc.getArgs(path)
        cc.checkJson(["name"], args)

        data = RecipesController.read_file(args["name"])
        return cc.createResponse(data, 200, {"Content-type": "application/json"})
    
    #@post /post_recipe;
    @staticmethod
    def post_recipe(server, path, auth):
        """
        Parse new recipe from give url.

        {
            "url": "https://url"
        }
        """
        body = cc.readArgs(server)
        cc.checkJson(["url"], body)

        name = ParserManager.parse(body["url"])
        if (name is None):
            raise NotFound("Parser was not found")
        return cc.createResponse({"name": name}, 201, {"Content-type": "application/json"})

    #@get /proxy;
    @staticmethod
    def proxy(server, path, auth):
        url = "https://www.recepty.cz/recept/rychla-babovka-2-3875"
        res = Downloader.download(url)
        return cc.createResponse({"data": res})

    # private methods

    @staticmethod
    def read_file(name: str) -> dict:
        with open(ResMan.web("files", f"{name}.json"), "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        return data
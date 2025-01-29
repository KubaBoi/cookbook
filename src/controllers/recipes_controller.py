import os
import json
import requests

from Cheese.httpClientErrors import *
from Cheese.cheeseController import CheeseController as cc
from Cheese.resourceManager import ResMan

from src.parsers.parser_manager import ParserManager

#@controller /recipes;
class RecipesController(cc):

    #@get /get_all;
    @staticmethod
    def get_all_recipes(server, path, auth):
        """
        Return all recipes.
        """
        fls = ResMan.web("files")
        r = []
        for root, dir, files in os.walk(fls):
            for file in files:
                data = RecipesController.read_file(os.path.join(dir, file))
                r.append(data)
        return cc.createResponse({"recipes": r}, 200, {"Content-type": "application/json"})

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

    # private methods

    @staticmethod
    def read_file(name: str) -> dict:
        with open(ResMan.web("files", f"{name}.json"), "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        return data
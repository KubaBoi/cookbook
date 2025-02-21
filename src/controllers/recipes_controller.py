import os
import json
import requests

from Cheese.httpClientErrors import *
from Cheese.cheeseController import CheeseController as cc
from Cheese.resourceManager import ResMan

from src.parsers.parser_manager import ParserManager

#@controller /recipes;
class RecipesController(cc):

    #@get /getAll;
    @staticmethod
    def get_all_recipes(server, path, auth):
        """
        Return all recipes.
        """
        fls = ResMan.web("files")
        r = []
        for root, dir, files in os.walk(fls):
            for file in files:
                data = RecipesController.read_file(file)
                r.append(data)
        return cc.createResponse(r, 200, {"Content-type": "application/json"})
    
    #@get /getRecipe;
    @staticmethod
    def get_recipe(server, path, auth):
        """
        Return details one recipe.

        /recipes/getRecipe?id=id
        """
        args = cc.getArgs(path)
        cc.checkJson(["id"], args)

        data = RecipesController.read_file(args["name"])
        return cc.createResponse(data, 200, {"Content-type": "application/json"})
    
    #@post /postRecipe;
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

        id = ParserManager.parse(body["url"])
        if (id is None):
            raise NotFound("Parser was not found")
        return cc.createResponse({"id": id}, 201, {"Content-type": "application/json"})

    # private methods

    @staticmethod
    def read_file(name: str) -> dict:
        if (not name.endswith("json")):
            name = f"{name}.json"

        with open(ResMan.web("files", name), "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        return data
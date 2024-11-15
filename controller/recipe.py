from typing import Annotated
import uuid

from pydantic import UUID4

from fastapi import Depends

from modals import Recipie, UpdateRecipie
from database.recipe import RecipiessFunction

from controller.auth import is_owner_of_recipe

class Recipe:
    
    def create_recipe(recipe: Recipie):   
        ''' Create new recipe '''     
        created_recipe = RecipiessFunction.create_recipe(recipe)
        return created_recipe
    
    def get_all_recipes(page: int, limit: int):
        ''' 
            Get all recipes 
            supports pagination as url query parameters
            ` ?page=1&limit=10 `
        '''
        recipies = RecipiessFunction.get_all_recipes(page, limit)
        return recipies
        
    def get_recipe_by_id(recipe_id: UUID4):
        ''' Get recipe by id '''
        recipe = RecipiessFunction.get_recipe_by_id(recipe_id)
        return recipe
    
    @is_owner_of_recipe
    def update_recipe(recipe_id: UUID4, recipe: UpdateRecipie, Token: Annotated[str, Depends]):        
        ''' Update recipe by id '''
        updated_recipe = RecipiessFunction.update_recipe(recipe_id, recipe)
        return updated_recipe
    
    @is_owner_of_recipe
    def delete_recipe(recipe_id: UUID4, Token: Annotated[str, Depends]):
        ''' Delete recipe by id '''
        deleted_recipe = RecipiessFunction.delete_recipe(recipe_id)
        return deleted_recipe
    
    def search_recipies(query: str, page: int, limit: int):
        ''' Search recipes in the database (name, ingredients, instructions) '''
        recipies = RecipiessFunction.search_recipies(query, page, limit)
        return recipies
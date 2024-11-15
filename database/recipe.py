from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

from pydantic import UUID4

from database.engine import engine
from database.utils import recipe_to_json, load_initial_data

from modals import DBRecipeModal

class RecipiessFunction:
    
    @load_initial_data
    def create_recipe(recipe: DBRecipeModal):
        '''  
            Create new recipe 
            ```json
                {
                    "name": "Recipe Name",
                    "ingredients": "Ingredients",
                    "instructions": "Instructions",
                }
            ```
        '''
        with Session(engine) as session:
            query = insert(DBRecipeModal).values(**recipe.dict())
            result = session.execute(query)
            session.commit()
        return result
    
    def get_all_recipes(page: int, limit: int):
        '''
            Databse function to get all recipes and support pagination using 
            offset and limit functionality of sqlalchemy
        '''
        
        offset = (page - 1) * limit
        
        with engine.connect() as conn:
            query = select(DBRecipeModal).limit(limit).offset(offset)
            result = conn.execute(query)
            rows = result.fetchall()
            if not rows:
                return {"message": "No recipes found"}
            fetched_result = recipe_to_json(rows, many=True)
        return fetched_result
    
    def get_recipe_by_id(recipe_id: UUID4):
        ''' Databse call to Get recipe by id '''
        with engine.connect() as conn:
            query = select(DBRecipeModal).where(DBRecipeModal.id == str(recipe_id))
            result = conn.execute(query, {"id": recipe_id})
            recpie = result.first()
            if not recpie:
                return {"message": "Recipe not found"}
            fetched_result = recipe_to_json(recpie)
        return fetched_result
    
    def update_recipe(recipe_id: UUID4, recipe: DBRecipeModal):
        ''' Databse call to Update recipe by id '''
        with Session(engine) as session:
            recipe_dict = {key: value for key, value in recipe.dict().items() if value is not None}
            query = update(DBRecipeModal).where(DBRecipeModal.id == str(recipe_id)).values(**recipe_dict)
            result = session.execute(query)
            session.commit()
        return result
    
    
    def delete_recipe(recipe_id: UUID4):
        ''' Databse call to Delete recipe by id '''
        with Session(engine) as session:
            query = delete(DBRecipeModal).where(DBRecipeModal.id == str(recipe_id))
            session.execute(query)
            session.commit()
        return {"success": True}
    
    def search_recipies(query: str, page: int, limit: int):
        ''' Databse call to Search recipes in the database (name, ingredients, instructions) '''
        offset = (page - 1) * limit
        
        with engine.connect() as conn:
            query = select(DBRecipeModal).where(
                DBRecipeModal.name.ilike(f"%{query}%") |
                DBRecipeModal.ingredients.ilike(f"%{query}%") |
                DBRecipeModal.instructions.ilike(f"%{query}%")
            ).limit(limit).offset(offset)
            result = conn.execute(query)
            rows = result.fetchall()
            if not rows:
                return {"message": "No recipes found"}
            fetched_result = recipe_to_json(rows, many=True)
        return fetched_result
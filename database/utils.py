import uuid
from datetime import datetime, timezone

def recipe_to_json(recipes, many=False):
    '''
    Function to convert recipe object to json
    '''
    if not many:
        return {
            "id": recipes.id,
            "name": recipes.name,
            "ingredients": recipes.ingredients,
            "instructions": recipes.instructions,
            "owner_id": recipes.owner_id,
            "created_at": recipes.created_at,
        }    
    return [{
        "id": recipe.id,
        "name": recipe.name,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "owner_id": recipe.owner_id,
        "created_at": recipe.created_at,
    } for recipe in recipes]
    

def load_initial_data(function):
    '''
    Decorator to load initial data
    '''
    def wrapper(*args, **kwargs):
        args[0].id = str(uuid.uuid4())
        args[0].created_at = datetime.now(timezone.utc)
        return function(*args, **kwargs)
        
    return wrapper
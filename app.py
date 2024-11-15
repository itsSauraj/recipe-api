from datetime import timedelta

from typing import Annotated
from pydantic import UUID4

from controller.auth import Auth as auth, ACCESS_TOKEN_EXPIRE_MINUTES, is_owner_of_recipe
from controller.recipe import Recipe
from modals import Token, UserInDB, Recipie as RecipieModal, UpdateRecipie as UpdateRecipieModal

from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config import FastAPIConfig

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

description = """
### Recipe API (database: SQLite, ORM: SQLAlchemy, framework: FastAPI)
<hr /> 

**This project is a simple recipe API that allows users to create, read, update, and delete recipes. So, 
I kindly request you to take care of it. It is not the very best api's out there.**
<br />
The database used in this project is SQLite, and the ORM used is SQLAlchemy.

* This is a fast api project that allows users to create, read, update, and delete recipes.
* The API supports user registration and authentication using JWT tokens.
* This API supports pagination for the recipes endpoint.
* The API supports searching for recipes by name, ingredients, or instructions.

### Endpoints
<hr />

* **GET** `/` - Welcome message
* **POST** `/register` - Register a new user
* **POST** `/token` - Get access token
* **POST** `/recipe` - Add a new recipe
* **GET** `/recipes` - Get all recipes
* **GET** `/recipe/{recipe_id}` - Get a recipe by id
* **PATCH** `/recipe/{recipe_id}` - Update a recipe by id
* **DELETE** `/recipe/{recipe_id}` - Delete a recipe by id
* **GET** `/recipie/search` - Search for recipes
"""

print(FastAPIConfig.app_description)
print(description == FastAPIConfig.app_description)

app = FastAPI(    
    title=FastAPIConfig.app_title,
    version=FastAPIConfig.app_version,
    summary=FastAPIConfig.app_summary,
    license_info=FastAPIConfig.app_license_info,
    contact=FastAPIConfig.app_contact_info,
    description=FastAPIConfig.app_description,
    openapi_tags=FastAPIConfig.app_tags_metadata
)

@app.get("/", tags=["* Welcome"])
def Welcome():
    ''' This function is used to get the root path of the API and just returns a welcome message '''
    return {"message": "Welcome to the Recipe API"}


#########################################################################################################################
# -------------------------------------------------USER----------------------------------------------------------------
#########################################################################################################################


@app.post("/token", tags=["User Authentication"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    ''' This function is used to get the access token for the user '''
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/register", tags=["User Authentication"])
async def register_user(user: UserInDB):
    ''' 
        ### This function is used to register a new user
        The body of the request should be in the following format:
        ```json
        {
            "name": "John Doe",
            "email": "jhondoe@gmail.com",
            "password": "password"
        }
    '''
    register = auth.register_user(user)
    auth_user = auth.authenticate_user(user.email, user.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



#########################################################################################################################
# -------------------------------------------------RECIPE----------------------------------------------------------------
#########################################################################################################################


@app.post("/recipe", tags=["Recipe"])
async def add_recipe(recipe: RecipieModal, Token: Annotated[str, Depends(oauth2_schema)]):
    '''
        ### This function is used to add a new recipe
        - It requires a token to be passed in the header
        ```json
        Authorization: Bearer <token>
        ```
        The body of the request should be in the following format:
        ```json
            {
                "name": "Recipe Name",
                "ingredients": "Ingredients",
                "instructions": "Instructions",
            }
            or
            {
                "name": "Recipe Name",
            }
            or
            {
                "ingredients": "Ingredients",
            }
            or
            {
                "instructions": "Instructions",
            }
            or
            {
                "name": "Recipe Name",
                "ingredients": "Ingredients",
            }
            or
            {
                "name": "Recipe Name",
                "instructions": "Instructions",
            }
            or
            {
                "ingredients": "Ingredients",
                "instructions": "Instructions",
            }
        ```
    '''
    user = auth.get_current_user(Token)
    recipe.owner_id = user.id
    
    created_recipe = Recipe.create_recipe(recipe)
    return created_recipe


@app.get("/recipes", tags=["Recipe"])
async def get_all_recipes(page: int = 1, limit: int = 10):
    '''
        ### This function is used to get all recipes
        It supports pagination using query parameters
        ` ?page=1&limit=10 `
    '''
    recipes = Recipe.get_all_recipes(page, limit)
    return recipes

@app.get("/recipe/{recipe_id}", tags=["Recipe"])
async def get_recipe(recipe_id: UUID4):
    '''
        ### This function is used to get a recipe by id
        It requires the recipe id to be passed in the path
        ` /recipe/{recipe_id} `
    '''
    recipe = Recipe.get_recipe_by_id(recipe_id)
    return recipe

@app.patch("/recipe/{recipe_id}", tags=["Recipe"])
async def update_recipe(recipe_id: UUID4, recipe: UpdateRecipieModal, Token: Annotated[str, Depends(oauth2_schema)]):
    '''
        ### This function is used to update a recipe by id
        It requires the recipe id to be passed in the path
        ` /recipe/{recipe_id} `
        It requires a token to be passed in the header
        ```json
        Authorization: Bearer <token>
        ```
        The body of the request should be in the following format:
        ```json
        {
            "name": "Recipe Name",
            "ingredients": "Ingredients",
            "instructions": "Instructions",
        }
        or
        {
            "name": "Recipe Name",
        }
        or
        {
            "ingredients": "Ingredients",
        }
        or
        {
            "instructions": "Instructions",
        }
        or
        {
            "name": "Recipe Name",
            "ingredients": "Ingredients",
        }
        or
        {
            "name": "Recipe Name",
            "instructions": "Instructions",
        }
        or
        {
            "ingredients": "Ingredients",
            "instructions": "Instructions",
        }
        ```
        <hr />
        <strong><em>Nobody can update a recipe that they do not own</em></strong>
    '''
    updated_recipe = Recipe.update_recipe(recipe_id=recipe_id, recipe=recipe, Token=Token)
    return updated_recipe

@app.delete("/recipe/{recipe_id}", tags=["Recipe"])
async def delete_recipe(recipe_id: UUID4, Token: Annotated[str, Depends(oauth2_schema)]):
    '''
        ### This function is used to delete a recipe by id
        It requires the recipe id to be passed in the path
        ` /recipe/{recipe_id} `
        It requires a token to be passed in the header
        ```json
        Authorization: Bearer <token>
        ```
        <hr />
        <strong><em>Nobody can delete a recipe that they do not own</em></strong>
    '''
    deleted_recipe = Recipe.delete_recipe(recipe_id=recipe_id, Token=Token)
    return deleted_recipe

@app.get("/recipie/search", tags=["Recipe"])
async def search_recipie(query: str = '',page: int = 1, limit: int = 10):
    '''
        ### This function is used to search for recipes
        It supports pagination using query parameters
        ` ?page=1&limit=10 `
        The query parameter is used to search for recipes by name, ingredients, or instructions
        ` /recipie/search?query=chicken `
        All together it looks like this
        ` /recipie/search?query=chicken&page=1&limit=10 `
    '''
    recipes = Recipe.search_recipies(query, page, limit)
    return recipes
description ="""
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

license_info = {
    "name": "MIT",
    "url": "https://github.com/itsSauraj/recipe-api.git?tab=MIT-1-ov-file",
}

contact_info = {
    "name": "Saurabh Yadav (itsSauraj)",
    "url": "https://github.com/itsSauraj",
    "email": "sauraj.contact@gmail.com"
}

tags_metadata = [
    {
        "name": "* Welcome"
    },
    {
        "name": "User Authentication",
        "description": "Operations with users. The **register**, **login**  logic is here.",
    },
    {
        "name": "Recipe",
        "description": "Operations with recipes. The **create**, **read**, **update** and **delete** logic is here.",
    }
]

class FastAPIConfig:
    app_title = "Recipe API"
    app_version = "1.0.0"
    app_summary = "A simple recipe API that allows users to create, read, update, and delete recipes."
    app_license_info = license_info
    app_contact_info = contact_info
    app_description = description
    app_tags_metadata = tags_metadata
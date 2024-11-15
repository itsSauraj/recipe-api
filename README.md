# Recipe API

### Description
This project is a simple recipe API that allows users to create, read, update, and delete recipes. The database used in this project is SQLite, and the ORM used is SQLAlchemy. The framework used is FastAPI.

### Features
- User registration and authentication using JWT tokens.
- Pagination for the recipes endpoint.
- Searching for recipes by name, ingredients, or instructions.

### Endpoints
- **GET** `/` - Welcome message
- **POST** `/register` - Register a new user
- **POST** `/token` - Get access token
- **POST** `/recipe` - Add a new recipe
- **GET** `/recipes` - Get all recipes
- **GET** `/recipe/{recipe_id}` - Get a recipe by id
- **PATCH** `/recipe/{recipe_id}` - Update a recipe by id
- **DELETE** `/recipe/{recipe_id}` - Delete a recipe by id
- **GET** `/recipe/search` - Search for recipes

### License
This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.

### Contact
For any inquiries, please contact:
- **Name**: Saurabh Yadav (itsSauraj)
- **GitHub**: [itsSauraj](https://github.com/itsSauraj)
- **Email**: sauraj.contact@gmail.com

### Tags
- **Welcome**
- **User Authentication**: Operations with users. The **register**, **login** logic is here.
- **Recipe**: Operations with recipes. The **create**, **read**, **update**, and **delete** logic is here.


### Configuration
The configuration for this project is defined in `config.py` and includes:
- `app_title`: "Recipe API"
- `app_version`: "1.0.0"
- `app_summary`: "A simple recipe API that allows users to create, read, update, and delete recipes."
- `app_license_info`: License information
- `app_contact_info`: Contact information
- `app_description`: Detailed description of the project
- `app_tags_metadata`: Metadata for API tags

### Project Setup
To set up the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/itsSauraj/recipe-api.git
    cd recipe-api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

5. Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

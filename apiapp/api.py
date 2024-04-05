import os
from dotenv import load_dotenv
import django
from django.conf import settings
from fastapi import FastAPI, HTTPException, Query
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from webapp.models import Recipe as DjangoRecipe
import logging

logger = logging.getLogger(__name__)

# Загрузка переменных окружения
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Настройка проекта Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipe_website.settings")
django.setup()

# Создаем экземпляр FastAPI
app = FastAPI()

# Подключение к базе данных проекта
DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@" \
               f"{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Error connecting to the database: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal Server Error: Unable to connect to the database")


class Recipe(BaseModel):
    """
    Pydantic-модель Recipe для FastAPI
    """
    title: str
    category: str
    description: str
    ingredients: str
    cooking_steps: str
    cooking_time: int
    image: str
    image_thumbnail: str
    author: str
    active: bool
    created_date: str


@app.get("/recipes/{recipe_name}", response_model=Recipe)
def read_recipe_by_name(recipe_name: str):
    """
    Маршрут FastAPI для чтения рецепта по названию (регистр названия рецепта не важен, при этом ищет рецепты,
    содержащие заданное название, а не только начинающиеся с него)
    """
    with SessionLocal() as db_session:
        recipe = db_session.query(DjangoRecipe).filter(DjangoRecipe.title.ilike(f"%{recipe_name}%")).first()

        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")

        # Преобразование объекта DjangoRecipe в экземпляр Pydantic-модели Recipe
        return Recipe(**recipe.dict())


@app.get("/recipes/by-ingredient", response_model=List[Recipe])
def get_recipes_by_ingredient(
        ingredient: str = Query(..., title="Ingredient", description="The ingredient to filter recipes")
):
    """
    Маршрут FastAPI для получения всех рецептов, в которых есть переданный ингредиент (регистр названия ингредиента не
    важен, при этом ищет рецепты, содержащие заданное название, а не только начинающиеся с него)
    """
    with SessionLocal() as db_session:
        recipes = db_session.query(DjangoRecipe).filter(DjangoRecipe.ingredients.ilike(f"%{ingredient}%")).all()

        if not recipes:
            raise HTTPException(status_code=404, detail="Recipes not found")

        # Преобразование объектов DjangoRecipe в экземпляры Pydantic-модели Recipe
        recipes_data = [Recipe(**recipe.dict()) for recipe in recipes]
        return recipes_data


@app.get("/recipes/by-category", response_model=List[Recipe])
def get_recipes_by_category(
        category: str = Query(..., title="Category", description="The category to filter recipes").lower()
):
    """
    Маршрут FastAPI для получения всех рецептов указанной категории (регистр не важен)
    """
    with SessionLocal() as db_session:
        recipes = db_session.query(DjangoRecipe).filter(DjangoRecipe.category.ilike(category)).all()

        if not recipes:
            raise HTTPException(status_code=404, detail="Recipes not found")

        # Преобразование объектов DjangoRecipe в экземпляры Pydantic-модели Recipe
        recipes_data = [Recipe(**recipe.dict()) for recipe in recipes]
        return recipes_data

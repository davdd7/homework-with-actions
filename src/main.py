from contextlib import asynccontextmanager
from typing import AsyncGenerator, List

from fastapi import Depends, FastAPI, HTTPException, Path, status
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from homework_with_actions.src.database import async_session, engine
from homework_with_actions.src.models import Base, Recipe
from homework_with_actions.src.schemas import (
    RecipesFirstPage,
    RecipesIn,
    RecipesSecondPage,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Функция запуска и шатдауна приложения
    @param app: приложение FastAPI
    @return: lifespan
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Открывает соединение для работы с БД
    @return: объект сессии
    """
    async with async_session() as session:
        async with session.begin():
            yield session


@app.post("/recipes", response_model=RecipesIn, status_code=status.HTTP_201_CREATED)
async def post_recipes(recipe: RecipesIn, db: AsyncSession = Depends(get_db)) -> Recipe:
    """
    Отправка нового рецепта
    @param recipe: рецепт
    @param db: открытие сессии
    @return: JSON-объект рецепта
    """
    new_recipe = Recipe(**recipe.model_dump())
    db.add(new_recipe)
    return new_recipe


@app.get("/recipes", response_model=List[RecipesFirstPage])
async def recipes_first_page(db: AsyncSession = Depends(get_db)) -> List[Recipe | None]:
    """
    Получение списка рецептов с сортировкой
    @param db: Открытие сессии к БД
    @return: Список объектов рецепта
    """
    recipe = await db.execute(
        select(Recipe).order_by(desc(Recipe.show_count), Recipe.cooking_time)
    )
    return list(recipe.scalars().all())


@app.get("/recipes/{id}", response_model=RecipesSecondPage)
async def recipes_second_page(
    id: int = Path(..., title="ID Рецепта в БД", ge=0),
    db: AsyncSession = Depends(get_db),
) -> Recipe | None:
    """
    Запрос определенного рецепта
    @param id: ID рецепта в БД
    @param db: Открытие доступа к БД
    @return: Объект полученного рецепта
    """
    recipe = await db.get(Recipe, id, with_for_update=True)
    if not recipe:
        raise HTTPException(
            status_code=404, detail="Recipe with id '{}' not found".format(id)
        )

    recipe.show_count += 1

    await db.commit()
    return recipe

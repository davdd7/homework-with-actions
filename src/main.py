from fastapi import FastAPI, Depends, HTTPException, Path, status
from sqlalchemy import desc

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))



import schemas

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from contextlib import asynccontextmanager, AbstractAsyncContextManager
from typing import List, Type

from sqlalchemy.orm import Session

import models

from database import engine, async_session
from models import Recipe


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager:
    """
    Функция запуска и шатдауна приложения
    @param app: приложение FastAPI
    @return: lifespan
    """
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


async def get_db() -> Session:
    """
    Открывает соединение для работы с БД
    @return: объект сессии
    """
    async with async_session() as session:
        async with session.begin():
            yield session

@app.post('/recipes',
          response_model=schemas.RecipesIn,
          status_code=status.HTTP_201_CREATED)
async def post_recipes(recipe: schemas.RecipesIn,
                       db: AsyncSession = Depends(get_db)) -> models.Recipe:
    """
    Отправка нового рецепта
    @param recipe: рецепт
    @param db: открытие сессии
    @return: JSON-объект рецепта
    """
    new_recipe = models.Recipe(**recipe.model_dump())
    db.add(new_recipe)
    return new_recipe


@app.get('/recipes', response_model=List[schemas.RecipesFirstPage])
async def recipes_first_page(db: AsyncSession = Depends(get_db)) -> List[models.Recipe | None]:
    """
    Получение списка рецептов с сортировкой
    @param db: Открытие сессии к БД
    @return: Список объектов рецепта
    """
    recipe = await db.execute(select(models.Recipe).order_by(desc(models.Recipe.show_count),
                                                          models.Recipe.cooking_time))
    return list(recipe.scalars().all())


@app.get('/recipes/{id}', response_model=schemas.RecipesSecondPage)
async def recipes_second_page(id: int = Path(..., title='ID Рецепта в БД', ge=0),
                              db: AsyncSession = Depends(get_db)) -> Type[Recipe | None]:
    """
    Запрос определенного рецепта
    @param id: ID рецепта в БД
    @param db: Открытие доступа к БД
    @return: Объект полученного рецепта
    """
    recipe = await db.get(models.Recipe, id, with_for_update=True)
    if not recipe:
        raise HTTPException(status_code=404, detail='Recipe with id "{}" not found'.format(id))

    recipe.show_count += 1

    await db.commit()
    return recipe


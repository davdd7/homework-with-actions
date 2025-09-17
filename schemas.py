from pydantic import BaseModel


class RecipesFirstPage(BaseModel):
    name: str
    show_count: int
    cooking_time: int

    class Config:
        from_attributes = True


class RecipesSecondPage(BaseModel):
    name: str
    cooking_time: int
    ingredients: str
    description: str

    class Config:
        from_attributes = True


class RecipesIn(BaseModel):
    name: str
    ingredients: str
    description: str
    cooking_time: int
    show_count: int

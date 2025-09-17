import pytest
from ..schemas import RecipesIn


@pytest.mark.asyncio
async def test_debug(client):
    print(f"Client type: {type(client)}")  # Должен быть AsyncClient

@pytest.mark.asyncio
async def test_create_recipe(client):
    response = await client.post(
        "/recipes",
        json={
            'name': 'TestRecipe',
            'ingredients': 'test kapusta, test baklazhan',
            'description': 'testim test',
            'cooking_time': 15
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "TestRecipe"
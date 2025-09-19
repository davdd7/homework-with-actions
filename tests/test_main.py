def test_create_item(client):
    response = client.post(
        "/recipes",
        json={
            "name": "TestRecipe",
            "ingredients": "test kapusta, test baklazhan",
            "description": "testim test",
            "cooking_time": 15,
            "show_count": 0,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "TestRecipe"


def test_bd(client, db_session):
    client.post(
        "/recipes",
        json={
            "name": "TestRecipeDB",
            "ingredients": "test kapusta, test baklazhan",
            "description": "testim test",
            "cooking_time": 15,
            "show_count": 0,
        },
    )

    db_session.commit()

    from homework_with_actions.src.models import Recipe

    recipe = db_session.query(Recipe).first()

    assert recipe.name == "TestRecipeDB"

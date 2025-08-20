import pytest

from httpx import AsyncClient

pytestmark = pytest.mark.anyio

async def test_not_a_route(async_client: AsyncClient):
    response = await async_client.get("/not_a_route")
    assert response.status_code == 404

async def test_get_insects(async_client : AsyncClient):
    response = await async_client.get("/insects")
    assert response.status_code == 200
    assert len(response.json()) == 5
    for insect in response.json():
        assert isinstance(insect["insect_id"], int)
        assert isinstance(insect["generic_name"], str)
        assert isinstance(insect["specific_name"], str)
        assert isinstance(insect["image_url"], str)
        assert isinstance(insect["image_attribution"], str | None)

async def test_get_dev_animals(async_client: AsyncClient):
    response = await async_client.get("/dev_animals")
    assert response.status_code == 200
    assert len(response.json()) == 5
    for animal in response.json():
        assert isinstance(animal["animal_id"], int)
        assert isinstance(animal["generic_name"], str)
        assert isinstance(animal["specific_name"], str)
        assert isinstance(animal["image_url"], str)
        assert isinstance(animal["image_attribution"], str | None)
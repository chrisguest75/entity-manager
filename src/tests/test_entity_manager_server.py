import os
import numbers
from pathlib import Path

import pytest
from aiohttp import web

import entity_manager.server

TEST_PATH = Path(os.path.dirname(os.path.realpath(__file__)))


@pytest.fixture(scope="module")
def entity_manager_server():
    server = entity_manager.server.EntityManagerServer()
    return server


@pytest.fixture()
def cli(loop, aiohttp_client, entity_manager_server):
    web_app = web.Application()
    entity_manager.server.initialize_web_app(web_app, entity_manager_server)
    return loop.run_until_complete(aiohttp_client(web_app))


async def test_server_root_404(cli):
    resp = await cli.get('/')
    assert resp.status == 404


async def test_server_health_200(cli):
    resp = await cli.get('/health')
    assert resp.status == 200

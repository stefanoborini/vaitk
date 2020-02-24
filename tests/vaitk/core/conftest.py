import pytest
from vaitk import core


@pytest.fixture
def coreapp():
    app = None
    try:
        app = core.CoreApplication(["test"])
        yield app
    finally:
        if app:
            app.exit()
        del app

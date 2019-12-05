import sys
from vaitk.core import CoreApplication


def test_basic_initialisation():
    app = CoreApplication(sys.argv)
    assert app.instance == CoreApplication.vApp
    assert app.application_name == sys.argv[0]
    assert app.application_version == ""

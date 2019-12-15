import sys

import vaitk.gui.GlobalColor
from vaitk import gui
from vaitk.gui import widgets

app = gui.Application(sys.argv)

label = widgets.Label("hello")
label.set_colors(vaitk.gui.GlobalColor.GlobalColor.yellow, vaitk.gui.GlobalColor.GlobalColor.blue)
label.show()
app.exec_()

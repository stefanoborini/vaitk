import sys

from vaitk import gui
from vaitk.gui import widgets, GlobalColor

app = gui.Application(sys.argv)

label = widgets.Label("hello")
label.set_colors(GlobalColor.yellow, GlobalColor.blue)
label.show()
app.exec_()

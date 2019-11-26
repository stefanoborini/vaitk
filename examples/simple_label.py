import sys
from vaitk import gui
from vaitk.gui import widgets

app = gui.Application(sys.argv)

label = widgets.Label("hello")
label.set_colors(gui.GlobalColor.yellow, gui.GlobalColor.blue)
label.show()
app.exec_()

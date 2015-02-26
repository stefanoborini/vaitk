import sys
from vaitk import gui
from vaitk.gui import widgets

app = gui.VApplication(sys.argv)

label = widgets.VLabel("hello")
label.setColors(gui.VGlobalColor.yellow, gui.VGlobalColor.blue)
label.show()
app.exec_()

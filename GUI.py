import gtk.glade

from MainWindow import *

def open_main_window():
    #epmmw = MainWindow()
    #wTree = gtk.glade.XML("epm.glade")
    #mainWindow = wTree.get_widget("mainWindow")
    #mainWindow.connect("destroy", gtk.main_quit)
    mainWindow = MainWindow()
    gtk.main()

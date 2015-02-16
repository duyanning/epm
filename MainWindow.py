import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import os.path

from Project import *

import sys

def epmDir():
    return os.path.dirname(sys.argv[0])

class MainWindow:
    def __init__(self):
        self.wTree = gtk.glade.XML(os.path.join(epmDir(), "epm.glade"), "mainWindow")
#        self.mainWindow = self.wTree.get_widget("mainWindow")

        dic = {"on_mainWindow_destroy" : self.onQuit,
               "on_btnOpen_clicked" : self.onOpenPrj
               }

        self.wTree.signal_autoconnect(dic)

        self.treestore = gtk.TreeStore(str)
        self.tvFiles = self.wTree.get_widget("treeFiles")
        self.tvFiles.set_model(self.treestore)

        self.tvFiles.connect("button_press_event", self.button_press_callback)

        tvcolumn = gtk.TreeViewColumn('Project')
        self.tvFiles.append_column(tvcolumn)
        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 0)

        hpaned1 = self.wTree.get_widget("hpaned1")
        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        self.notebook.show()

        hpaned1.add2(self.notebook)
        frame = gtk.Frame("aaa")
        frame.set_border_width(10)
        frame.set_size_request(100, 75)
        frame.show()
        label = gtk.Label("bbb")
        label.show()
        frame.add(label)
        label = gtk.Label("ccc")

        self.notebook.append_page(frame, label)

    def button_press_callback(widget, event, data):
        print "abc"
#   Glib::RefPtr<Gtk::TreeView::Selection> refSelection = get_selection();
#   if(refSelection)
#   {
#     Gtk::TreeModel::iterator iter = refSelection->get_selected();
#     if(iter)
#     {
#       int id = (*iter)[m_Columns.m_col_id];
#       std::cout << "  Selected ID=" << id << std::endl;
#     }
#   }
        pass
    
    def onOpenPrj(self, w):
        print "onOpenPrj"
        dlg = gtk.FileChooserDialog("Open..",
                                    None,
                                    gtk.FILE_CHOOSER_ACTION_OPEN,
                                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                     gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dlg.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("*.epmprj")
        filter.add_pattern("*.epmprj")
        dlg.add_filter(filter)
        response = dlg.run()

        if response == gtk.RESPONSE_OK:
            self.openProject(dlg.get_filename())

        dlg.destroy()
 
    def openProject(self, filename):

        self.treestore.clear()

        prj = Project(filename)
        prj.load()

        piter = self.treestore.append(None, [os.path.basename(prj.path())])
        for src in prj.sourceFilesList():
            self.treestore.append(piter, [src])

    def onQuit(self, w):
        print "onQuit"
        gtk.main_quit()

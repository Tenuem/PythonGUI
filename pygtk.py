import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import sys
import card_dealer as cd

WINDOW_WIDTH = 680
WINDOW_HEIGHT = 680
CARD_WIDTH = WINDOW_WIDTH // 10
CARD_HEIGHT = CARD_WIDTH * 5 // 4

def rotate_image(image, angle):
    #pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
    rotated_pixbuf = image.rotate_simple(angle)
    return rotated_pixbuf

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Brydżowy rozdajnik kart")
        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)

        
        self.init_ui()

    def init_ui(self):
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # new game button
        new_game_button = Gtk.Button.new_with_label("Nowa gra")
        new_game_button.connect("clicked", self.new_game)
        self.grid.attach(new_game_button, 8, 9, 2, 1)

        # menu button
        menu_button = Gtk.Button.new_with_label("Menu")
        menu_button.connect("clicked", self.menu)
        #grid.attach(menu_button, 0, 0, 1, 1)

        self.list_store = Gtk.ListStore(str)
        items = ["o grze", "o nas", "wyjdź"]
        for item in items:
            self.list_store.append([item])

        bout_us = Gtk.Button.new_with_label("O nas")
        bout_us.connect("clicked", lambda menu: self.menu_action("o nas"))

        bout_game = Gtk.Button.new_with_label("O grze")
        bout_game.connect("clicked", lambda menu: self.menu_action("o grze"))

        self.grid.attach(bout_us, 2, 0, 2, 1)
        self.grid.attach(bout_game, 0, 0, 2, 1)

        #tree_view = Gtk.TreeView.new_with_model(self.list_store)
        #renderer = Gtk.CellRendererText()
        #column = Gtk.TreeViewColumn("Menu", renderer, text=0)
        #tree_view.append_column(column)
        #tree_view.connect("row-activated", self.menu_item_clicked)
        #grid.attach(tree_view, 0, 0, 3, 1)

        self.selected_item_label = Gtk.Label()
        #grid.attach(self.selected_item_label, 0, 2, 2, 1)

        # card handling
        self.deck = cd.generate_deck()
        self.hands = cd.deal_cards(self.deck)
        self.dispose_cards(self.grid)

    def new_game(self, button):
        #for child in self.grid.get_children():
        #    self.grid.remove(child)
        #self.remove(self.grid)
        self.hands = cd.deal_cards(self.deck)
        self.dispose_cards(self.grid)
        #self.init_ui()

    def menu_action(self, item):
        #model = tree_view.get_model()
        #item = model[path][0]

        if item == "o grze":
            dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO,
                                       buttons=Gtk.ButtonsType.OK, text="O grze")
            dialog.format_secondary_text("Program rozdaje karty w brydżu sportowym")
            dialog.run()
            dialog.destroy()
        elif item == "o nas":
            dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO,
                                       buttons=Gtk.ButtonsType.OK, text="O nas")
            dialog.format_secondary_text("Nie ma nas bez was")
            dialog.run()
            dialog.destroy()
        else:
            Gtk.main_quit()

    def menu(self, button):
        self.list_store.clear()
        items = ["o grze", "o nas", "wyjdź"]
        for item in items:
            self.list_store.append([item])

    def dispose_cards(self, grid):
        import math

        for i, hand in enumerate(self.hands):
            for j, card in enumerate(hand):
                orientation = i % 2  # N&S horizontal, E&W vertical
                factor = 3 if i<2 else 1
                image = Gtk.Image()
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(card.filename())
                scaled_pixbuf = pixbuf.scale_simple(CARD_WIDTH, CARD_HEIGHT, GdkPixbuf.InterpType.BILINEAR)
                image.set_from_pixbuf(rotate_image(scaled_pixbuf, factor*90*orientation))

                event_box = Gtk.EventBox()
                event_box.add(image)

                if orientation == 0:  # N or S
                    if i == 0:  # N
                        self.grid.attach(event_box, 2+j, 1, 2, 1)
                    else:
                        self.grid.attach(event_box, 2+j, 16, 2, 1)
                else:  # E or W
                    if i == 1:  # E
                        self.grid.attach(event_box, 16, 2+j, 1, 2)
                    else:  # W
                        self.grid.attach(event_box, 0, 2+j, 1, 2)

                event_box.show_all()

if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


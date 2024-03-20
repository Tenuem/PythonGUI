import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QListWidget, QMessageBox

import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt, QTimer

import card_dealer as cd


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

CARD_WIDTH = WINDOW_WIDTH//10
CARD_HEIGHT = CARD_WIDTH*5//4  

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Brydżowy rozdajnik kart"
        self.setWindowTitle(self.title)
        
        self.initUI()
        
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
    def initUI(self):
        # new game button
        self.button = QPushButton('Nowa gra', self)

        # Set button position to be centered in the window
        button_width = 100
        button_height = 30
        self.button.setGeometry((WINDOW_WIDTH - button_width) // 2, (WINDOW_HEIGHT - button_height) // 2, button_width, button_height)

        # Connect the button's clicked signal to a function
        self.button.clicked.connect(self.newgame)

        # menu button
        self.button = QPushButton('Menu', self)

        # Set button position to be centered in the window
        button_width = 50
        button_height = 20
        self.button.setGeometry(5, 5, button_width, button_height)

        # Connect the button's clicked signal to a function
        self.button.clicked.connect(self.menu)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(WINDOW_WIDTH//2-100, WINDOW_HEIGHT//2-50, 200, 100)

        # Add items to the list
        items = ["o grze", "o nas", "wyjdź"]
        self.list_widget.addItems(items)
        self.list_widget.setVisible(False)

        # Connect item selection event to a function
        self.list_widget.itemClicked.connect(self.menu_item_clicked)

        self.selected_item_label = QLabel("", self)
        self.selected_item_label.setGeometry(WINDOW_WIDTH//2-100, WINDOW_HEIGHT//2-50, 200, 100)
        self.selected_item_label.setVisible(False)

        self.labels = []
        # card handling
        self.deck = cd.generate_deck()
        self.hands = cd.deal_cards(self.deck)

        self.dispose_cards()
    
    def newgame(self):
        for label in self.findChildren(QLabel):
            label.deleteLater()

        QApplication.processEvents()

        self.new_shuffle()

    def menu_item_clicked(self, item):
        # Handle item selection event
        if item.text() == "o grze":
            QMessageBox.information(self, "O grze", "Program rozdaje karty w brydżu sportowym")
        elif item.text() == "o nas":
            QMessageBox.information(self, "O nas", "Nie ma nas bez was")
        else:
            self.list_widget.setVisible(False)

    def menu(self):
        self.list_widget.setVisible(not self.list_widget.isVisible())

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0, 120, 0))

    def new_shuffle(self):
        self.hands = cd.deal_cards(self.deck)
        self.dispose_cards()

    def dispose_cards(self):
        import math
        self.labels = []
        for i, hand in enumerate(self.hands):
            for j, card in enumerate(hand):
                orientation = i%2 # N&S horizontal, E&W vertical
                label = QLabel(self)
                pixmap = QtGui.QPixmap(card.filename())
                pixmap = pixmap.scaled(CARD_WIDTH, CARD_HEIGHT)
                margin = math.floor(CARD_WIDTH*1.5)

                if orientation == 0: # N or S
                    if i == 0: # N
                        label.setGeometry(margin+j*(CARD_WIDTH//2), 0, CARD_WIDTH, CARD_HEIGHT)
                    else:
                        label.setGeometry(margin+j*(CARD_WIDTH//2), WINDOW_HEIGHT-CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT)
                    label.setPixmap(pixmap) 
                else: # E or W
                    if i == 1: # E
                        label.setGeometry(WINDOW_WIDTH-CARD_HEIGHT, WINDOW_HEIGHT-margin-CARD_WIDTH-CARD_WIDTH//2*j, CARD_HEIGHT, CARD_WIDTH)
                    else: # W
                        label.setGeometry(0, margin+CARD_WIDTH//2*j, CARD_HEIGHT, CARD_WIDTH)
                    pixmap = pixmap.transformed(QtGui.QTransform().rotate(-90)) if i == 1 else pixmap.transformed(QtGui.QTransform().rotate(90))
                    label.setPixmap(pixmap)

                label.setStyleSheet("border: 2px solid black;")
                self.labels.append(label)
                label.show()

if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #bridge_app = BridgeApp()
    #print('klepka')
    #sys.exit(app.exec_())

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

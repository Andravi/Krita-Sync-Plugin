from PyQt5.QtWidgets import *
from krita import *
from PyQt5.QtGui import QFont



class KritaSyncDriverDock(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Krita Sync Driver")
        mainWidget = QWidget(self)
        self.setWidget(mainWidget)
        
        buttonSyncWithDriver = QPushButton("sincronizar com Driver", mainWidget)
        buttonSaveInDriver = QPushButton("Salvar no Driver", mainWidget)
        e1 = QLineEdit()
        e1.setFont(QFont("Arial",12))

        buttonSyncWithDriver.clicked.connect(self.copyFromDriver)
        buttonSaveInDriver.clicked.connect(self.copyToDriver)
        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(e1)
        mainWidget.layout().addWidget(buttonSyncWithDriver)
        mainWidget.layout().addWidget(buttonSaveInDriver)
        

    def canvasChanged(self, canvas):
        pass    
        
    
    def copyFromDriver(self):
        print(1)
        ...
    
    
    def copyToDriver(self):
        print(2)
        ...

Krita.instance().addDockWidgetFactory(DockWidgetFactory("KritaSyncDriverDock", DockWidgetFactoryBase.DockRight, KritaSyncDriverDock))

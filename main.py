from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from pysnmp.hlapi import *

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle('My Window')

        # Create an input field
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.move(50, 50)
        self.input_field.resize(200, 30)

        # Create a button
        self.button = QtWidgets.QPushButton(self)
        self.button.setText('Get Printed Data')
        self.button.move(50, 100)
        self.button.resize(200, 30)
        self.button.clicked.connect(self.get_printed_data)

    def get_printed_data(self):
        ip_address = self.input_field.text()
        community_string = 'public'

        # Use PySNMP to retrieve the printed data
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                CommunityData(community_string),
                UdpTransportTarget((ip_address, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('1.3.6.1.2.1.43.10.2.1.4.1.1')),
                ObjectType(ObjectIdentity('1.3.6.1.2.1.43.10.2.1.4.1.2')),
                ObjectType(ObjectIdentity('1.3.6.1.2.1.43.10.2.1.4.1.5')),
                lexicographicMode=False)
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            total_pages = 0
            black_and_white_pages = 0
            color_pages = 0
            for varBind in varBinds:
                oid, value = varBind
                if str(oid) == '1.3.6.1.2.1.43.10.2.1.4.1.1':
                    total_pages = int(value) if value else 0
                elif str(oid) == '1.3.6.1.2.1.43.10.2.1.4.1.2':
                    black_and_white_pages = int(value) if value else 0
                elif str(oid) == '1.3.6.1.2.1.43.10.2.1.4.1.3':
                    color_pages = int(value) if value else 0
        # Update the label with the printed data
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Total pages: {}\nBlack and white pages: {}\nColor pages: {}'.format(total_pages, black_and_white_pages, color_pages))
        self.label.move(50, 150)
        self.label.resize(200, 100)
        self.label.show()


app = QApplication([])
win = MyWindow()
win.show()
app.exec_()

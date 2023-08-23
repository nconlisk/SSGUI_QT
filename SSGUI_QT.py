""" 
PyQT implementation of a Secret Santa emailer app.

Requires api access to an email client.

Requires names and email addresses of participants as a comma separated list or for manual entry.


"""

import sys

import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QFileDialog

__version__ = "0.1"
__author__ = "Noel Conlisk"

class SSGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # Set main window props
        self.setWindowTitle("Secret Santa Draw")
        self.setFixedSize(300, 300)

        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Create the display and the buttons
        formLayout = QFormLayout()
        self.name_Ent = QLineEdit()
        self.email_Ent = QLineEdit()
        formLayout.addRow('Name:', self.name_Ent)
        formLayout.addRow('Email:', self.email_Ent)
        self.generalLayout.addLayout(formLayout)
        self._createButtons()
        self.buttonLogic()
        self.a = {} # sets up dict to contain names and emails
        # Display box to show added participants
        self.dictDisplay = QLineEdit()
        self.dictDisplay.setFixedHeight(35)
        self.dictDisplay.setReadOnly(True)
        self.generalLayout.addWidget(self.dictDisplay)
        

   
    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {
                   'Add Name': (0, 0),
                   'Clear Names': (0, 1),
                   'Load Names': (1, 0),
                   'Draw Pairs': (1, 1),
                  }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(100, 50)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)
       
        
    def buttonLogic(self):

        self.buttons["Load Names"].clicked.connect(self.loadInfo)
        self.buttons["Clear Names"].clicked.connect(self.reset_Santa)
        self.buttons["Add Name"].clicked.connect(self.getInfo)
        self.buttons["Draw Pairs"].clicked.connect(self.secret_Santa)
      
    
    

    def loadInfo(self):

        self.a = {}    # Reset list to empty before importing names.

        try:
            filename = QFileDialog.getOpenFileName()
            nameList = open(filename[0], "r" ) 
            if nameList:
                for lines in nameList.readlines():
                    if len(lines) > 1:
                        name, email = lines.split(",")
                        self.a[name] = email.strip()
        
            included_names = [] 
            for i in self.a.keys():
                included_names.append(i)
                #Include a slot to display names in the draw and to display draw success.
                self.dictDisplay.setText(str(included_names))  
        except:
            return
        
        
            
    
    def getInfo(self): 

        name = self.name_Ent.text()
        email = self.email_Ent.text()

        self.a[name] = email
        self.name_Ent.clear()
        self.email_Ent.clear()
        self.dictDisplay.setText(str(list(self.a)))

        return self.a


    def secret_Santa(self):

        cur_year = datetime.datetime.now().year

        # create list of names from dict keys
        # later use name to return email address for match notification

        names = list(self.a.keys())

        
        random.shuffle(names)

        
        match = []  
        for (i, x) in enumerate(names):
            match +=  [x, names[i-1]]

            # EMAIL SECTION
            my_address = "your.address@gmail.com"    # ENTER YOUR EMAIL ADDRESS HERE    
            to_address = self.a[x]
            msg = MIMEMultipart()
            msg['From'] = my_address
            msg['To'] = to_address
            msg['Subject'] = "Secret Santa Draw"
            body = (
            f"Dear {x},\n"
            f"Congratulations, your match for {cur_year}'s Secret Santa is {names[i-1]}\n"
            f"Please have your gift ready for exchange on the 25th December and\n"
            f"remember to stick within the budget.\n"
            f"\n"
            f"Merry Christmas,\n"
            f"Secret Santa Team\n")
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)    # CHANGE SMTP AND PORT IF GMAIL NOT USED
            server.starttls()
            server.login(my_address, "yourPassword")    # ENTER YOUR EMAIL ACCOUNT PASSWORD HERE
            text = msg.as_string()
            server.sendmail(my_address, to_address, text)
            server.quit()
        
        # write match results out to a file as confirmation.
        file = open(f"Results_{cur_year}.txt", "w")
        file.write(str(match))
        file.close()
        self.dictDisplay.setText(f"Hohoho Secret Santa's for {cur_year} have been notified")



    def reset_Santa(self):

        # When clear names button pushed this function assigns an empty dictionary to a and clears the message display.

        self.dictDisplay.setText("")
        self.a = {}
        
        


def main():
    """Main function."""
    # Create an instance of QApplication
    SSAPP = QApplication(sys.argv)
    # Show the app's GUI
    view = SSGUI()
    view.show()
    # Execute the app's main loop
    sys.exit(SSAPP.exec_())

if __name__ == '__main__':
    main()

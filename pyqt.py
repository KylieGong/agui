import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import argparse
import re

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parameters):
        super(MainWindow, self).__init__()

        self.groups = groups
        self.radio_groups = []
        self.sliderlabels = []

        self.initUI()
    
    def initUI(self):
        self.pagelayout = QtWidgets.QVBoxLayout()       #page layout
        self.dbtnlayout = QtWidgets.QHBoxLayout()       #layout for the default buttons
        self.elmtlayout = QtWidgets.QVBoxLayout()   #layout for the added widgets, stacks elements
        
        #add layouts to the page
        self.pagelayout.addLayout(self.dbtnlayout) 
        self.pagelayout.addLayout(self.elmtlayout)

        #run, save, load, quit, help button
        btn = QtWidgets.QPushButton(self)
        btn.setText("run")
        btn.clicked.connect(self.run)
        self.dbtnlayout.addWidget(btn)

        btn = QtWidgets.QPushButton(self)
        btn.setText("save")
        btn.clicked.connect(self.save)
        self.dbtnlayout.addWidget(btn)

        btn = QtWidgets.QPushButton(self)
        btn.setText("load")
        btn.clicked.connect(self.load)
        self.dbtnlayout.addWidget(btn)

        btn = QtWidgets.QPushButton(self)
        btn.setText("quit")
        btn.clicked.connect(self.quit)
        self.dbtnlayout.addWidget(btn)

        btn = QtWidgets.QPushButton(self)
        btn.setText("help")
        btn.clicked.connect(self.help)
        self.dbtnlayout.addWidget(btn)
        
        #set the main page layout
        widget = QtWidgets.QWidget()
        widget.setLayout(self.pagelayout) 
        scroll = QtWidgets.QScrollArea()    #add scrollbar
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        self.setGeometry(500, 100, 700, 500)
        self.setCentralWidget(scroll)

        self.createWidgetsFromGroups()
    
    def run(self):
        print('run')
    
    def save(self):
        print('save')
    
    def load(self):
        print('load')
    
    def quit(self):
        self.close()
        print('quit')

    def help(self):
        print('help')

    def createWidgetsFromGroups(self):
        for group in self.groups:
            group_type, group_name, options, default_option, help = group

            if group_type == "RADIO":
                print("radio button created")
                new_group = QtWidgets.QButtonGroup()
                self.radio_groups.append(new_group)
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                group_layout.addWidget(label)
                for option in options:
                    option = option.strip()
                    radio_button = QtWidgets.QRadioButton(option)
                    new_group.addButton(radio_button)
                    group_layout.addWidget(radio_button)
                    if option in default_option:
                        radio_button.setChecked(True)
                self.elmtlayout.addLayout(group_layout)

            elif group_type == "IFILE" or group_type == "OFILE" or group_type == "IDIR":
                print("browse files button created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                group_layout.addWidget(label)
                btn = QtWidgets.QPushButton(self)
                btn.setText("browse...")
                def browse():
                    file = QtWidgets.QFileDialog.getOpenFileNames(self, "Select File", "")
                    print(file)
                btn.clicked.connect(browse)
                txt = QtWidgets.QLineEdit(self)
                group_layout.addWidget(btn)
                group_layout.addWidget(txt)
                self.elmtlayout.addLayout(group_layout)

            elif group_type == "CHECK":
                print("checkbox created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                group_layout.addWidget(label)
                for option in options:
                    option = option.strip()
                    checkbox = QtWidgets.QCheckBox(option, self)
                    group_layout.addWidget(checkbox)
                    if option in default_option:
                        checkbox.setChecked(True)
                self.elmtlayout.addLayout(group_layout)

            elif group_type == "ENTRY":
                print("textbox created")
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                group_layout.addWidget(label)
                txt = QtWidgets.QLineEdit(self)
                txt.setText(default_option)
                group_layout.addWidget(txt)
                self.elmtlayout.addLayout(group_layout)
            
            elif group_type == "SCALE":
                group_layout = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(group_name+":")
                group_layout.addWidget(label)
                options = ''.join(options)
                options = options.split(':')

                print("slider created")
                #creates a horizontal slider
                slider = QtWidgets.QSlider(self)
                slider.setOrientation(QtCore.Qt.Horizontal)
                slider.setSingleStep(int(float(options[2])*100))
                slider.setPageStep(int(float(options[2])*100))       #moves the slider when clicking or up/down
                slider.setRange(int(options[0])*100, int(options[1])*100)
                slider.setValue(int(float(default_option[0])*100))

                label_slider = QtWidgets.QLabel(str(default_option[0]))
                slider.valueChanged.connect(lambda value, lbl=label_slider: self.updateLabel(lbl, value))
                
                group_layout.addWidget(label_slider)
                group_layout.addWidget(slider)
                self.elmtlayout.addLayout(group_layout)

    def updateLabel(self, label, value):
        label.setText(str(value/100))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dynamic GUI Builder")
    parser.add_argument("param_file", help="Path to the text file containing parameters")
    args = parser.parse_args()

    with open(args.param_file, "r") as file:
        # content = file.read()
        lines = file.readlines()

    groups = []
    # matches = re.findall(r'#>\s+(\w+)\s+(\w+)=(.+?)(?:\n|#>|$)', content, re.DOTALL)
    # for match in matches:
        # group_type = match[0]
        # group_name = match[1]
        # options = match[2].split(' ', 1)
        # default_option = []
        # if len(options) > 1: 
        #     default_option = options[0].split(',')
        #     options = options[1].split(',')
    pattern = r"\s*(\w+)\s*=\s*([^\s#]+)\s*#\s*([^\#]+)\s*#\s*>\s*(\w+)(?:\s+(\S+))?"
    for line in lines:
        match = re.match(pattern, line)
        if match:
            group_type = match.group(4)
            group_name = match.group(1)
            default_option = match.group(2)
            options = match.group(5).split(',') if match.group(5) else ""
            help = match.group(3)

            groups.append((group_type, group_name, options, default_option, help))

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(groups)
    w.show()

    print(sys.argv)

    try:
        print('opening window')
        sys.exit(app.exec())
    except SystemExit:
        print('closing window')
import json
import sys
from io import StringIO
from datetime import datetime

from PySide2.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtCore
from SpchtDescriptorFormat import Spcht

# Windows Stuff for Building under Windows
try:
    # Include in try/except block if you're also targeting Mac/Linux
    from PySide2.QtWinExtras import QtWin
    myappid = 'UBL.SPCHT.checkerGui.0.2'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class spcht_checker(QDialog):

    def __init__(self):
        super(spcht_checker, self).__init__()
        self.taube = Spcht()
        self.setBaseSize(1280, 720)
        self.setMinimumSize(720, 480)
        self.setWindowTitle("SPCHT Format Checker & analyzer")
        self.setWindowFlag(QtCore.Qt.Window)

        main_layout = QGridLayout(self)

        # left side
        line1 = QHBoxLayout()
        self.str_sdf_file = QLineEdit()
        self.str_sdf_file.setPlaceholderText("Click the load button to open a spcht.json file")
        self.str_sdf_file.setReadOnly(True)
        self.btn_sdf_file = QPushButton("spcht.json")
        self.btn_sdf_retry = QPushButton("retry")
        self.btn_sdf_retry.setDisabled(True)
        line1.addWidget(self.str_sdf_file)
        line1.addWidget(self.btn_sdf_file)
        line1.addWidget(self.btn_sdf_retry)

        line3 = QHBoxLayout()
        self.str_json_file = QLineEdit()
        self.str_json_file.setPlaceholderText("Click the open button after loading a spcht.json file to try out testdata")
        self.str_json_file.setReadOnly(True)
        self.btn_json_file = QPushButton("Testdata")
        self.btn_json_file.setToolTip("A spcht testdata file is formated in json with a list as root and each element containing the dictionary of one entry.")
        self.btn_json_file.setDisabled(True)
        self.btn_json_retry = QPushButton("retry")
        self.btn_json_retry.setToolTip("This DOES NOT retry to load the Testdata but \ninstead reloads the Spcht File and THEN reloads\n the testdata as part of its routine")
        self.btn_json_retry.setDisabled(True)
        line3.addWidget(self.str_json_file)
        line3.addWidget(self.btn_json_file)
        line3.addWidget(self.btn_json_retry)

        # middle part - View 1
        middleLayout = QHBoxLayout()
        self.line2 = QTreeView()
        self.treeViewModel = QStandardItemModel()
        self.treeViewModel.setHorizontalHeaderLabels(
            ['Name/#', 'source', 'graph', 'fields', 'subfields', 'info', 'comments'])
        self.line2.setModel(self.treeViewModel)
        self.line2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.line2.setUniformRowHeights(True)

        label_fields = QLabel("Fields")
        self.lst_fields = QListView()
        self.lst_fields.setMaximumWidth(200)
        self.lst_fields_model = QStandardItemModel()
        self.lst_fields.setModel(self.lst_fields_model)
        fields = QVBoxLayout()
        fields.addWidget(label_fields)
        fields.addWidget(self.lst_fields)

        label_graphs = QLabel("Graphs")
        self.lst_graphs = QListView()
        self.lst_graphs.setMaximumWidth(300)
        self.lst_graphs_model = QStandardItemModel()
        self.lst_graphs.setModel(self.lst_graphs_model)
        graphs = QVBoxLayout()
        graphs.addWidget(label_graphs)
        graphs.addWidget(self.lst_graphs)

        middleLayout.addWidget(self.line2)
        middleLayout.addLayout(fields)
        middleLayout.addLayout(graphs)

        # middle part - View 2
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Monospace", 10))

        # middle part - View 3
        self.txt_tabview = QTextEdit()
        self.txt_tabview.setReadOnly(True)
        self.txt_tabview.setFont(QFont("Monospace", 10))
        self.tbl_tabview = QTableView()
        self.tbl_tabview.horizontalHeader().setStretchLastSection(True)
        self.mdl_tbl_sparql = QStandardItemModel()
        self.mdl_tbl_sparql.setHorizontalHeaderLabels(["resource identifier", "property name", "property value"])
        self.tbl_tabview.setModel(self.mdl_tbl_sparql)
        self.tbl_tabview.setColumnWidth(0, 300)
        self.tbl_tabview.setColumnWidth(1, 300)

        tabView = QTabWidget()
        tabView.setTabPosition(QTabWidget.West)
        tabView.setTabShape(QTabWidget.Triangular)
        tabView.addTab(self.txt_tabview, "Text")
        tabView.addTab(self.tbl_tabview, "Table")


        # bottom
        self.btn_tristate = QPushButton()
        self.btn_tristate.setMaximumWidth(60)
        self.btn_tristate.setFlat(True)
        self.tristate = 0
        self.notifybar = QStatusBar()
        self.notifybar.showMessage("Dies ist ein Test"*20)
        self.notifybar.setSizeGripEnabled(False)
        bottombar = QHBoxLayout()
        bottombar.addWidget(self.btn_tristate)
        bottombar.addWidget(self.notifybar)

        # general layouting
        self.centralLayout = QStackedWidget()
        randomStackasWidget = QWidget()
        randomStackasWidget.setLayout(middleLayout)
        self.centralLayout.addWidget(self.console)
        self.centralLayout.addWidget(randomStackasWidget)
        self.centralLayout.addWidget(tabView)

        main_layout.addLayout(line1, 0, 0)
        main_layout.addWidget(self.centralLayout, 1, 0)
        main_layout.addLayout(line3, 2, 0)
        main_layout.addLayout(bottombar, 3, 0)

        # Event Binds
        self.btn_sdf_file.clicked.connect(self.btn_spcht_load_dialogue)
        self.btn_sdf_retry.clicked.connect(self.btn_spcht_load_retry)
        self.btn_tristate.clicked.connect(self.toogleTriState)
        self.btn_json_file.clicked.connect(self.btn_clk_loadtestdata)
        self.toogleTriState(0)

    def btn_spcht_load_dialogue(self):
        path_To_File, type = QtWidgets.QFileDialog.getOpenFileName(self, "Open spcht descriptor file", "./", "Spcht Json File (*.spcht.json);;Json File (*.json);;Every file (*.*)")

        if path_To_File == "":
            return None

        self.btn_sdf_retry.setDisabled(False)
        self.str_sdf_file.setText(path_To_File)
        self.load_spcht(path_To_File)

    def btn_spcht_load_retry(self):
        self.load_spcht(self.str_sdf_file.displayText())

    def load_spcht(self, path_To_File):
        try:
            with open(path_To_File, "r") as file:
                testdict = json.load(file)
                output = StringIO()
                status = Spcht.check_format(testdict, out=output)
        except json.decoder.JSONDecodeError as e:
            self.console.insertPlainText(spcht_checker.time_log(f"JSON Error: {str(e)}"))
            self.toogleTriState(0)
            return None
        except FileNotFoundError as e:
            self.console.insertPlainText(spcht_checker.time_log(f"File not Found: {str(e)}"))
            self.toogleTriState(0)
            return None

        self.taube.load_descriptor_file(path_To_File)
        if status:
            self.centralLayout.setCurrentIndex(1)
            self.btn_json_file.setDisabled(False)
            self.populate_treeview_with_spcht()
            self.populate_text_views()
        else:
            self.console.insertPlainText(spcht_checker.time_log(f"SPCHT Error: {output.getvalue()}"))
            self.toogleTriState(0)

    def populate_treeview_with_spcht(self):
        i = 0
        # populate views
        if self.treeViewModel.hasChildren():
            self.treeViewModel.removeRows(0, self.treeViewModel.rowCount())
        for each in self.taube:
            i += 1
            tree_row = QStandardItem(each.get('name', f"Element #{i}"))
            col0 = QStandardItem("") # dummy
            col1 = QStandardItem(each.get('source'))
            col2 = QStandardItem(each.get('graph', ""))
            col3 = QStandardItem(each.get('field', ""))
            col4 = QStandardItem(each.get('subfield', ""))
            col5 = QStandardItem("No Info yet")
            col6 = QStandardItem(each.get('comment'))
            spcht_checker.disableEdits(col0, col1, col2, col3, col4, col5, col6)
            tree_row.appendRow([col0, col1, col2, col3, col4, col5, col6])
            tree_row.setEditable(False)
            self.treeViewModel.appendRow(tree_row)
            self.line2.setFirstColumnSpanned(i-1, self.line2.rootIndex(), True)

    def populate_text_views(self):
        # retrieve used fields & graphs
        fields = self.taube.get_node_fields()
        graphs = self.taube.get_node_graphs()
        self.lst_fields_model.clear()
        self.lst_graphs_model.clear()
        for each in fields:
            tempItem = QStandardItem(each)
            tempItem.setEditable(False)
            self.lst_fields_model.appendRow(tempItem)
        for each in graphs:
            tempItem = QStandardItem(each)
            tempItem.setEditable(False)
            self.lst_graphs_model.appendRow(tempItem)

    def toogleTriState(self, status=0):
        toggleTexts = ["Console", "View", "Tests"]
        if isinstance(status, bool):  # connect calls as false
            if self.tristate >= 2:
                self.tristate = 0
            else:
                self.tristate += 1
            self.centralLayout.setCurrentIndex(self.tristate)
        else:
            self.centralLayout.setCurrentIndex(status)
            self.tristate = self.centralLayout.currentIndex()
        self.btn_tristate.setText(toggleTexts[self.tristate])

    def btn_clk_loadtestdata(self, file):
        debug_dict = {}  # TODO: loading of definitions
        try:
            with open("thetestset.descri.json") as file:
                temp_dict = json.load(file)
                if isinstance(temp_dict, dict):
                    code_green = 1
                    for key, value in temp_dict.items():
                        if not isinstance(key, str) or not isinstance(value, str):
                            code_green = 0
                            break
                    if code_green == 1:
                        debug_dict = temp_dict
        except FileNotFoundError:
            print("No accompanied descriptor found")
            pass # nothing happens
        except json.JSONDecodeError:
            print("Json Debug error")
            pass # also okay
        # loading debug data from debug dict if possible
        with open("thetestset.json", "r") as file:
            thetestset = json.load(file)
            tbl_list = []
            text_list = []
            for entry in thetestset:
                temp = self.taube.processData(entry, "https://data.finc.info/resources/")  # TODO: input for graph
                if isinstance(temp, list):
                    text_list.append(
                    "\n\n=== {} - {} ===\n".format(entry.get('id', "Unknown ID"), debug_dict.get(entry.get('id'), "Ohne Name")))
                    for each in temp:
                        if each[3] == 0:
                            tbl_list.append((each[0], each[1], each[2]))
                            tmp_sparql = f"<{each[0]}> <{each[1]}> \"{each[2]}\" . \n"
                        else:  # "<{}> <{}> <{}> .\n".format(graph + ressource, node['graph'], facet))
                            tmp_sparql = f"<{each[0]}> <{each[1]}> <{each[2]}> . \n"
                            tbl_list.append((each[0], each[1], f"<{each[2]}>"))
                        text_list.append(tmp_sparql)
        # txt view
        self.txt_tabview.clear()
        for each in text_list:
            self.txt_tabview.insertPlainText(each)
        # table view
        if self.mdl_tbl_sparql.hasChildren():
            self.mdl_tbl_sparql.removeRows(0, self.mdl_tbl_sparql.rowCount())
        for each in tbl_list:
            col0 = QStandardItem(each[0])
            col1 = QStandardItem(each[1])
            col2 = QStandardItem(each[2])
            self.mdl_tbl_sparql.appendRow([col0, col1, col2])
        self.toogleTriState(2)


    @staticmethod
    def disableEdits(*args1 : QStandardItem):
        # why is this even necessary, why why why
        for each in args1:
            each.setEditable(False)

    @staticmethod
    def time_log(line : str, time_string="%Y.%m.%d-%H:%M:%S", spacer="\n", end="\n"):
        return f"{datetime.now().strftime(time_string)}{spacer}{line}{end}"


thisApp = QtWidgets.QApplication(sys.argv)
window = spcht_checker()
window.show()
sys.exit(thisApp.exec_())
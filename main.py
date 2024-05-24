import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel, QTableView
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt

BOOKS = pd.read_excel('./data.xlsx')

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        # self.dataset_view.clicked.connect(self.dataset_view1)
        self.graphic_report.clicked.connect(self.open_graphic_report)
        self.dataset_view = self.findChild(QPushButton, 'dataset_view')
        self.dataset_view.clicked.connect(self.show_dataset_view)

    def dataset_view1(self):
        self.dataset_window = DatasetView()
        self.dataset_window.show()

    def show_dataset_view(self):
        self.dataset_window = DatasetView(BOOKS)
        self.dataset_window.show()
    def open_graphic_report(self):
        # Логика для открытия отчета или другого окна
        print("Graphic report button clicked")
        # Пример:
        self.graphic_window = GraphicReportView()
        self.graphic_window.show()


class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._df = df

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[section]
            elif orientation == Qt.Vertical:
                return str(self._df.index[section])
        return None


class DatasetView(QDialog):
    def __init__(self, df):
        super().__init__()
        uic.loadUi('dataset_.ui', self)

        # Настройка QTableView
        self.dataset_view = self.findChild(QTableView, 'dataset_view')
        self.model = PandasModel(df)
        self.dataset_view.setModel(self.model)

class GraphicReportView(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('graphic_report.ui', self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

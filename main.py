import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel, QTableView, QWidget
import pandas as pd

import matplotlib.pyplot as plt
from PyQt5.QtCore import QAbstractTableModel, Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
        uic.loadUi('graphic_reports.ui', self)
        self.kach_kach.clicked.connect(self.kach_kach_clicked)

    def kach_kach_clicked(self):
        self.kach_kach_window = GraphicsReport_kach_kach()
        self.kach_kach_window.show()


class GraphicsReport_kach_kach(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('kach_kach_window.ui', self)
        self.bulid_btn.clicked.connect(self.bulid_btn_clicked)

    def bulid_btn_clicked(self):
        selected_text = self.comboBox.currentText().split(' - ')
        first_param, second_param = selected_text[0], selected_text[1]

        self.build_window = GraphicsReport_kach_kach_View(first_param, second_param)
        self.build_window.show()

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class GraphicsReport_kach_kach_View(QDialog):
    def __init__(self, first_param, second_param):
        super().__init__()
        self.first_param = first_param
        self.second_param = second_param


        self.setWindowTitle('Качественный-Качественный')
        self.setGeometry(100, 100, 800, 600)

        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Пример данных и создание DataFrame
        data = {
            self.first_param: BOOKS[self.first_param],
            self.second_param: BOOKS[self.second_param]
        }
        df = pd.DataFrame(data)
        # Исключение данных по стране "США"
        df = df[df[self.first_param] != 'USA']
        df = df[df[self.second_param] != 'USA']
        count_data = df.groupby([self.first_param, self.second_param]).size().unstack()

        # Создание кластеризованной столбчатой диаграммы
        count_data.plot(kind='bar', stacked=False, ax=sc.axes)
        sc.axes.set_xlabel(self.first_param)
        sc.axes.set_ylabel(self.second_param)
        sc.axes.set_title(f'Clustered Bar Chart for {self.first_param} and {self.second_param}')
        sc.axes.legend(title=self.second_param)

        layout = QVBoxLayout()
        layout.addWidget(sc)

        self.setLayout(layout)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

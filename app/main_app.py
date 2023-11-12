import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from frames.plot_symbols_nse import PlotSymbolsNSE
from frames.update_symbols_nse import UpdateSymbolsNSE
from frames.plotly_financial import PlotlyFinancial
import sqlite3
import csv

class StockPlotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db_connection = sqlite3.connect('stock_data.sqlite')
        # self.init_db()

        self.init_ui()
    def init_ui(self):
        self.setWindowTitle('Stock Plot App')

        # Buttons
        self.plot_button = QPushButton('NSE Price Plot', self)
        self.plot_button.clicked.connect(self.open_plot_symbols_nse)
        
        self.update_button = QPushButton('NSE Plotly Financial Plots', self)
        self.update_button.clicked.connect(self.open_plotly_financial)

        self.update_button = QPushButton('NSE Listings Update', self)
        self.update_button.clicked.connect(self.open_update_symbols_nse)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.plot_button)
        layout.addWidget(self.update_button)
        self.setLayout(layout)

    def open_plot_symbols_nse(self):
        self.plot_symbols_nse = PlotSymbolsNSE()
        self.plot_symbols_nse.show()

    def open_update_symbols_nse(self):
        self.update_symbols_nse = UpdateSymbolsNSE()
        self.update_symbols_nse.show()
    
    def open_plotly_financial(self):
        self.plotly_financial = PlotlyFinancial()
        self.plotly_financial.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockPlotApp()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())

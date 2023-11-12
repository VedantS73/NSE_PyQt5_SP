from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from nse_api import NSE
from datetime import date

class PlotSymbolsNSE(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Stock Plot App')
        self.setFixedSize(1300, 1000)

        # Widgets
        self.symbol_label = QLabel('Stock Symbol:')
        self.symbol_input = QLineEdit(self)
        self.start_date_label = QLabel('Start Date:')
        self.start_date_input = QDateEdit(self)
        self.start_date_input.setDate(date(2023, 1, 1))
        self.end_date_label = QLabel('End Date:')
        self.end_date_input = QDateEdit(self)
        self.end_date_input.setDate(date(2023, 11, 20))
        self.view_label = QLabel('View:')
        self.view_combo = QComboBox(self)
        self.view_combo.addItems(['Line', 'Candlestick'])
        self.plot_button = QPushButton('Plot', self)
        self.plot_button.clicked.connect(self.plot_stock)

        # Matplotlib Figure and Canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.symbol_label)
        layout.addWidget(self.symbol_input)
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_input)
        layout.addWidget(self.view_label)
        layout.addWidget(self.view_combo)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.canvas, stretch=6)
        self.setLayout(layout)

    def plot_stock(self):
        symbol = self.symbol_input.text()
        start_date = self.start_date_input.date().toPyDate()
        end_date = self.end_date_input.date().toPyDate()
        view_type = self.view_combo.currentText()

        if not symbol:
            return

        nse = NSE()
        df = nse.getHistoricalData(symbol, 'EQ', start_date, end_date)

        if df is not None and not df.empty:
            self.ax.clear()

            if view_type == 'Line':
                self.ax.plot(df['date'], df['close'], label='Close Price')
                self.ax.set_title('Stock Price Over Time (Line View)')
            elif view_type == 'Candlestick':
                self.ax.plot(df['date'], df['close'], label='Close Price', linestyle='--', marker='o', color='b')
                self.ax.vlines(df['date'], df['low'], df['high'], color='black', linewidth=1, label='Candlestick')
                self.ax.set_title('Stock Price Over Time (Candlestick View)')

            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Value')
            self.ax.legend()

            self.canvas.draw()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = PlotSymbolsNSE()
    window.show()
    sys.exit(app.exec_())
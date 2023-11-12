# plotly_stock_plot.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QComboBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from nse_api import NSE
import plotly.graph_objects as go
from datetime import date
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt

class PlotlyFinancial(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Stock Plot App (Plotly)')
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

        # Plotly WebEngineView
        self.web_view = QWebEngineView(self)

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
        layout.addWidget(self.web_view, stretch=6)
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
        
        print("Received data from NSE API")
        print(df)

        if df is not None and not df.empty:
            fig = go.Figure()

            if view_type == 'Line':
                fig.add_trace(go.Scatter(x=df['date'], y=df['prev_close'], mode='lines', name='Close Price'))
                fig.update_layout(title='Stock Price Over Time (Line View)', xaxis_title='Date', yaxis_title='Value')
            elif view_type == 'Candlestick':
                fig.add_trace(go.Candlestick(x=df['date'],
                                             open=df['open'],
                                             high=df['high'],
                                             low=df['low'],
                                             close=df['prev_close'],
                                             name='Candlestick'))
                fig.write_html('plotly_figure.html', full_html=False)
                self.web_view.setUrl(QUrl.fromLocalFile('plotly_figure.html'))

                fig.update_layout(title='Stock Price Over Time (Candlestick View)', xaxis_title='Date', yaxis_title='Value')

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = PlotlyFinancial()
    window.show()
    sys.exit(app.exec_())

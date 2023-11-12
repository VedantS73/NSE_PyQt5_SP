from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox
import sqlite3
import csv

class UpdateSymbolsNSE(QWidget):
    def __init__(self, parent=None):
        super(UpdateSymbolsNSE, self).__init__(parent)

        # Initialize SQLite database
        self.db_connection = sqlite3.connect('data.sqlite')
        self.init_db()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('NSE Listings Update')
        self.setFixedSize(1000, 800)

        # Content
        label = QLabel('This is the NSE Listings Update frame.')

        # Button to upload CSV
        upload_button = QPushButton('Upload CSV', self)
        upload_button.clicked.connect(self.upload_csv)

        # Table to display data
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # Assuming there are four columns in the table
        self.table.setHorizontalHeaderLabels(['ID', 'Symbol', 'Company Name', 'Market Cap'])

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(upload_button)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Load data into the table
        self.load_table_data()

    def init_db(self):
        # Create tables or perform any other database initialization
        with self.db_connection:
            cursor = self.db_connection.cursor()
            # Example: Creating a table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nse_symbols (
                    id INTEGER PRIMARY KEY,
                    symbol TEXT,
                    company_name TEXT,
                    mkt_cap REAL
                )
            ''')

    def upload_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        csv_file, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if csv_file:
            with open(csv_file, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Skip the header row

                with self.db_connection:
                    cursor = self.db_connection.cursor()

                    for row in csv_reader:
                        symbol = row[1].strip()
                        company_name = row[2].strip()
                        mkt_cap_str = row[3].replace(',', '').strip()
                        mkt_cap = None if not mkt_cap_str else float(mkt_cap_str)

                        cursor.execute('''
                            INSERT INTO nse_symbols (symbol, company_name, mkt_cap)
                            VALUES (?, ?, ?)
                        ''', (symbol, company_name, mkt_cap))

                    print('Imported data from CSV into the database')

            # Show a popup message
            self.show_popup('Database Update Complete', 'The database has been successfully updated.')

            # Load data into the table after updating the database
            self.load_table_data()

    def load_table_data(self):
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('SELECT * FROM nse_symbols')
            data = cursor.fetchall()

            self.table.setRowCount(len(data))

            for row_index, row_data in enumerate(data):
                for col_index, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row_index, col_index, item)
            company_name_column = self.table.horizontalHeader().visualIndex(2)  # Assuming "Company Name" is the third column (index 2)
            self.table.setColumnWidth(company_name_column, 600)  # Set the width as needed

    def closeEvent(self, event):
        # Close the SQLite connection when the widget is closed
        self.db_connection.close()
        event.accept()

    def show_popup(self, title, message):
        popup = QMessageBox()
        popup.setWindowTitle(title)
        popup.setText(message)
        popup.addButton(QMessageBox.Ok)
        popup.exec_()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = UpdateSymbolsNSE()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import pandas as pd
import os

# Dummy Twitter Auth Token for demonstration purposes
twitter_auth_token = '149d730626b18463799cd35c026c857751b9a9e2'

class TwitterScraperGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Twitter Scraper")
        self.setGeometry(100, 100, 400, 350)

        # Layout
        layout = QVBoxLayout()

        # Search Keyword input
        self.keyword_label = QLabel("Enter Search Keyword:")
        self.keyword_input = QLineEdit(self)

        # Date Range input (from date)
        self.from_date_label = QLabel("From Date (YYYY-MM-DD):")
        self.from_date_input = QLineEdit(self)

        # Date Range input (to date)
        self.to_date_label = QLabel("To Date (YYYY-MM-DD):")
        self.to_date_input = QLineEdit(self)

        # Language input
        self.lang_label = QLabel("Language (e.g. en):")
        self.lang_input = QLineEdit(self)

        # Limit input
        self.limit_label = QLabel("Enter Tweet Limit:")
        self.limit_input = QLineEdit(self)

        # Execute button
        self.run_button = QPushButton("Run Search", self)
        self.run_button.clicked.connect(self.run_search)

        # Add widgets to layout
        layout.addWidget(self.keyword_label)
        layout.addWidget(self.keyword_input)
        layout.addWidget(self.from_date_label)
        layout.addWidget(self.from_date_input)
        layout.addWidget(self.to_date_label)
        layout.addWidget(self.to_date_input)
        layout.addWidget(self.lang_label)
        layout.addWidget(self.lang_input)
        layout.addWidget(self.limit_label)
        layout.addWidget(self.limit_input)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def run_search(self):
        keyword = self.keyword_input.text()
        from_date = self.from_date_input.text()
        to_date = self.to_date_input.text()
        lang = self.lang_input.text()
        limit = self.limit_input.text()

        # Validate inputs
        if not keyword or not from_date or not to_date or not lang or not limit:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return

        try:
            limit = int(limit)  # Ensure limit is an integer
            # Build the search keyword for tweet-harvest
            search_keyword = f'{keyword} since:{from_date} until:{to_date} lang:{lang}'

            # Output filename
            filename = 'result.csv'

            # Run the tweet-harvest command
            os.system(f'npx -y tweet-harvest@2.6.1 -o "{filename}" -s "{search_keyword}" --tab "LATEST" -l {limit} --token {twitter_auth_token}')  # type: ignore

            # Process the result into an Excel file
            data = 'result.csv'
            result = pd.read_csv(data)
            result.to_excel('hasil.xlsx', index=False)

            QMessageBox.information(self, "Success", "Search completed and result saved as hasil.xlsx.")

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Tweet limit must be a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

# Run the GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TwitterScraperGUI()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
import os

class TweetScraperGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # Labels and input
        self.label_keyword = QLabel('Search Keyword:', self)
        self.input_keyword = QLineEdit(self)

        self.label_since = QLabel('Since (YYYY-MM-DD):', self)
        self.input_since = QLineEdit(self)

        self.label_until = QLabel('Until (YYYY-MM-DD):', self)
        self.input_until = QLineEdit(self)

        self.label_lang = QLabel('Language:', self)
        self.input_lang = QLineEdit(self)
        self.input_lang.setText('id')  

        self.label_limit = QLabel('Limit:', self)
        self.input_limit = QLineEdit(self)

        # Button to execute the scrawl
        self.scrape_button = QPushButton('Execute Scrawl', self)
        self.scrape_button.clicked.connect(self.execute_scrape)

        # Layouts
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_keyword)
        vbox.addWidget(self.input_keyword)

        vbox.addWidget(self.label_since)
        vbox.addWidget(self.input_since)

        vbox.addWidget(self.label_until)
        vbox.addWidget(self.input_until)

        vbox.addWidget(self.label_lang)
        vbox.addWidget(self.input_lang)

        vbox.addWidget(self.label_limit)
        vbox.addWidget(self.input_limit)

        vbox.addWidget(self.scrape_button)

        self.setLayout(vbox)
        self.setWindowTitle('Tweet Scraper')

    def execute_scrape(self):
        search_keyword = self.input_keyword.text()
        since = self.input_since.text()
        until = self.input_until.text()
        lang = self.input_lang.text()
        limit = self.input_limit.text()

        # Validate inputs
        if not search_keyword or not since or not until or not lang or not limit:
            QMessageBox.warning(self, "Input Error", "Please fill all the fields.")
            return

        try:
            limit = int(limit)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Limit must be a valid integer.")
            return

        # Format the search query
        search_query = f'{search_keyword} since:{since} until:{until} lang:{lang}'
        filename = 'uye.csv'
        twitter_auth_token = '149d730626b18463799cd35c026c857751b9a9e2'  # Add your Twitter API token here

        # Execute the tweet-harvest command
        command = f'npx -y tweet-harvest@2.6.1 -o "{filename}" -s "{search_query}" --tab "LATEST" -l {limit} --token {twitter_auth_token}'

        try:
            os.system(command)
            QMessageBox.information(self, "Success", f"Scraping completed and saved to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to execute command: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scraper_gui = TweetScraperGUI()
    scraper_gui.show()
    sys.exit(app.exec_())

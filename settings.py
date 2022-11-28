import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

NOMURL = 'https://nominatim.openstreetmap.org'

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings.ui'))


class SettingsWidget(QDialog, FORM_CLASS):
    def __init__(self, parent):
        super(SettingsWidget, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore)
        settings = QSettings()
        self.nominatimURL = settings.value('/BulkNominatim/URL', NOMURL)
        self.maxAddress = int(settings.value('/BulkNominatim/maxAddress', 100))
        self.language = settings.value('/BulkNominatim/language', 'en')
        self.levelOfDetail = int(settings.value('/BulkNominatim/levelOfDetail', 18))
        self.nomServiceLineEdit.setText(self.nominatimURL)
        self.maxRequestLineEdit.setText(str(self.maxAddress))
        self.languageLineEdit.setText(self.language)
        
    def accept(self):
        '''Accept the settings and save them for next time.'''
        settings = QSettings()
        self.nominatimURL = self.nomServiceLineEdit.text().strip()
        settings.setValue('/BulkNominatim/URL', self.nominatimURL)
        try:
            self.maxAddress = int(self.maxRequestLineEdit.text())
        except:
            self.maxAddress = 100
            self.maxRequestLineEdit.setText(str(self.maxAddress))
        settings.setValue('/BulkNominatim/maxAddress', self.maxAddress)
        self.language = self.languageLineEdit.text().strip()
        settings.setValue('/BulkNominatim/language', self.language)
        self.levelOfDetail = self.detailSpinBox.value()
        settings.setValue('/BulkNominatim/levelOfDetail', self.levelOfDetail)
        self.close()
        
    def restore(self):
        self.nomServiceLineEdit.setText(NOMURL)
        self.maxRequestLineEdit.setText(str(100))
        self.languageLineEdit.setText('en')
        self.detailSpinBox.setValue(18)

    def searchURL(self):
        return self.nominatimURL + '/search.php'
        
    def reverseURL(self):
        return self.nominatimURL + '/reverse.php'

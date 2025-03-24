import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PIL import Image

class ImageToPDFConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Convertitore Immagini in PDF')
        self.setWindowIcon(QIcon('./imgs/converter-ico.ico'))

        self.layout = QVBoxLayout()

        image_label = QLabel(self)
        image_label.setPixmap(QPixmap('./imgs/convert-image-to-pdf.png').scaled(250, 250, Qt.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(image_label)

        self.drop_label = QLabel("Trascina e rilascia le immagini qui", self)
        font = QFont("Times New Roman", 12)
        self.drop_label.setFont(font)
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.drop_label)

        self.file_list_label = QLabel(self)
        self.layout.addWidget(self.file_list_label)

        convert_button = QPushButton("Converti in PDF", self)
        convert_button.clicked.connect(self.convert_to_pdf)
        convert_button.setMinimumHeight(50)
        self.layout.addWidget(convert_button)

        self.setLayout(self.layout)
        self.setAcceptDrops(True)

        # Lista per memorizzare i file selezionati
        self.input_files = []

    def dragEnterEvent(self, event):
        # Accetta solo file
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # Ottieni i file trascinati
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.input_files = [file for file in file_paths if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.update_file_list_label()

    def update_file_list_label(self):
        if self.input_files:
            file_names = "\n".join([os.path.basename(file) for file in self.input_files])
            self.file_list_label.setText(f"File selezionati:\n{file_names}")
        else:
            self.file_list_label.clear()

    def convert_to_pdf(self):
        if not self.input_files:
            QMessageBox.warning(self, "Attenzione", "Nessun file selezionato!")
            return

        for img_path in self.input_files:
            try:
                # Apri l'immagine
                image = Image.open(img_path)
                # Definisci il percorso PDF
                pdf_path = os.path.splitext(img_path)[0] + ".pdf"
                # Salva come PDF
                image.convert("RGB").save(pdf_path, "PDF")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore durante la conversione di {img_path}: {e}")

        self.file_list_label.setText("Conversione completata!")
        self.input_files.clear()  # Resetta la lista dei file dopo la conversione


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageToPDFConverter()
    ex.setGeometry(300, 300, 400, 200)
    ex.show()
    sys.exit(app.exec_())

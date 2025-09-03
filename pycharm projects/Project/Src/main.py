
import glob
import io
import os
import sys

import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QTableWidgetItem
# from pyqtgraph.examples.crosshair import label
# import speech_recognition as sr
from ICS.Src.main.ATEC import Ui_MainWindow
from PyQt5.QtWebEngineWidgets import *
import folium
from folium.plugins import MousePosition
# will convert the image to text string

# adds image processing capabilities

# converts the text to speech
import pyttsx3
# Import docx NOT python-docx
# import docx
# translates into the mentioned lang uage

# Import libraries
import platform
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from ICS.Src.PlaylistModel import Player


########################################################################################################################
class MainSrc(QMainWindow, Ui_MainWindow):

    def _init_(self, parent=None, ):
        super(MainSrc, self)._init_(parent)
        self.setupUi(self)



       # Current date and time display to label
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start()
        self.Signals_and_Slots()
        self.stackedWidget.setCurrentWidget(self.page_Main)
        self.image_file_list = []

        self.PB_Audio_Records.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.page_Audio))
        self.PB_GIS_MAPS.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.page_GIS_Maps))
        self.LaunchGISMaps()
    ######################################################################
    def Signals_and_Slots(self):
        self.PB_Import_OCR.clicked.connect(self.ImportOCRFiles)
        self.PB_Rec_Text.clicked.connect(self.RecogniseText)
        self.PB_Play_OCR_Audio.clicked.connect(self.PlayOCRAudio)
        self.PB_Save_OCR_To_Word.clicked.connect(self.SaveOCR_to_Word_File)
        self.PB_Save_OCR_To_Text.clicked.connect(self.SaveOCR_to_Text_File)
        self.PB_Rot_OCR.clicked.connect(self.RotateImageOCR)
        self.PB_Import_Audio_Files.clicked.connect(self.getAudioRecords)

        self.PB_Import_OCR_PDF.clicked.connect(self.ImportPdfScannedFiles)
        self.PB_Import_OCR_PDF.clicked.connect(lambda : self.stackedWidget_2.setCurrentWidget(self.page_pdf_ocr))
        self.PB_Import_OCR.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.page_image_ocr))

        self.PB_OCR_IMAGE.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.page_OCR_TEXT))
        self.musicplayer = Player(None)
        self.VE_MusicPlayer.addWidget(self.musicplayer)
        self.PB_Play_Audio_to_Text.clicked.connect(self.ConvertAudiotoText)

    ######################################################################
    def showTime(self):
        self.time = QtCore.QDateTime.currentDateTime()
        self.timeDisplay = self.time.toString('dd-MM-yyyy hh:mm:ss ')
        self.label_date.setText(self.timeDisplay)
    ##################################################################################
    def ImportPdfScannedFiles(self):
        PDF_file, _ = QFileDialog.getOpenFileName(self, "Select File",os.getcwd(),"Pdf Files (*.pdf)")
        if not PDF_file:
            return

        # Windows also needs poppler_exe
        path_to_poppler_exe = Path(r'poppler/Library/bin')

        if platform.system() == "Windows":
            pdf_pages = convert_from_path(
                PDF_file, 500, poppler_path=path_to_poppler_exe
            )
        else:
            pdf_pages = convert_from_path(PDF_file, 500)
        # Read in the PDF file at 500 DPI
        # Iterate through all the pages stored above
        self.image_file_list = []
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            # enumerate() "counts" the pages for us.

            # Create a file name to store the image
            filename = f"page_{page_enumeration:03}.png"

            page.save(filename, "png")
            self.image_file_list.append(filename)
        print('filename',self.image_file_list[0])


        self.ocr_filename = os.path.basename(self.image_file_list[0])

        print(self.ocr_filename)


        pixmap = QPixmap(self.ocr_filename)
        # pixmap_resized = pixmap.scaled(600, 405, QtCore.Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(800,800,QtCore.Qt.KeepAspectRatio)
        self.label_OCR_TEXT_PDF.setPixmap(pixmap)
    ##################################################################################
    def RotateImageOCR(self):
        Original_Image = Image.open(self.ocr_filename)
        # Rotate Image By 180 Degree
        rotated_image = Original_Image.rotate(90)
        # self.ocr_filename = rotated_image
        # self.setImagetoLabel(label=self.label_OCR_TEXT)
        # pixmap = QPixmap(rotated_image)
        # self.label_OCR_TEXT.setPixmap(pixmap)
##################################################################################
    def ImportOCRFiles(self):
        # pass
        print('Hello')
        filter = "(*.png)"
        filenames, _ = QFileDialog.getOpenFileName(self, "Select File",os.getcwd(),"Images (*.png *.JPEG *.jpg)")
        if not filenames:
            return
        # if filenames:
        self.ocr_filename = os.path.basename(filenames)
        print(self.ocr_filename)
        print(filenames)
        # QFileDialog.setNameFilters([".doc",".xls"])
        # self.label = QLabel()
        self.setImagetoLabel(self.label_OCR_TEXT)
    ##################################################################################
    def setImagetoLabel(self,label = QLabel):
        pixmap = QPixmap(self.ocr_filename)
        # pixmap_resized = pixmap.scaled(600, 405, QtCore.Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(800,800,QtCore.Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        # self.setCentralWidget(self.label)
    ##################################################################################
    def RecogniseText(self):
        # opening an image from the source path
        img = Image.open(self.ocr_filename)

        # describes image format in the output
        print(img)
        # path where the tesseract module is installed
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        # converts the image to result and saves it into result variable
        result = pytesseract.image_to_string(img)
        # write text in a text file and save it to source path
        with open('abc.txt', mode='w') as file:
            file.write(result)
            print(result)
            self.textEdit_OCR_TEXT.setText(result)
    ##################################################################################
    def PlayOCRAudio(self):
        engine = pyttsx3.init()
        # an audio will be played which speaks the test if pyttsx3 recognizes it
        engine.say( self.textEdit_OCR_TEXT.toPlainText())
        engine.runAndWait()
    #######################################################################
    def SaveOCR_to_Text_File(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File",
                                                   os.getcwd(),"Images (*.txt)")
        if file_path:
            a = open(file_path, 'w')
            a.write(self.textEdit_OCR_TEXT.toPlainText())
            a.close()
    #######################################################################
    def SaveOCR_to_Word_File(self):
        # Create an instance of a word document
        doc = docx.Document()
        doc.add_paragraph(self.textEdit_OCR_TEXT.toPlainText())

        file_path, _ = QFileDialog.getSaveFileName(self, "Save File",
                                                   os.getcwd(),"Images (*.docx *.doc)")
        if file_path:
            # Now save the document to a location
            doc.save(file_path)
            # self.DisplayMessageActionLog(f'Data Saved to file {file_path}',
            #                              ColorCode=INFORMATION_COLOR_CODE)

    #######################################################################
    def getAudioRecords(self):
        path = "Speaker30_006"
        Audio_files = glob.glob(os.path.join(path, "*.wav"))
        print(Audio_files)
        df =pd.DataFrame(Audio_files,columns=['File Name'])
        print(df)
        self.UpdateAudiRecordsTable(dataframe=df)
    ######################################################################
    def UpdateAudiRecordsTable(self, dataframe=pd.DataFrame):
        self.tableWidget.setRowCount(dataframe.shape[0])
        self.tableWidget.setColumnCount(dataframe.shape[1])
        header_font = QFont()
        header_font.setPointSize(12)  # Set font size
        self.tableWidget.setHorizontalHeaderLabels(['File Name'])
        self.tableWidget.horizontalHeader().setFont(header_font)
        self.tableWidget.setFont(header_font)
        # self.tableWidget.setHorizontalHeaderLabels(dataframe.columns)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        for row in range(dataframe.shape[0]):
            for col in range(dataframe.shape[1]):
                # if col == 2:
                #     value_to_insert = dataframe.iat[row, col][int(self.CB_Ant_Num.currentText())]
                #     item = QTableWidgetItem(str(value_to_insert))
                # else:
                item = QTableWidgetItem(str(dataframe.iat[row, col]))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row, col, item)
        self.tableWidget.selectRow(self.tableWidget.rowCount() - 1)

    ######################################################################
    def ConvertAudiotoText(self):
        r = sr.Recognizer()
        rowindex = self.tableWidget.currentRow()
        filename = self.tableWidget.currentItem().text()
        print(filename)
        with sr.AudioFile(filename) as source:
            audio = r.record(source)
            try:
                s = r.recognize_google(audio)
                print("Text: " + s)

            except Exception as e:
                print("Exception: " + str(e))
        self.textEdit.setText(s)

    def LaunchGISMaps(self):
        self.View = QWebEngineView(self)
        self.m = folium.Map([32.9228,75.1313], zoom_start=13, max_zoom=32,
                            min_zoom=1,
                            # min_lat=self.Complete_Image_Data[0][0], min_lon=self.Complete_Image_Data[0][1],
                            # max_lat=self.Complete_Image_Data[1][0], max_lon=self.Complete_Image_Data[1][1],
                            max_bounds=True, zoom_control=True)
        # folium.raster_layers.ImageOverlay(
        #     image=self.Site_Info_Folder + '/Site_Map.jpg',
        #     bounds=self.Complete_Image_Data[0:]).add_to(self.m)
        folium.LatLngPopup().add_to(self.m)
        formatter = "function(num) {return L.Util.formatNum(num, 5) + ' º ';};"
        MousePosition(
            position='topright',
            separator=' | ',
            empty_string='NaN',
            lng_first=False,
            num_digits=20,
            prefix='Coordinates:',
            lat_formatter=formatter,
            lng_formatter=formatter).add_to(self.m)
        icon = 'icons/Harries.png'
        folium.Marker([32.9228,75.2145],
                      icon=folium.CustomIcon(icon_image=icon, icon_size=(40, 80)),
                      popup=str('Station Id : 1 , Operator Info: xxx'),
                          tooltip=str('Click to Make Call')
                      ).add_to(self.m)

        icon = 'icons/DMR.png'
        folium.Marker([32.9458,75.1313],
                      icon=folium.CustomIcon(icon_image=icon, icon_size=(80, 80)),
                      popup=str('Station Id : 1 , Operator Info: Bravo3'),
                          tooltip=str('Click to Make Call')
                      ).add_to(self.m)

        icon = 'icons/Motorola.png'
        folium.Marker([32.9587,75.1756],
                      icon=folium.CustomIcon(icon_image=icon, icon_size=(40, 60)),
                      popup=str('Station Id : 1 , Operator Info: Bravo3'),
                          tooltip=str('Click to Make Call')
                      ).add_to(self.m)

        icon = 'icons/ICP.png'
        folium.Marker([32.9228,75.1313],
                      icon=folium.CustomIcon(icon_image=icon, icon_size=(150, 150)),
                      popup=str('Station Id : ICP'),
                          # tooltip=str('Click to Make Call')
                      ).add_to(self.m)

        data = io.BytesIO()
        self.originalmap = self.m
        self.m.save(data, close_file=False)
        self.View.reload()
        self.View.setHtml(data.getvalue().decode())
        self.VE_GISMaps.addWidget(self.View)
########################################################################################################################
if _name_ == "_main_":
    app = QApplication(sys.argv)
    win = MainSrc()
    win.show()
    sys.exit(app.exec_())
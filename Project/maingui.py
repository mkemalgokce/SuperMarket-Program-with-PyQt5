from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from main import *
import sys 

class mainWindow(QWidget):
    main = Main()
    def __init__(self):
        super().__init__()
        self.setUi()
    
    def setUi(self):
        self.ana_Ayarlar()
        self.layer1()

    def ana_Ayarlar(self):
        self.setWindowIcon(QIcon(("login.png")))
        self.setWindowTitle('Market Sistemi')
        self.setGeometry(0,0,1920,1080)
        self.setMinimumSize(960,540)

    def layer1(self):
        vBox = QVBoxLayout()
        hBox = QHBoxLayout()
        #table func
        table = self.create_Table()

        #Butonlar
        b_UrunEkle = QPushButton('Urun Ekle',self)
        b_UrunSil = QPushButton('Urun Sil',self)
        b_UrunAra = QPushButton('Urun Ara',self)
        b_StokEkle = QPushButton('Stok Ekle',self)
        b_UrunSat = QPushButton('Sat',self)
        b_KasayiGor = QPushButton('Bakiyeyi Gor',self)
        b_kasaGiris = QPushButton('Kasa Para Al / Para Ekle',self)

        #Butonlarin Fonksiyonlari
        b_UrunEkle.clicked.connect(self.b_EkleFunction)
        b_UrunSil.clicked.connect(self.deleteClicked)
        b_UrunAra.clicked.connect(self.b_AraFunction)
        b_KasayiGor.clicked.connect(self.b_KasaFunction)
        b_StokEkle.clicked.connect(self.b_StokFunction)
        b_kasaGiris.clicked.connect(self.b_kasaGirisFunc)
        b_UrunSat.clicked.connect(self.b_UrunSatFunc)

        vBox.addWidget(table)
        vBox.addLayout(hBox)
        hBox.addWidget(b_UrunEkle)
        hBox.addWidget(b_UrunSil)
        hBox.addWidget(b_UrunAra)
        hBox.addWidget(b_StokEkle)
        hBox.addWidget(b_UrunSat)
        hBox.addWidget(b_KasayiGor)
        hBox.addWidget(b_kasaGiris)


        self.setLayout(vBox)
       
    def create_Table(self):
        
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)

        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(("Urun No.", "Isim", "Son Satim Tarihi", "Son Alim Tarihi", "Stok","Alis Fiyati","Satis Fiyati"))
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.load_Data()

        return self.table
    def load_Data(self):
        self.main.database.c.execute("SELECT * FROM urunler")
        urunler = self.main.database.c.fetchall()
        self.table.setRowCount(len(urunler))
        row = 0
        for urun in urunler:
            self.table.setItem(row , 0 , QTableWidgetItem(str(urun[0])))
            self.table.setItem(row , 1 , QTableWidgetItem(urun[1]))
            self.table.setItem(row , 2 , QTableWidgetItem(urun[2]))
            self.table.setItem(row , 3 , QTableWidgetItem(urun[3]))
            self.table.setItem(row , 4 , QTableWidgetItem(str(urun[4])))
            self.table.setItem(row , 5 , QTableWidgetItem(str(urun[5])))
            self.table.setItem(row , 6 , QTableWidgetItem(str(urun[6])))
            row +=1
            
            

    def b_EkleFunction(self):
        
        self.ekleDialog = QDialog()
        self.ekleDialog.setFixedSize(300,300)

        lbl_0 = QLabel('Isim ',self.ekleDialog)
        lbl_2 = QLabel('Stok',self.ekleDialog)
        lbl_3 = QLabel('Alis Fiyati',self.ekleDialog)
        lbl_4 = QLabel('Satis Fiyati',self.ekleDialog)

        self.in_name = QLineEdit(self.ekleDialog)
        self.in_name.setPlaceholderText('Urun ismi giriniz.')
        self.in_stok = QLineEdit(self.ekleDialog)
        self.in_stok.setPlaceholderText('Adet ya da Kg Giriniz.')
        self.in_stok.setValidator(QDoubleValidator())
        self.in_alisFiyat = QLineEdit(self.ekleDialog)
        self.in_alisFiyat.setPlaceholderText('TL')
        self.in_alisFiyat.setValidator(QDoubleValidator())
        self.in_satisFiyat = QLineEdit(self.ekleDialog)
        ekle_Button = QPushButton('Ekle',self.ekleDialog)
        self.in_satisFiyat.setValidator(QDoubleValidator())
        
        vBox = QVBoxLayout()

        vBox.addWidget(lbl_0)
        vBox.addWidget(self.in_name)
        vBox.addWidget(lbl_2)
        vBox.addWidget(self.in_stok)
        vBox.addWidget(lbl_3)
        vBox.addWidget(self.in_alisFiyat)
        vBox.addWidget(lbl_4)
        vBox.addWidget(self.in_satisFiyat)
        vBox.addWidget(ekle_Button)
        
        ekle_Button.clicked.connect(self.dialogEkleButton)
        self.ekleDialog.setLayout(vBox)
        self.ekleDialog.exec()

    def deleteClicked(self):
        if(self.table.selectedIndexes()==[]):
            self.hataDialog('Urun Secilmedi.')
        else :
            self.main.deleteProduct(self.table.selectedIndexes())
            self.load_Data()

    def b_AraFunction(self):
        self.araDialog = QDialog(self)
        
        self.araDialog.setFixedSize(300,120)
        lbl_AraDialog = QLabel('Aramak Istediginiz Urunun Adini Giriniz.',self.araDialog)
        lbl_AraDialog.setAlignment(Qt.AlignCenter)
        self.lE_AraDialog = QLineEdit(self.araDialog)
        self.lE_AraDialog.setPlaceholderText('Urun ismini giriniz.')
        b_AraDialog = QPushButton('Ara',self.araDialog)

        vBox = QVBoxLayout()

        vBox.addWidget(lbl_AraDialog)
        vBox.addWidget(self.lE_AraDialog)
        vBox.addWidget(b_AraDialog)

        b_AraDialog.clicked.connect(self.araDialogFunc)
        self.araDialog.setLayout(vBox)
        self.araDialog.exec()



    def dialogEkleButton(self):
        today = str(datetime.datetime.now())
        today = today.split('.')[0]
        if(self.in_stok.text()=='' or self.in_alisFiyat.text()=='' or self.in_satisFiyat.text()==''):
            self.hataDialog('Hata tum bilgileri giriniz.')
        else :

            r =self.main.addProduct(self.in_name.text(),today,float(self.in_stok.text()),float(self.in_alisFiyat.text()),float(self.in_satisFiyat.text()))
            if(r == 0):
                self.hataDialog('Ayni Urun Var.')
            else :
                self.load_Data()
                self.ekleDialog.hide()
        
    
    def araDialogFunc(self):
        #self.table.selectedIndexes()[0].data()
        name = self.lE_AraDialog.text()
        data = self.main.findProduct(name)
        if (data != 0):
            data =self.main.findProduct(name)[1]
            for i in range(0,self.main.database.getRowCount()):
                if str(data) == self.table.item(i,0).text():
                    self.table.selectRow(i)
                    break
        else : 
            error_dialog = QMessageBox(self.araDialog)
            lbl = QLabel('Urun Bulunamadi.',error_dialog)
            lbl.setFont(QFont('Arial', 12))
            lbl.setAlignment(Qt.AlignCenter)
            error_dialog.exec()

    def b_KasaFunction(self):
        msgKasa = QMessageBox(self)
        newLabel = QLabel(msgKasa)
        msgKasa.setStyleSheet("QLabel{min-width: 150px;}");
        newLabel.setText('Bakiye : '+str(round(self.main.database.getBakiye(), 4))+'TL')
        newLabel.setAlignment(Qt.AlignCenter)
        msgKasa.exec()
    
    def b_StokFunction(self):
        self.stokDialog = QDialog(self)

        vBox = QVBoxLayout()

        lbl_Isim = QLabel('Isim Giriniz',self.stokDialog)
        self.lE_Isim = QLineEdit(self.stokDialog)
        lbl_Adet = QLabel('Stok Adeti Giriniz',self.stokDialog)
        self.lE_StokAdeti = QLineEdit(self.stokDialog)
        lbl_AlisFiyati = QLabel('Alis Fiyati Giriniz',self.stokDialog)
        self.lE_AlisFiyati = QLineEdit(self.stokDialog)
        btn_Ekle = QPushButton('Ekle',self.stokDialog)

        vBox.addWidget(lbl_Isim)
        vBox.addWidget(self.lE_Isim)
        vBox.addWidget(lbl_Adet)
        vBox.addWidget(self.lE_StokAdeti)
        vBox.addWidget(lbl_AlisFiyati)
        vBox.addWidget(self.lE_AlisFiyati)
        vBox.addWidget(btn_Ekle)

        btn_Ekle.clicked.connect(self.btn_EkleFunc)
        self.stokDialog.setLayout(vBox)
        self.stokDialog.exec()

    def btn_EkleFunc(self):
       
        if self.main.addStock(self.lE_Isim.text(),int(self.lE_StokAdeti.text()),int(self.lE_AlisFiyati.text())) == 0 :
            self.hataDialog('Urun Bulunamadi .')
        else :
            self.main.addStock(self.lE_Isim.text(),int(self.lE_StokAdeti.text()),int(self.lE_AlisFiyati.text()))
            self.load_Data()
            self.stokDialog.hide()

    def b_kasaGirisFunc(self):
       self.kasaGirisDialog = QDialog(self)

       vBox = QVBoxLayout()

       lbl1 = QLabel('Parayi Giriniz.')
       self.lE_Para = QLineEdit()
       self.lE_Para.setPlaceholderText('TL')
       btn1 = QPushButton('Ekle',self.kasaGirisDialog)
       btn2 = QPushButton('Al',self.kasaGirisDialog)

       btn1.clicked.connect(self.para_Ekle)
       btn2.clicked.connect(self.para_Al)

       vBox.addWidget(lbl1)
       vBox.addWidget(self.lE_Para)
       vBox.addWidget(btn1)
       vBox.addWidget(btn2)

       self.kasaGirisDialog.setLayout(vBox)

       self.kasaGirisDialog.exec()

    def para_Ekle(self):
        bakiye = round(self.main.database.getBakiye(), 4)
        bakiye += float(self.lE_Para.text())
        date = str(datetime.datetime.now())
        date = date.split('.')[0]
        self.main.database.logandBakiye('+'+self.lE_Para.text()+' Kasaya Para Eklendi'+'('+date+')',bakiye)
        self.load_Data()
        self.kasaGirisDialog.hide()
    
    def para_Al(self):
        bakiye = round(self.main.database.getBakiye(), 4)
        bakiye -= float(self.lE_Para.text())
        date = str(datetime.datetime.now())
        date = date.split('.')[0]
        self.main.database.logandBakiye('-'+self.lE_Para.text()+'Kasadan para Alindi'+'('+date+')',bakiye)
        self.load_Data()
        self.kasaGirisDialog.hide()


    def hataDialog(self,strErr):
        errBox = QMessageBox(self)
        errBox.setStyleSheet("QLabel{min-width: 200px;}");
        errLabel = QLabel(errBox)
        errLabel.setText('Hata ! , ' + strErr)
        errLabel.setAlignment(Qt.AlignCenter)
        errBox.exec()

    def b_UrunSatFunc(self):
        self.satDialog = QDialog()
        vBox = QVBoxLayout()

       
        lbl1 = QLabel('Urun Adini Giriniz.',self.satDialog)
        self.lE_satIsim = QLineEdit(self.satDialog)
        lbl2 = QLabel('Miktari Giriniz')
        self.lE_satMiktar = QLineEdit(self.satDialog)
        btn = QPushButton('Onayla')

        btn.clicked.connect(self.satOnaylaFunc)
        vBox.addWidget(lbl1)
        vBox.addWidget(self.lE_satIsim)
        vBox.addWidget(lbl2)
        vBox.addWidget(self.lE_satMiktar)
        vBox.addWidget(btn)

        self.satDialog.setLayout(vBox)
        self.satDialog.exec()
    def satOnaylaFunc(self):
        date = str(datetime.datetime.now())
        date = date.split('.')[0]
        data = self.main.database.getRow(self.lE_satIsim.text())
        print(data)
        if(data == None):
            self.hataDialog('Urun Bulunamadi.')
        else :

            satStok = float(self.lE_satMiktar.text())
            stok = data[-3]
            satFiyat = data[-1]
            if(stok>=satStok):
                newStok = stok - satStok
                newBakiye = self.main.database.getBakiye() + satStok*satFiyat
                self.main.database.logandBakiye('+'+str(newBakiye)+' '+self.lE_satIsim.text()+' satis yapildi'+'('+date+')',newBakiye)
                self.main.database.satisYap(self.lE_satIsim.text(),newStok)
                self.load_Data()
                self.satDialog.hide()
            else:
                self.hataDialog('Urun adeti yanlis !')
            


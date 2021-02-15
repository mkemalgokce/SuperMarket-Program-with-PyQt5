import random 
from mydatabase import *



class Main():
    database = dataBase()
    def __init__(self):
        super().__init__()
        self
        
    def findProduct(self,name):
        if(self.database.findRow(name) != None):
            return self.database.findRow(name)
        else :
            return 0

    def addProduct(self,name=str,alimTarihi=str,stok=float,fiyatAlis=float,fiyatSatis=float):
        id = random.randint(10**11,10**12)
        if self.database.addRow(id,name,'-',alimTarihi,stok,fiyatAlis,fiyatSatis):
            date = str(datetime.datetime.now())
            date = date.split('.')[0]
            newBakiye = self.database.getBakiye() - (stok * fiyatAlis)
            logString = name +' '+ str(stok) +' adet/kg urunu Eklendi ' + '('+date+')'
            self.database.logandBakiye(logString,newBakiye) 
        else :
            return 0
        

    def addStock(self,name=str,stockCount=int,alisFiyati=int):
        date = str(datetime.datetime.now())
        date = date.split('.')[0]
        logString = name + ' ' + str(stockCount) + ' adet/kg stok Eklendi' + '('+date+')'
        newBakiye = self.database.getBakiye() - (stockCount * alisFiyati)
        self.database.logandBakiye(logString,newBakiye)
        if(self.findProduct(name)== 0):
            return 0 # error
        else : 
            self.database.updateRow(name,self.findProduct(name)[-3]+stockCount,alisFiyati)
    
    def deleteProduct(self,data):
        date = str(datetime.datetime.now())
        date = date.split('.')[0]
        self.database.deleteRow(data[1].data())
        self.database.logandBakiye(data[1].data()+' urunu silindi.'+' ('+date+' )',self.database.getBakiye())



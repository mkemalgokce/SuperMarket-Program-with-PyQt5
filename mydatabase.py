import sqlite3
import datetime
class dataBase():
    conn = None
    c = None
    def __init__(self):
        self.createTable()
    def createTable(self):
        self.conn = sqlite3.connect('urundb.db')
        self.c = self.conn.cursor()
        #Urun bilgilerinin tutuldugu db
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS Urunler 
        (urunid INT,name TEXT PRIMARY KEY, satimTarihi TEXT , alimTarihi TEXT ,stok INT ,fiyatAlis REAL, fiyatSatis REAL)''')
        #Bakiyenin tutuldugu ve loglamanin yapildigi db
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS Bakiye 
        (logData TEXT PRIMARY KEY , bakiye INT)''')
        self.c.execute(''' 
        INSERT OR IGNORE INTO Bakiye VALUES('Ana Bakiye',0)
        ''')
        self.conn.commit()

    def addRow(self,urunid =int ,name=str,satimTarihi=str,alimTarihi=str,stok=int,fiyatAlis=float,fiyatSatis=float):
        ilk  = self.getRowCount()
        self.c.execute(''' 
        INSERT OR IGNORE INTO Urunler 
        VALUES(?,?,?,?,?,?,?)''',
        (urunid,name,satimTarihi,alimTarihi,stok,fiyatAlis,fiyatSatis))
        son = self.getRowCount()
        if(son - ilk == 0):
            return 0
        return 1
        self.conn.commit()
    
    def findRow(self,name=str):
        self.c.execute("SELECT rowid, * FROM Urunler WHERE name Like ?",('%'+name+'%',))
        data = self.c.fetchone()

        return data

    def getRow(self,name=str):
        self.c.execute('SELECT rowid, * FROM Urunler WHERE name = ?',(name,))
        data = self.c.fetchone()
        return data
    def deleteRow(self,name=str,columnid= int):
        self.c.execute('delete from Urunler where name=?',(name,))
        self.conn.commit()
    def updateRow(self,name=str,stok=int,fiyatAlis=float):
        today= datetime.date.today()
        today = today.strftime("%d.%m.%Y")
        self.c.execute('UPDATE Urunler SET stok = ? , alimTarihi = ? ,fiyatAlis = ? WHERE name = ?',(stok,today,fiyatAlis,name,))
        
        self.conn.commit()
        
    def getRowCount(self):
        self.c.execute("select * from Urunler")
        results = self.c.fetchall()
        rowCount = len(results)
        return rowCount
    
    def logandBakiye(self,logData = str , bakiye = int):
        self.c.execute("INSERT OR REPLACE INTO Bakiye VALUES(?,?)",(logData,bakiye,))
        self.conn.commit()
    def getBakiye(self):
        last_row = self.c.execute('select * from bakiye').fetchall()[-1][-1]
        return last_row
    def satisYap(self,name,stok):
        today = str(datetime.datetime.now())
        today = today.split('.')[0]
        self.c.execute('UPDATE Urunler SET stok = ? ,satimTarihi = ? WHERE name = ?',(stok,today,name,))
        self.conn.commit()

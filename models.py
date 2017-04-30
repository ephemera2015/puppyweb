from sqlorm import *
import datetime
    
class User(TableBase):
    
    uid=IntField(primary_key=True,auto_increment=True)
    uname=StringField(nullable=False,unique=True)
    upwd=StringField(nullable=False)
    uavatar=StringField(nullable=False)
    
class Entry(TableBase):
    
    eid=IntField(primary_key=True,auto_increment=True)
    etitle=StringField(nullable=False)
    econtent=StringField(nullable=False)
    eimgs=StringField()
    etimestamp=DateTimeField(default=datetime.datetime.now)
    uid=IntField(foreign_key=User.uid)
    
def connectDataBase(db_name):
    TableBase.connect(db_name)
        
def createAllModels(db_name,drop_existing=False):
     TableBase.connect(db_name)
     TableBase.createAll(drop_existing)
     TableBase.close()

def closeDataBase():
    TableBase.close()
    
if __name__=='__main__':
    from config import DATABASE
    createAllModels(DATABASE,True)

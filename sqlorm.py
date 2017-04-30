#-*-conding:utf-8-*-
import sqlite3

class Field(object):
    
    def __init__(self,primary_key=False,auto_increment=False,foreign_key=None,nullable=True,unique=False,default=None):
        self.primary_key=primary_key
        self.foreign_key=foreign_key
        self.nullable=nullable
        self.auto_increment=auto_increment
        self.default=default
        self.unique=unique
        
    def fieldMap(self):
        return None
    
    def tosql(self,v):
        return None
        

        
class IntField(Field):
    
    def fieldMap(self):
        return 'integer'
        
    def tosql(self,v):
        return str(v)
    
class BinaryField(Field):
        
    def fieldMap(self):
        return 'blob'
        
    def tosql(self,v):
        return v 
    
class StringField(Field):
    
    def fieldMap(self):
        return 'text'
        
    def tosql(self,v):
        return r"'"+v+r"'"
    
class DateTimeField(Field):
        
    def fieldMap(self):
        return 'text'
    
    def tosql(self,v):
        return r"'"+str(v)+r"'"

def findAttrName(x):
    for child in TableBase.__subclasses__():
        #print child.__dict__.keys()
        for attr in child.__dict__.keys():
            if x is child.__dict__[attr]:
                return child,attr     
                    
class TableMeta(type):

    def __new__(cls,name,bases,attrs):
        maps={}
        for k,v in attrs.items():
            if isinstance(v,Field):
                maps[k]=v
        '''for k in maps.keys():
            attrs.pop(k)'''
        attrs['__table__']=name
        attrs['__mapping__']=maps
        return type.__new__(cls,name,bases,attrs)
        
class FactoryRow(dict):
    def __getattr__(self,k):
        return self.get(k)
        
class TableBase():
    
    __metaclass__=TableMeta
    db=None
    
    @classmethod
    def connect(cls,db_name):
        cls.db=sqlite3.connect(db_name)
        def foo(cursor,row):
            x=FactoryRow()
            for idx,col in enumerate(cursor.description):
                x[col[0]]=row[idx]
            return x
        cls.db.row_factory=foo
    
    @classmethod
    def close(cls):
        if cls.db:
            cls.db.close()
            cls.db=None
            
    @classmethod
    def rawsql(cls,sql):
        return cls.db.execute(sql)
    
    @classmethod
    def insert(cls,**args):
        try:
            sql='insert into '+cls.__name__+'('
            keys=cls.__mapping__.keys()
            akeys=args.keys()
            for k in akeys:
                if not k in keys:
                    raise AttributeError(cls.__name__+' has no attribute '+k)
            for k in keys:
                if (not k in akeys) and (cls.__mapping__[k].default):
                    try:
                        args[k]=cls.__mapping__[k].default() 
                    except:
                        args[k]=cls.__mapping__[k].default 
            sql+=','.join(args.keys())
            sql+=') values('
            values=(cls.__mapping__[k].tosql(v) for k,v in args.items() )
            sql+=','.join(values)+');'
            #print sql;
            cls.db.execute(sql)
            cls.db.commit()
            return True
        except:
            return False

        
    @classmethod
    def update(cls,condition,**value):
        sql='update '+cls.__name__+' set '
        for k,v in value.items():
            sql+=k+' = '+cls.__mapping__[k].tosql(v)+', '
        sql=sql[:-2]
        sql+=' where '+condition
        cls.db.execute(sql)
        cls.db.commit()
   
    @classmethod
    def delete(cls,condition):
        sql='delete from '+cls.__name__+' where '+condition
        cls.db.execute(sql)
        cls.db.commit()
        
    @classmethod
    def one(cls):
        sql='select * from '+cls.__name__
        return cls.db.execute(sql).fetchone()     
         
    @classmethod
    def all(cls):
        sql='select * from '+cls.__name__
        return cls.db.execute(sql).fetchall()
        
    @classmethod
    def query(cls,condition,fields=None):
        if not fields:
            sql='select * from '+cls.__name__+' where '+condition
        else:
            sql='select '
            for f in fields:
                c,name=findAttrName(f)
                sql+=c.__name__+'.'+name+', '
            sql=sql[0:-2]
            sql+=' from '+cls.__name__+' where '+condition
        #print sql
        return cls.db.execute(sql).fetchall()
                    
    @classmethod    
    def exists(cls,condition):
        rv=cls.query(condition)
        return bool(rv)
    
    @classmethod
    def join(cls,b,natural=True):
        if natural:
            return type(cls.__name__+' natural join '+b.__name__,(TableBase,),{})
        return type(cls.__name__+','+b.__name__,(TableBase,),{})
        
    @classmethod
    def createAll(cls,drop_existing=False):
        sql=''
        for child in cls.__subclasses__():
            if sql:
                sql+='\n'
            if drop_existing:
                sql+='drop table if exists '+child.__name__+';\n'
            sql+='create table '+child.__name__+'(\n'
            foreign_keys=[]
            for k,v in child.__mapping__.items():
                sql+=k+' '
                sql+=v.fieldMap()
                if v.primary_key:
                    sql+=' primary key'
                    if v.auto_increment:
                        sql+=' autoincrement'
                if not v.nullable:
                    sql+=' not null'
                if v.unique:
                    sql+=' unique'
                if v.foreign_key:
                    foreign_keys.append((k,v.foreign_key))
                sql+=',\n'
            if  not foreign_keys:
                sql=sql[:-2]
            for f in foreign_keys:
                c,n=findAttrName(f[1])
                sql+='foreign key('+f[0]+') references '+c.__name__+'('+n+');\n'
            if foreign_keys:
                sql=sql[:-2]    
            sql+= '\n);'
        #print sql 
        cls.db.executescript(sql)
        

def And(x,y):
    return '('+x+')'+' and '+'('+y+')'
    
def Or(x,y):
    return '('+x+')'+' or '+'('+y+')'

def _getXY(x,y):
    cls,name=findAttrName(x)
    try:
        a,n=findAttrName(y)
        v=a.__name__+'.'+n
    except:
        v=cls.__mapping__[name].tosql(y)
    return cls.__name__+'.'+name,v
    
def Eq(x,y):
    a,b=_getXY(x,y)
    return a+' = '+b

def Neq(x,y):
    a,b=_getXY(x,y)
    return a+' != '+b
    
def Gt(x,y):
    a,b=_getXY(x,y)
    return a+' > '+b

def Lt(x,y):
    a,b=_getXY(x,y)
    return a+' < '+b
    
def Geq(x,y):
    a,b=_getXY(x,y)
    return a+' >= '+b

def Leq(x,y):
    a,b=_getXY(x,y)
    return a+' <= '+b
    
def Like(x,y):
    a,b=_getXY(x,y)
    return a+' like '+b
    
def Nlike(x,y):
    a,b=_getXY(x,y)
    return a+' not like '+b  

if __name__=='__main__':
    pass
    
    
    
    
    
    
    
    

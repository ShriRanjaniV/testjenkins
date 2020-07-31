from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DBBASE = declarative_base()
engine = create_engine('postgresql+psycopg2://anirudh:Intain@35.206.254.216/anirudh')

class User(DBBASE):
    '''
    user_id - user email id
    transaction_id - UID
    '''
    __tablename__ = 'userdetails'
    user_id = Column(String, nullable = False)
    transaction_id = Column(String, primary_key=True)
    def __init__(self, email, uid):
        self.user_id = email
        self.transaction_id = uid
    
    @staticmethod
    def check_upload(uid, session):
        user = DBBASE.metadata.tables['userdetails']
        query_result = session.execute(user.select())
        session.close()
        data = [list(row) for row in query_result]
        for row in data:
            if uid == row[1]:
                return False
        return True
    
    @staticmethod
    def insert_upload(uid, email):
        Session = sessionmaker(bind = engine)
        session = Session()
        if User.check_upload(uid=uid, session=session):
            u1 = User(email=email,uid=uid)
            session.add(u1)
            session.commit()
        else:
            print('UID is present please use a new one')
            return False
        return True

class Tranasaction(DBBASE):
    
    '''
    process_id - auto incremented value
    step_id - is a int value, upload = 1; classifier = 2; extract = 3; verification = 4; profile = 5
    transaction_id - Foreign key between 2 Tables
    ''' 

    __tablename__ = 'processdetails'
    process_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String, ForeignKey('userdetails.transaction_id'), nullable=False)
    step_id = Column(String)
    time_stamp = Column(DateTime)

    def __init__(self,current,uid):
        self.transaction_id = uid
        self.time_stamp = datetime.datetime.now()
        self.step_id = current
    
    @staticmethod
    def check_user(user_id, session, uid):
        user = DBBASE.metadata.tables['userdetails']
        user_result = session.execute(user.select())
        session.close()
        user_data = [list(row) for row in user_result]
        if [user_id,uid] in user_data:
            return True
        return False
    
    @staticmethod
    def check_transaction(uid, step, user_id):
        Session = sessionmaker(bind = engine)
        session = Session()
        process = DBBASE.metadata.tables['processdetails']
        transaction_result = session.query().with_entities(process.c.transaction_id,process.c.step_id)
        transaction_data = [list(row) for row in transaction_result]
        last_step = int(step) - 1
        if Tranasaction.check_user(user_id=user_id,session=session,uid=uid):
            if [uid,str(last_step)] in transaction_data:
                return True
            else:
                print("Previuos step isn't finished")
                return False
        else:
            print("User isn't given access for this endpoint")
            return False

    @staticmethod
    def insert_process(user, uid, step):
        Session = sessionmaker(bind = engine)
        session = Session()
        t1 = Tranasaction(current=step,uid=uid)
        session.add(t1)
        session.commit()
        session.close()
'''
result = engine.execute(User.metadata.tables['userdetails'].select())
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
u1 = User(email='kamesh1164@gmail.com',uid='1111111111111111')
session.add(u1)
session.commit()
user = DBBASE.metadata.tables['userdetails']
tranasaction = DBBASE.metadata.tables['processdetails']
'''
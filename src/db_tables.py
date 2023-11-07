from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import String, Integer, DateTime, Boolean
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import os


HOST_IP = "localhost" 
db_string = f"postgresql://praktikum:praktikum@{HOST_IP}:9876/smarthome"
engine = create_engine(db_string)

if not database_exists(engine.url):
    print("[DB-Manager] SmarthomeDB created")
    create_database(engine.url)
else:
    print("[DB-Manager] SmarthomeDB already exist")
    exit

engine.connect()
base = declarative_base()
conn = engine.connect()
Session = sessionmaker()


class Sensor_logs(base):
    __tablename__ = "sensor_logs"
    id = Column(Integer, primary_key=True)
    sid = Column(Integer)
    time = Column(String(100))
    value = Column(String(100))

class Sensors(base):
    __tablename__ = "sensors"
    sid = Column(Integer, primary_key=True)
    uuid = Column(Integer)
    sensor_type = Column(String(100))
    name = Column(String(100))
    renamed = Column(Boolean)
    

base.metadata.create_all(conn)
print("[DB-Manager] SmarthomeDB Tables created")
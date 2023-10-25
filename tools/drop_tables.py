from sqlalchemy_utils import drop_database
from sqlalchemy import create_engine


HOST_IP = "localhost" 
db_string = f"postgresql://praktikum:praktikum@{HOST_IP}:9876/smarthome"
engine = create_engine(db_string)
engine.connect()

drop_database(engine.url)
print("### Database droped ###")
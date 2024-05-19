from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, Float, Time

from models.RiegoModel import RiegoConfig


class DataBase:
    def __init__(self) -> None:
        self.engine = create_engine(
            url="sqlite:///./Invernadero.db", connect_args={"check_same_thread": False}
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        self.meta = MetaData()

    def create_tables(self):
        self.temperatures_table = Table(
            "temps",
            self.meta,
            Column("temp", Float),
            Column("timestamp", Time, Column("sensor_id", Integer)),
        )

        self.irrigation_table = Table(
            "irrigation",
            self.meta,
            Column("time", String),
            Column("duration", Integer),
            Column("min_temp", Float),
            Column("max_temp", Float),
            Column("timestamp", Time),
        )

        self.meta.create_all(self.engine)

    def add_temperature_record(self, sensor_id: int, temp: float, timestamp: datetime):
        session = self.SessionLocal()

        try:
            temp_data = {
                "sensor_id": sensor_id,
                "temp": temp,
                "timestamp": timestamp,
            }
            session.execute(self.temperatures_table.insert().values(**temp_data))
            session.commit()

            return True
        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
            return False
        finally:
            session.close()

    def get_temperatures(self, sendor_id: int):
        pass

    def add_irrigation_set(self, data: RiegoConfig):
        session = self.SessionLocal()

        try:
            irrigation_data = {
                "time": data.time,
                "duration": data.duration,
                "min_temp": data.min_temp,
                "max_temp": data.max_temp,
                "timestamp": data.timestamp,
            }
            session.execute(self.irrigation_table.insert().values(**irrigation_data))
            session.commit()

            return True
        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
            return False
        finally:
            session.close()


db = DataBase()

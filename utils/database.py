# from datetime import datetime
import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, Float, Time

from models.RiegoModel import RiegoConfig


class DataBase:
    def __init__(self) -> None:
        self.engine = create_engine(
            url="sqlite:///./Invernadero.db",
            connect_args={"check_same_thread": False},
            echo=True,
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        self.meta = MetaData()

        self.create_tables()

    def create_tables(self):
        self.temperatures = Table(
            "temps",
            self.meta,
            Column("temp", Float),
            Column("timestamp", type_=Time, default=datetime.time, primary_key=True),
            Column("sensor_id", Integer, primary_key=True),
        )

        self.irrigation = Table(
            "irrigation",
            self.meta,
            Column("time", String),
            Column("duration", Integer),
            Column("min_temp", Float),
            Column("max_temp", Float),
            Column("timestamp", type_=Time, server_default=func.now()),
        )

        self.meta.create_all(self.engine)

    def add_temperature_record(self, sensor_id: int, temp: float):
        session = self.SessionLocal()

        try:
            temp_data = {
                "sensor_id": sensor_id,
                "temp": temp,
                # "timestamp": timestamp,
            }
            session.execute(self.temperatures.insert().values(**temp_data))
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

    def add_irrigation_set(
        self, time: str, duration: int, min_temp: float, max_temp: float
    ):
        session = self.SessionLocal()

        try:
            irrigation_data = {
                "time": time,
                "duration": duration,
                "min_temp": min_temp,
                "max_temp": max_temp,
                # "timestamp": datetime.time(),
            }
            session.execute(self.irrigation.insert().values(**irrigation_data))

            session.commit()

            return True
        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
            return False
        finally:
            session.close()


db = DataBase()

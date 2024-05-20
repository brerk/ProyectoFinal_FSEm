# from datetime import datetime
import datetime
from typing import List, Union
from sqlalchemy import create_engine, func, update, select

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, Float, Time, DateTime

from models.RiegoModel import RiegoConfig


class DataBase:
    def __init__(self) -> None:
        self.engine = create_engine(
            url="sqlite:///./Invernadero.db",
            connect_args={"check_same_thread": False},
            # echo=True,
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
            Column("sensor_id", Integer, primary_key=True),
            Column(
                "timestamp", type_=DateTime, server_default=func.now(), primary_key=True
            ),
        )

        self.irrigation = Table(
            "irrigation",
            self.meta,
            Column("time", String),
            Column("duration", Integer),
            Column("min_temp", Float),
            Column("max_temp", Float),
            Column("timestamp", type_=DateTime, server_default=func.now()),
        )

        self.config = Table(
            "config",
            self.meta,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("min_temp", Float),
            Column("max_temp", Float),
        )

        self.meta.create_all(self.engine)

    def add_temperature_record(self, sensor_id: int, temp: float):
        session = self.SessionLocal()

        try:
            temp_data = {
                "sensor_id": sensor_id,
                "temp": temp,
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

    def get_temperatures(self, sensor_id: int) -> Union[list, None]:
        session = self.SessionLocal()

        try:
            res = session.execute(
                self.temperatures.select().where(
                    self.temperatures.c.sensor_id == sensor_id
                )
            )

            return [task._asdict() for task in res]
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        finally:
            session.close()

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

    def get_irrigation_tasks(self) -> Union[List, None]:
        session = self.SessionLocal()

        try:
            res = session.execute(self.irrigation.select())

            return [RiegoConfig(**task._asdict()) for task in res]
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        finally:
            session.close()

    def set_temp_limits(self, min_temp, max_temp):
        session = self.SessionLocal()

        try:
            config_exists = session.execute(select(self.config)).fetchone()

            if config_exists:
                session.execute(
                    update(self.config)
                    .values(min_temp=min_temp, max_temp=max_temp)
                    .where(self.config.c.id == config_exists.id)
                )
            else:
                config_data = {
                    "min_temp": min_temp,
                    "max_temp": max_temp,
                }
                session.execute(self.config.insert().values(**config_data))

            session.commit()
            return True

        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
            return False

        finally:
            session.close()

    def get_temp_limits(self) -> list:
        session = self.SessionLocal()

        try:
            res = session.execute(self.config.select())

            return [r._asdict() for r in res]
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        finally:
            session.close()


db = DataBase()

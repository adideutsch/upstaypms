from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Reservations(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer)
    room_type = Column(String)
    arrival_date = Column(Date)
    departure_date = Column(Date)
    status = Column(Enum("Active", "Cancelled", name="statuses"))

    def __repr__(self):
        return f"<Reservation(id='{self.id}', " \
                            f"hotel_id='{self.hotel_id}', " \
                            f"room_type='{self.room_type}', " \
                            f"arrival_date='{self.arrival_date}', " \
                            f"departure_date='{self.departure_date}', " \
                            f"status='{self.status}')>"


class Hotels(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    hotel_name = Column(String)

    def __repr__(self):
        return f"<Hotel(id='{self.id}', " \
                      f"hotel_name='{self.hotel_name}')>"


class HotelInventory(Base):
    __tablename__ = 'hotel_inventory'
    hotel_id = Column(Integer, primary_key=True)
    room_type = Column(String, primary_key=True)
    room_inventory = Column(Integer)

    def __repr__(self):
        return f"<HotelInventory(hotel_id='{self.hotel_id}', " \
                               f"room_type='{self.room_type}', " \
                               f"room_inventory='{self.room_inventory}')>"


def create_tables(engine):
    Base.metadata.create_all(engine)

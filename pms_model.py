import datetime
import enum
from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.ext.declarative import declarative_base

from db_utils import get_db_session

Base = declarative_base()


class StatusEnum(enum.Enum):
    Active = "Active"
    Cancelled = "Cancelled"


class Reservations(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer)
    room_type = Column(String)
    arrival_date = Column(Date)
    departure_date = Column(Date)
    #status = Column(Enum("Active", "Cancelled", name="statuses"))
    status = Column(Enum(StatusEnum))

    def __repr__(self):
        return f"<Reservation(id='{self.id}', " \
                            f"hotel_id='{self.hotel_id}', " \
                            f"room_type='{self.room_type}', " \
                            f"arrival_date='{self.arrival_date}', " \
                            f"departure_date='{self.departure_date}', " \
                            f"status='{self.status}')>"


def create_datetime_object(date_string):
    return datetime.datetime.strptime(date_string, '%d-%m-%Y')


def add_reservation(hotel_id, room_type, arrival_date, departure_date, status):
    session = get_db_session()
    reservation = Reservations(hotel_id=hotel_id,
                               room_type=room_type,
                               arrival_date=create_datetime_object(arrival_date),
                               departure_date=create_datetime_object(departure_date),
                               status=status)
    session.add(reservation)
    session.commit()
    return reservation.id


def cancel_reservation(reservation_id):
    session = get_db_session()
    reservation = session.query(Reservations).get(reservation_id)
    reservation.status = "Cancelled"
    session.commit()


def activate_reservation(reservation_id):
    session = get_db_session()
    reservation = session.query(Reservations).get(reservation_id)
    reservation.status = "Active"
    session.commit()


class Hotels(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    hotel_name = Column(String)

    def __repr__(self):
        return f"<Hotel(id='{self.id}', " \
                      f"hotel_name='{self.hotel_name}')>"


def add_hotel(hotel_name):
    session = get_db_session()
    hotel = Hotels(hotel_name=hotel_name)
    session.add(hotel)
    session.commit()
    return hotel.id


class HotelInventory(Base):
    __tablename__ = 'hotel_inventory'
    hotel_id = Column(Integer, primary_key=True)
    room_type = Column(String, primary_key=True)
    room_inventory = Column(Integer)

    def __repr__(self):
        return f"<HotelInventory(hotel_id='{self.hotel_id}', " \
                               f"room_type='{self.room_type}', " \
                               f"room_inventory='{self.room_inventory}')>"


def add_inventory(hotel_id, room_type, room_inventory):
    session = get_db_session()
    inventory = HotelInventory(hotel_id=hotel_id,
                               room_type=room_type,
                               room_inventory=room_inventory)
    session.add(inventory)
    session.commit()


def create_tables(engine):
    Base.metadata.create_all(engine)

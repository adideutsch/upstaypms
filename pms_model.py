import datetime
from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.ext.declarative import declarative_base

from db_utils import DBSession

DATE_FORMAT = '%d-%m-%Y'
OPERATION_ERROR_RETURN_CODE = -1
ACTIVE_STATUS = "Active"
CANCELLED_STATUS = "Cancelled"
Base = declarative_base()


def create_datetime_object(date_string):
    """
    Convert a string-formatted date into a datetime object
    """
    return datetime.datetime.strptime(date_string, DATE_FORMAT).date()


def generate_days_list(start_date, end_date):
    """
    Create a list containing all the dates between start_date and end_date
    """
    return list(map(lambda day: start_date+datetime.timedelta(day), range((end_date-start_date).days)))


class Reservations(Base):
    """
    Reservation of a hotel room
    """
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer)
    room_type = Column(String)
    arrival_date = Column(Date)
    departure_date = Column(Date)
    status = Column(Enum(ACTIVE_STATUS, CANCELLED_STATUS, name="statuses"))

    def __repr__(self):
        return f"<Reservation(id='{self.id}', " \
                            f"hotel_id='{self.hotel_id}', " \
                            f"room_type='{self.room_type}', " \
                            f"arrival_date='{self.arrival_date}', " \
                            f"departure_date='{self.departure_date}', " \
                            f"status='{self.status}')>"


def get_occupancy(hotel_id, date, room_type):
    """
    For a given hotel and room type at a certain date, return the amount of reserved rooms
    """
    session = DBSession().get_db_session()
    return session.query(Reservations).filter(Reservations.arrival_date <= date)\
                                      .filter(Reservations.departure_date > date)\
                                      .filter(Reservations.hotel_id == hotel_id)\
                                      .filter(Reservations.room_type == room_type)\
                                      .filter(Reservations.status == ACTIVE_STATUS)\
                                      .count()


def add_reservation(hotel_id, room_type, arrival_date, departure_date, status):
    """
    Add a new reservation to the system
    """
    session = DBSession().get_db_session()
    # Check for invalid room type (doesn't exist in inventory for desired hotel)
    room_type_inventory = session.query(HotelInventory).filter(HotelInventory.hotel_id == hotel_id) \
                                                       .filter(HotelInventory.room_type == room_type)
    if len(room_type_inventory.all()) != 1:
        return OPERATION_ERROR_RETURN_CODE
    # Check for invalid reservation dates
    arrival_date = create_datetime_object(arrival_date)
    departure_date = create_datetime_object(departure_date)
    if departure_date <= arrival_date or arrival_date < datetime.date.today():
        return OPERATION_ERROR_RETURN_CODE
    # Check availability in inventory before adding reservation
    max_occupancy = room_type_inventory.first().room_inventory
    for date in generate_days_list(arrival_date, departure_date):
        if not get_occupancy(hotel_id, date, room_type) < max_occupancy:
            return OPERATION_ERROR_RETURN_CODE
    reservation = Reservations(hotel_id=hotel_id,
                               room_type=room_type,
                               arrival_date=arrival_date,
                               departure_date=departure_date,
                               status=status)
    session.add(reservation)
    session.commit()
    return reservation.id


def get_reservation(reservation_id):
    """
    Retrieve an existing reservation from the system
    """
    session = DBSession().get_db_session()
    reservation = session.query(Reservations).get(reservation_id)
    return {"reservation_id": reservation.id,
            "hotel_id": reservation.hotel_id,
            "room_type": reservation.room_type,
            "arrival_date": reservation.arrival_date.strftime(DATE_FORMAT),
            "departure_date": reservation.departure_date.strftime(DATE_FORMAT),
            "status": reservation.status}


def cancel_reservation(reservation_id):
    """
    Cancel an existing reservation. Note: this will only change the reservation's status to "Cancelled".
    """
    session = DBSession().get_db_session()
    reservation = session.query(Reservations).get(reservation_id)
    reservation.status = CANCELLED_STATUS
    session.commit()


def activate_reservation(reservation_id):
    """
    Activate an existing reservation. Note: this will only change the reservation's status to "Active".
    """
    session = DBSession().get_db_session()
    # If this functionality ever becomes an endpoint to 3rd parties, make sure to check
    # availability in inventory before activating reservation
    reservation = session.query(Reservations).get(reservation_id)
    reservation.status = ACTIVE_STATUS
    session.commit()


class Hotels(Base):
    """
    A Hotel facility
    """
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    hotel_name = Column(String)

    def __repr__(self):
        return f"<Hotel(id='{self.id}', " \
                      f"hotel_name='{self.hotel_name}')>"


def add_hotel(hotel_name):
    """
    Add a new hotel to the system
    """
    session = DBSession().get_db_session()
    hotel = Hotels(hotel_name=hotel_name)
    session.add(hotel)
    session.commit()
    return hotel.id


class HotelInventory(Base):
    """
    The inventory size of a specific room type at a specific hotel
    """
    __tablename__ = 'hotel_inventory'
    hotel_id = Column(Integer, primary_key=True)
    room_type = Column(String, primary_key=True)
    room_inventory = Column(Integer)

    def __repr__(self):
        return f"<HotelInventory(hotel_id='{self.hotel_id}', " \
                               f"room_type='{self.room_type}', " \
                               f"room_inventory='{self.room_inventory}')>"


def add_inventory(hotel_id, room_type, room_inventory):
    """
    Add an inventory record to the system
    """
    session = DBSession().get_db_session()
    # If this functionality ever becomes a real endpoint to 3rd parties, make sure to check
    # inventory for this room type, make sure it is new type
    inventory = HotelInventory(hotel_id=hotel_id,
                               room_type=room_type,
                               room_inventory=room_inventory)
    session.add(inventory)
    session.commit()


def get_hotel_roomtypes(hotel_id):
    """
    Get a given hotel's room types
    """
    session = DBSession().get_db_session()
    room_inventories = session.query(HotelInventory).filter(HotelInventory.hotel_id == hotel_id)
    return list(map(lambda room_inventory: room_inventory.room_type, room_inventories))


def get_inventory(hotel_id, room_type):
    """
    Get the general inventory size of a specific room type at a specific hotel
    Note: This doesn't take into account any existing reservations
    """
    session = DBSession().get_db_session()
    room_type_inventory = session.query(HotelInventory).filter(HotelInventory.hotel_id == hotel_id) \
                                                       .filter(HotelInventory.room_type == room_type).first()
    return room_type_inventory.room_inventory


def list_date_inventory(hotel_id, date):
    """
    Get the complete inventory of a specific date in a given hotel
    """
    room_types = get_hotel_roomtypes(hotel_id)
    date_inventory = {}
    for room_type in room_types:
        occupied = get_occupancy(hotel_id, date, room_type)
        inventory = get_inventory(hotel_id, room_type)
        available = inventory - occupied
        date_inventory[room_type] = {"available": available, "occupied": occupied}
    return date_inventory


def list_inventory(hotel_id, start_date, end_date):
    """
    Get the complete inventory of a specific date range in a given hotel
    """
    # Check for invalid dates
    start_date = create_datetime_object(start_date)
    end_date = create_datetime_object(end_date)
    if end_date < start_date:
        return OPERATION_ERROR_RETURN_CODE
    days_list = generate_days_list(start_date, end_date+datetime.timedelta(1))
    return {date: list_date_inventory(hotel_id, date) for date in days_list}


def create_tables(engine):
    """
    If any of the system tables does not exist, it will be created
    """
    Base.metadata.create_all(engine)

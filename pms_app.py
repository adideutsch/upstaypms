from sanic import Sanic
from sanic.response import json

from config import DB_SERVER, DB_NAME, DB_USER
from pms_model import Hotels, HotelInventory, Reservations
from db_utils import get_db_session

app = Sanic('pms_app')
app.config.DB_HOST = DB_SERVER
app.config.DB_NAME = DB_NAME
app.config.DB_USER = DB_USER

# EXAMPLE ENDPOINT 1
@app.route('/')
async def test(request):
    return json({'hello': 'world'})

# EXAMPLE ENDPOINT 2
@app.route("/query_string")
async def query_string(request):
    return json({"parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string})

@app.route("/add_reservation")
async def query_string(request):
    print(f"args: {request.args}")

    hotel_id = request.args["hotel_id"][0]
    room_type = request.args["room_type"][0]
    arrival_date = request.args["arrival_date"][0]
    departure_date = request.args["departure_date"][0]
    status = request.args["status"][0]

    print(f"parsed info: hid:{hotel_id}, rtype:{room_type}, a_date:{arrival_date}, d_date:{departure_date}, status:{status}")

    reservation = Reservations(hotel_id=hotel_id, room_type=room_type, arrival_date=arrival_date, departure_date=departure_date, status=status)
    session = get_db_session()
    session.add(reservation)
    session.commit()

    return json({"parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string, "inserted_id": reservation.id})


def add_hotel(session, hotel_name):
    hotel = Hotels(hotel_name=hotel_name)
    session.add(hotel)
    session.commit()
# session = get_db_session()
# add_hotel(session=session, hotel_name="Leonardo Plaza Ashdod")

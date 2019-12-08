from sanic import Sanic
from sanic.response import json

from config import DB_SERVER, DB_NAME, DB_USER
import pms_model as model

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


@app.route("/add_hotel")
async def add_hotel_endpoint(request):
    hotel_name = request.args["hotel_name"][0]
    hotel_id = model.add_hotel(hotel_name)
    return json({"hotel_id": hotel_id})


@app.route("/add_inventory")
async def add_inventory_endpoint(request):
    hotel_id = request.args["hotel_id"][0]
    room_type = request.args["room_type"][0]
    room_inventory = request.args["room_inventory"][0]
    model.add_inventory(hotel_id, room_type, room_inventory)
    return json({"success": True})


@app.route("/cancel_reservation")
async def cancel_reservation_endpoint(request):
    reservation_id = request.args["reservation_id"][0]
    model.cancel_reservation(reservation_id)
    return json({"success": True})


@app.route("/add_reservation")
async def add_reservation_endpoint(request):
    hotel_id = request.args["hotel_id"][0]
    room_type = request.args["room_type"][0]
    arrival_date = request.args["arrival_date"][0]
    departure_date = request.args["departure_date"][0]
    status = request.args["status"][0]

    reservation_id = model.add_reservation(hotel_id, room_type, arrival_date, departure_date, status)
    return json({"reservation_id": reservation_id})

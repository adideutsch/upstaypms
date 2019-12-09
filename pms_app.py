from sanic import Sanic
from sanic.response import json

from config import DB_SERVER, DB_NAME, DB_USER
import pms_model as model

app = Sanic('pms_app')
app.config.DB_HOST = DB_SERVER
app.config.DB_NAME = DB_NAME
app.config.DB_USER = DB_USER


@app.route("/add_hotel")
async def add_hotel_endpoint(request):
    """
    Add a new hotel to the system
    """
    hotel_name = request.args["hotel_name"][0]
    hotel_id = model.add_hotel(hotel_name)
    return json({"hotel_id": hotel_id})


@app.route("/add_inventory")
async def add_inventory_endpoint(request):
    """
    Add inventory to a given hotel
    """
    hotel_id = request.args["hotel_id"][0]
    room_type = request.args["room_type"][0]
    room_inventory = request.args["room_inventory"][0]
    model.add_inventory(hotel_id, room_type, room_inventory)
    return json({"success": True})


@app.route("/cancel_reservation")
async def cancel_reservation_endpoint(request):
    """
    Cancel an existing reservation
    """
    reservation_id = request.args["reservation_id"][0]
    model.cancel_reservation(reservation_id)
    return json({"success": True})


@app.route("/add_reservation")
async def add_reservation_endpoint(request):
    """
    Add a new reservation
    """
    hotel_id = request.args["hotel_id"][0]
    room_type = request.args["room_type"][0]
    arrival_date = request.args["arrival_date"][0]
    departure_date = request.args["departure_date"][0]
    status = request.args["status"][0]
    reservation_id = model.add_reservation(hotel_id, room_type, arrival_date, departure_date, status)
    if reservation_id == model.OPERATION_ERROR_RETURN_CODE:
        return json({"success": False})
    return json({"success": True, "reservation_id": reservation_id})


@app.route("/get_reservation")
async def get_reservation_endpoint(request):
    """
    Get an existing reservation
    """
    reservation_id = request.args["reservation_id"][0]
    reservation_dict = model.get_reservation(reservation_id)
    return json(reservation_dict)


@app.route("/list_inventory")
async def list_inventory_endpoint(request):
    """
    List the inventory of a hotel in a specific date range
    """
    hotel_id = request.args["hotel_id"][0]
    start_date = request.args["start_date"][0]
    end_date = request.args["end_date"][0]
    inventory = model.list_inventory(hotel_id, start_date, end_date)
    if inventory == model.OPERATION_ERROR_RETURN_CODE:
        return json({"success": False})
    return json({"success": True, "inventory": inventory})

from sanic import Sanic
from sanic.response import json

from config import DB_SERVER, DB_NAME, DB_USER

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
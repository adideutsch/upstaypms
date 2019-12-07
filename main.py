#WEB_SERVER = "35.223.102.169"
DB_SERVER = "35.223.245.72"

from sanic import Sanic
from sanic.response import json

app = Sanic('pms')
app.config.DB_HOST = DB_SERVER
app.config.DB_NAME = 'pmsdb'
app.config.DB_USER = 'upstayapp'

@app.route('/')
async def test(request):
    return json({'hello': 'world'})

@app.route("/query_string")
def query_string(request):
  return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
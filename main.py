#WEB_SERVER = "35.223.102.169"
DB_SERVER = "35.223.245.72"
DB_NAME = 'pmsdb'
DB_USER = 'upstayapp'
DB_PASSWORD = 'nyxhotel'
DB_PORT = '5432'

from sanic import Sanic
from sanic.response import json
import psycopg2
import sqlalchemy as db
from sqlalchemy import Column, Integer, String

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	fullname = Column(String)
	nickname = Column(String)
	def __repr__(self):
		return "<User(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)


app = Sanic('pms')
app.config.DB_HOST = DB_SERVER
app.config.DB_NAME = DB_NAME
app.config.DB_USER = DB_USER

@app.route('/')
async def test(request):
    return json({'hello': 'world'})

@app.route("/query_string")
async def query_string(request):
  return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })

if __name__ == '__main__':


	engine = db.create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}')
	# try:
	#     connect_str = f"dbname='{DB_NAME}' user='{DB_USER}' host='{DB_SERVER}' password='{DB_PASSWORD}'"
	#     # use our connection values to establish a connection
	#     conn = psycopg2.connect(connect_str)
	#     # create a psycopg2 cursor that can execute queries
	#     cursor = conn.cursor()
	#     # create a new table with a single column called "name"
	#     cursor.execute("""CREATE TABLE tutorials (name char(40));""")
	#     # run a SELECT statement - no data in there, but we can try it
	#     cursor.execute("""SELECT * from tutorials""")
	#     conn.commit() # <--- makes sure the change is shown in the database
	#     rows = cursor.fetchall()
	#     print(rows)
	#     cursor.close()
	#     conn.close()
	# except Exception as e:
	#     print("Uh oh, can't connect. Invalid dbname, user or password?")
	#     print(e)

    #app.run(host='0.0.0.0', port=80)
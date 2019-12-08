from db_utils import get_db_engine
from pms_model import create_tables
from pms_app import app

if __name__ == '__main__':
    create_tables(get_db_engine())
    app.run(host='0.0.0.0', port=80)

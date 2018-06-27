from models.orm import create_pool

from config import configs

from handle import app

if __name__ == '__main__':
	create_pool(user=configs.db.user, password=configs.db.password, db=configs.db.db)
	app.run(host=configs.web.host, port=configs.web.port)
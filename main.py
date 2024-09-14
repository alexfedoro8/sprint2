from sqlalchemy import create_engine



# Констринг для подключения к базе данных
DATABASE_URL = "postgresql+psycopg2://postgres:postgresql@localhost/sprint"

# Создание объекта Engine
engine = create_engine(DATABASE_URL, echo=True)

#подключаемся к базе
engine.connect()




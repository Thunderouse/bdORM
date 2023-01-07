
import sqlalchemy
from sqlalchemy.orm import sessionmaker

import json

from models import create_tables, drop_tables, Publisher, Book, Shop, Stock, Sale

def find(session, pub_name):
    # не используется за краткостью
    q = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name.like(f'%{pub_name}%'))
    return q

if __name__ == '__main__':
    # base_name = 'bookshopbd'
    # password = 'input your password'
    # dbms = "postgresql"
    # userdb = 'postgres'
    dbms = input('Введите имя СУБД:')
    base_name = input('Введите имя БД:')
    userdb = input('Введите логин:')
    password = input('Введите пароль:')

    DSN = f"{dbms}://{userdb}:{password}@localhost:5432/{base_name}"
    print(DSN)
    engine = sqlalchemy.create_engine(DSN)
    drop_tables(engine)
    create_tables(engine)

    # сессия
    Session = sessionmaker(bind=engine)
    session = Session()

    with open('tests_data.json') as f:
        data = json.load(f)
    tables = {'publisher': Publisher, 'book': Book, 'shop': Shop, 'stock': Stock, 'sale': Sale}
    for el in data:
        # 'model', 'pk', 'fields'
        table = tables[el['model']](id=el['pk'], **el['fields'])
        session.add(table)
    session.commit()

    while True:
        print('\nСписок издателей:')
        q = session.query(Publisher)
        for pub in q:
            print(pub.name)

        pub_name = input('\nВведите имя издателя:')
        q = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name.like(f'%{pub_name}%'))
        print(f'Список магазинов, где продаются книги издателя {pub_name}:')
        for _ in q:
            print(_.name)

        if input('\nНажмите q чтобы выйти или любую клавишу чтобы продолжить').lower() == 'q':
            break

session.close()


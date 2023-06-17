import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
def connect_db_postgres(login,password,name_db):
    dns = f'postgresql://{login}:{password}@localhost:5432/{name_db}'
    engine = sqlalchemy.create_engine(dns)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def create_tables(engine):
    Base.metadata.create_all(engine)

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=False)
    def __str__(self):
        return f'Publusher {self.name}'

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publish = relationship(Publisher, backref="publisher")

    def __str__(self):
        return f'Book {self.title}'

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=False)

    def __str__(self):
        return f'Shop {self.name}'

class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship(Book, backref="book")
    shop = relationship(Shop, backref="shop")

    def __str__(self):
        return f'Publusher {self.id_book},{self.id_shop}'

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref="stock")

    def __str__(self):
        return f'Sale {self.price}'

def find_publisher(conn, name):
    publ = conn.query(Publisher.id, Book.title, Shop.name, Sale.price, Sale.date_sale).filter(
        Publisher.name.like(f'%{name}%')).join(Book).join(Stock).join(Shop).join(Sale).all()
    return publ



if __name__ == '__main__':
    login = 'postgres'
    passw = 'postgres'
    name_db = 'netology_db'
    conn = connect_db_postgres(login, passw, name_db)
    f_p = input('Укажите фамилию автора: ')
    for it in find_publisher(conn, f_p):
        print(f'{it[1]} | {it[2]} | {it[3]} | {format(it[4],"%d-%m-%Y")}')

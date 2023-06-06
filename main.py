import psycopg2
from psycopg2.sql import SQL, Identifier

def create_db(conn):
    # создание таблиц
    with conn.cursor() as cur:
        cur.execute("""
           CREATE TABLE IF NOT EXISTS client(
               id SERIAL PRIMARY KEY,
               first_name VARCHAR(40) NOT NULL,
               last_name VARCHAR(40) NOT NULL,
               email VARCHAR(50) NOT NULL
           );
           """)
        cur.execute("""
           CREATE TABLE IF NOT EXISTS phone(
               id SERIAL PRIMARY KEY,
               phone_number TEXT NOT NULL,
               id_CLIENT INTEGER NOT NULL REFERENCES client(id)
           );
           """)
        conn.commit()  # фиксируем в БД


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO client(first_name, last_name, email) VALUES(%s,%s,%s) RETURNING id;
                """, (first_name, last_name, email))
        if phones != None:
            client_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO phone(phone_number, id_CLIENT) VALUES(%s,%s);
                """, (phones, client_id))
        conn.commit()


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                       INSERT INTO phone(phone_number, id_CLIENT) VALUES(%s,%s);
                    """, (phone, client_id))
        conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    phone = input("Укажите номер телефона для замены: ")
    with conn.cursor() as cur:
        arg_list = {'first_name': first_name, "last_name": last_name, 'email': email}
        for key, arg in arg_list.items():
            if arg:
                cur.execute(SQL("UPDATE client SET {}=%s WHERE id=%s").format(Identifier(key)),
                             (arg, client_id))
        if phones != None:
            cur.execute("""
                          UPDATE phone SET phone_number=%s WHERE id_client=%s and phone_number=%s;
                          """, (phones, client_id, phone))
        conn.commit()


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM phone WHERE id_client=%s and phone_number=%s;
                """, (client_id, phone))
        conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM phone WHERE id_client=%s;
                    """, (client_id,))

        cur.execute("""
                   DELETE FROM client WHERE id=%s;
                   """, (client_id,))
        conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        arg_list = {'first_name': first_name, "last_name": last_name, 'email': email, 'phone_number': phone}
        for key, arg in arg_list.items():
            if arg:
                cur.execute(SQL("select C.first_name || ' ' || C.last_name  as client from CLIENT C left join PHONE P on C.id = P.id_client WHERE {}=%s").format(Identifier(key)),
                            (arg,))
        client_list = ["".join(it) for it in cur.fetchall()]
    return f'Найдены клиенты: {", ".join(client_list)}'

with psycopg2.connect(database="clients_db", user="postgres", password="error911") as conn:
    # create_db(conn)
    #add_client(conn, 'Vova','Putinov','12323@mail.ru')
    #add_phone(conn, 16, '+79885533344')
    #change_client(conn, 16, phones='+79881111111')
    #delete_client(conn,16)
    #delete_phone(conn,22,'+79555555555')
    print(find_client(conn, first_name='Vova'))

conn.close()

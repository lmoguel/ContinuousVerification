import psycopg2
import sys
from flask import jsonify

class db_manager():
    """
    Execute db sentences and it's an intermediate between the services and db
    """
    user = ""
    password = ""
    host = ""
    port = ""
    database = ""

    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        #self.connect_db()

    def connect_db(self):
        try:
            connection = psycopg2.connect(user = self.user,
                                        password = self.password,
                                        host = self.host,
                                        port = self.port,
                                        database = self.database)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
            connection = None
        return connection
            
    def disconnect_db(self, connection):
        if(connection):
                connection.close()
                print("PostgreSQL connection is closed")


    def insert_building_block(self, id, name_b, address_b, port, description_text):
        connection = self.connect_db()
        result = 0
        if(connection):
            try:
                query_sentence = "INSERT INTO building_block(id, name_b, address_b, port, description_text) \
                                VALUES(%s, %s, %s, %s, %s) RETURNING id;"
                cur = connection.cursor()
                cur.execute(query_sentence, (id, name_b, address_b, port, description_text))
                result = cur.fetchone()[0]
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result
    
    def insert_company(self, id, name_c, email, password_c, address_c, port):
        connection = self.connect_db()
        result = 0
        if(connection):
            try:
                query_sentence = "INSERT INTO company(id, name_c, email, password_c, address_c, port)\
                                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
                cur = connection.cursor()
                cur.execute(query_sentence, (id, name_c, email, password_c, address_c, port))
                result = cur.fetchone()[0]
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def insert_contract_sc(self, id, type_sc, name_sc, address_sc, port, valid_contract, transaction_id, building_block_id):
        connection = self.connect_db()
        result = 0
        if(connection):
            try:
                query_sentence = "INSERT INTO contract_sc(id, type_sc, name_sc, address_sc, port, valid_contract,\
                                transaction_id, building_block_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) \
                                RETURNING id;"
                cur = connection.cursor()
                cur.execute(query_sentence, (id, type_sc, name_sc, address_sc, port, valid_contract,
                                            transaction_id, building_block_id))
                result = cur.fetchone()[0]
                #result = 1
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def insert_orders(self, id, status_o, transaction_id, content_id, logistic, file_name, iden):
        connection = self.connect_db()
        result = 0
        if(connection):
            try:
                query_sentence = "INSERT INTO orders(id, status_o, transaction_id, content_id, logistic, content_name, iden)\
                                VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;"
                cur = connection.cursor()
                cur.execute(query_sentence, (id, status_o, transaction_id, content_id, logistic, file_name, iden))
                result = cur.fetchone()[0]
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def insert_supply_chain(self, id, contract_id, catalog_in, catalog_out):
        connection = self.connect_db()
        result = 0
        if(connection):
            try:
                query_sentence = "INSERT INTO supply_chain(id, contract_id, catalog_in, catalog_out)\
                                VALUES(%s, %s, %s, %s) RETURNING id;"
                cur = connection.cursor()
                cur.execute(query_sentence, (id, contract_id, catalog_in, catalog_out))
                #result = cur.fetchone()[0]
                result = 1
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result   

    def get_bb_address_data(self, id):
        connection = self.connect_db()
        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT address_b, port FROM building_block where id=%s"
                cur.execute(query_sentence, (id,))
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result
    
    def get_organization_name(self, id):
        connection = self.connect_db()
        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT name_c, email FROM company where id=%s"
                cur.execute(query_sentence, (id,))
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def get_id_order(self, content_id, transaction_id):
        connection = self.connect_db()
        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT id FROM orders where content_id=%s and transaction_id=%s"
                cur.execute(query_sentence, (content_id,transaction_id,))
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [get_id_order]: Can't get the id order")
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def get_identification(self, content_id, transaction_id):
        connection = self.connect_db()
        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT iden FROM orders where content_id=%s and transaction_id=%s"
                cur.execute(query_sentence, (content_id, transaction_id,))
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [get_identification]: Can't get the identification")
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result


    def get_iden(self, content_id):
        connection = self.connect_db()
        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT iden FROM orders where status_o=%s"
                cur.execute(query_sentence, (content_id,))
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [get_id_order]: Can't get the id order")
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    
    def update_order_status(self, id, status_o):
        connection = self.connect_db()
        result = None
        if(connection):
            try:
                query_sentence = "UPDATE orders set status_o=%s where id=%s"
                cur = connection.cursor()
                cur.execute(query_sentence, (status_o, id))
                result = 1
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB update_order_status]: " + error)
            finally:
                cur.close()
                self.disconnect_db(connection)
            return result

    def get_transaction(self, id_order):
        connection = self.connect_db()

        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT transaction_id FROM orders where id=%s"
                cur.execute(query_sentence, (id_order,))
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB get_content_name]: " + str(error))
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    
    def get_content_id(self, id_order):
        connection = self.connect_db()

        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT content_id FROM orders where id=%s"
                cur.execute(query_sentence, (id_order,))
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB get_content_name]: " + str(error))
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result
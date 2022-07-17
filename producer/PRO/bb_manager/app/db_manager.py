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
            print(self.user)
            print(self.password)
            print(self.host)
            print(self.port)
            print(self.database)
            connection = None
        return connection
            
    def disconnect_db(self, connection):
        if(connection):
                connection.close()
                print("PostgreSQL connection is closed")

    def insert_building_block(self, id, name_b, address_b, port):
        connection = self.connect_db()
        result = None
        if(connection):
            try:
                query_sentence = "INSERT INTO building_block(id, name_b, address_b, port) \
                                VALUES(%s, %s, %s, %s) RETURNING id;"
                cur = connection.cursor()
                cur.execute(query_sentence, (id, name_b, address_b, port))
                result = cur.fetchone()[0]
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB insert_building_block]: " + str(error))
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def insert_stage(self, id, name_s, executable_sentence):
        connection = self.connect_db()
        result = None
        if(connection):
            try:
                query_sentence = "INSERT INTO stage(id, name_s, executable_sentence) VALUES(%s, %s, %s) RETURNING id;"
                cur = connection.cursor()
                cur.execute(query_sentence, (id, name_s, executable_sentence))
                result = cur.fetchone()[0]
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB insert_stage]: " + str(error))
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result
    
    def insert_value_chain(self, value_chain_id, contract_id, valid_contract, transaction_id):
        """
        Create a new value chain inside this building block
        """
        connection = self.connect_db()
        result = 0
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "INSERT INTO value_chain(id, contract_id, valid_contract, transaction_id) values (%s, %s, %s, %s) RETURNING id;"
                cur.execute(query_sentence, (value_chain_id, contract_id, valid_contract, transaction_id))
                result = cur.fetchone()[0]
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def insert_order(self, id, status_o, transaction_id, content_id, logistic, file_name, iden):
        """
        Create a new order inside the building block to control the content through all the stages inside
        this building block
        """
        connection = self.connect_db()
        result = 0
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "INSERT INTO orders(id, status_o, transaction_id, content_id, logistic, content_name, iden) \
                                VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;"
                cur.execute(query_sentence, (id, status_o, transaction_id, content_id, logistic, file_name, iden))
                result = cur.fetchone()[0]
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def insert_vc_stage(self, value_chain_id, stage_id, folder_in, folder_out):
        """
        Create a new relation between a value chain and one or more stages
        """
        connection = self.connect_db()
        result = 0
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "INSERT INTO vc_stage(value_chain_id, stage_id, folder_in, folder_out) \
                                VALUES (%s, %s, %s, %s) RETURNING value_chain_id"
                cur.execute(query_sentence, (value_chain_id, stage_id, folder_in, folder_out))
                #result = cur.fetchone()[0]
                connection.commit()
                result = 1
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB insert_vc_stage]" + str(error))
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result


    def get_stages(self):
        connection = self.connect_db()
        
        result = 0
        if(connection):
            try:
                cur = connection.cursor()
                cur.execute("SELECT * FROM stage")
                rows = cur.fetchall()
                result = rows
                #for row in rows:
                #    result.append([row[0], row[1], row[2]])
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close
                self.disconnect_db(connection)
        return result

    def get_building_block_id(self):
        connection = self.connect_db()

        result = None
        if(connection):
            try:
                cur = connection.cursor()
                cur.execute("SELECT id FROM building_block")
                result = cur.fetchone()[0]
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB get_building_block_id: " + str(error))
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def get_id_order(self, content_id):
        connection = self.connect_db()

        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT id FROM orders where content_id=%s"
                cur.execute(query_sentence, (content_id,))
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB get_id_order]: " + str(error))
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def transaction_authentication(self, transaction_id):
        """
        Authenticate the organization to use the building block processing
        """
        connection = self.connect_db()
        result = 0
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT * FROM value_chain where transaction_id=%s and valid_contract=%s"
                cur.execute(query_sentence, (transaction_id, 't'))
                result = cur.fetchone()[0]
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result
    

    def add_value_chain(self, id, contract_id, valid_contract, transaction_id, volume_in_path, volume_out_path):
        connection = self.connect_db()
        result = None
        if(connection):
            try:
                query_sentence = "INSERT INTO value_chain(id, contract_id, valid_contract, transaction_id, volume_in_path,\
                                volume_out_path) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;"
                cur = connection.cursor()
                print("CHECK 4: " + query_sentence)
                cur.execute(query_sentence, (id, contract_id, valid_contract, transaction_id, volume_in_path, volume_out_path))
                result = cur.fetchone()[0]
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB add_value_chain]: " + str(error))
            finally:
                cur.close()
                self.disconnect_db(connection)
        
        return result

    def insert_intra_order(self, id, id_order, stage_id, status, content_id, logistic, iden):
        connection = self.connect_db()
        result = None
        if(connection):
            try:
                query_sentence = "INSERT INTO intra_orders(id, id_orders, stage_id, status_o, content_id, logistic, iden) \
                                VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;"
                cur = connection.cursor()
                cur.execute(query_sentence, (id, id_order, stage_id, status, content_id, logistic, iden))
                updated_rows = cur.rowcount
                if(updated_rows!=0):
                    result = '1'
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB insert_intra_order]: " + str(error))
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

    def get_content_name(self, id):
        connection = self.connect_db()

        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT content_name FROM orders where id=%s"
                cur.execute(query_sentence, (id,))
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB get_content_name]: " + str(error))
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result

    def get_iden(self, id_order, transaction_id):
        connection = self.connect_db()

        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT iden FROM orders where id=%s and transaction_id=%s"
                cur.execute(query_sentence, (id_order, transaction_id,))
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB get_iden]: " + str(error))
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


    def get_building_name(self):
        connection = self.connect_db()

        result = None
        if(connection):
            try:
                cur = connection.cursor()
                query_sentence = "SELECT name_b FROM building_block"
                cur.execute(query_sentence)
                result = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR [DB get_content_name]: " + str(error))
            finally:
                cur.close()
                self.disconnect_db(connection)
        return result
    

    #def update_order_inside_bb(self, id):
    #    connection = self.connect_db()
    #    result = None
    #    if(connection):
    #        try:
    #            query_sentence = "UPDATE i"
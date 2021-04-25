from flask import Flask, request, jsonify
from configparser import ConfigParser
import mysql.connector
from mysql.connector import errorcode
import requests
import logging
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser()
config.read(f'{dir_path}/caseApi.cfg')
logging.basicConfig(filename=config['LOGGING']['log_file'], level=config['LOGGING']['log_level'])

app = Flask(__name__)

def connect():
    return mysql.connector.connect(
        user=config['DEFAULT']['mysql_user'],
        password=config['DEFAULT']['mysql_password'],
        host=config['DEFAULT']['mysql_host'],
        database=config['DEFAULT']['mysql_database'],
        auth_plugin='mysql_native_password')


@app.route('/select', methods=['GET'])
def selection():
    try:
        mysqldb = connect()
        cursor =  mysqldb.cursor(buffered=True)
        query = f"SELECT * FROM {config['DEFAULT']['mysql_database']}.{config['DEFAULT']['mysql_table']};"
        cursor.execute(query)
        response = cursor.fetchall()
        mysqldb.close()
    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return("AUTH ERROR! PLEASE CHECK LOG FILE.")
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return("DB NOT EXIST! PLEASE CHECK LOG FILE.")
    
        else:
            logging.error(str(e))
            print(e.errno)
            return("SOME ERROR OCCURED! PLEASE CHECK LOG FILE.")
    
    print(response)
    return jsonify(response)

@app.route('/insert', methods=['POST','PUT'])
def insertion():

    name = request.args.get("name")
    lastname = request.args.get("lastname")
    email = request.args.get("email")
    try:
        mysqldb = connect()
        cursor =  mysqldb.cursor(buffered=True)
        query = f"""INSERT INTO 
        {config['DEFAULT']['mysql_database']}.{config['DEFAULT']['mysql_table']} (name, lastname, email) VALUES
        ('{name}', '{lastname}', '{email}');"""
        cursor.execute(query)
        mysqldb.commit()
        mysqldb.close()
    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            print(e.errno)
            return("AUTH ERROR! PLEASE CHECK LOG FILE.")
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return("DB NOT EXIST! PLEASE CHECK LOG FILE.")
    
        else:
            logging.error(str(e))
            print(e.errno)
            return("SOME ERROR OCCURED! PLEASE CHECK LOG FILE.")

    print("Success")      
    return jsonify(Success=True)

@app.route('/delete', methods=['DELETE'])
def delete_():
    id = request.args.get("id")
    try:
        mysqldb = connect()
        cursor =  mysqldb.cursor(buffered=True)
        query = f""" DELETE FROM {config['DEFAULT']['mysql_database']}.{config['DEFAULT']['mysql_table']} WHERE ID = {id}; """
        cursor.execute(query)
        mysqldb.commit()
        mysqldb.close()
    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            logging.error(str(e))
            return("AUTH ERROR! PLEASE CHECK LOG FILE.")
            
        elif(e.errno == errorcode.ER_BAD_DB_ERROR):
            logging.error(str(e))
            return("DB NOT EXIST! PLEASE CHECK LOG FILE.")
    
        else:
            logging.error(str(e))
            return("SOME ERROR OCCURED! PLEASE CHECK LOG FILE.")
    
    print("Success")
    return jsonify(Success=True)
    

if __name__=="__main__":
    app.run(host=config['APISERVER']['api_host'], port=config['APISERVER']['api_port'])
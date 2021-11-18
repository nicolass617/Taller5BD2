from datetime import datetime

from neo4j import GraphDatabase, basic_auth

URL = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "1234"
DATABASE = "fourpaws"

driver = GraphDatabase.driver(URL, auth=basic_auth(USERNAME, PASSWORD))

db = driver.session(database=DATABASE)

db.close()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

class DBManager():
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        
    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            
    def createTable(self, tableName, tableSchema):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tableName} {tableSchema}''')
                            
    def insertRow(self, tableName, columns, data):
        if isinstance(data, list):
            self.cursor.executemany(f'''INSERT OR IGNORE INTO {tableName} {columns}''', data)
        else:
            self.cursor.execute(f'''INSERT OR IGNORE INTO {tableName} {columns}''', data)
        self.conn.commit()
        
    def dropTable(self, tableName):
        self.cursor.execute(f'''DROP TABLE IF EXISTS {tableName}''')
    
    def updateTable(self, tableName, newColumn):
        self.cursor.execute(f'''ALTER TABLE {tableName} ADD {newColumn}''')
        
    def deleteRow(self, tableName, condition):
        sql = f'''DELETE FROM {tableName} WHERE {condition}'''
        self.cursor.execute(sql)
        self.conn.commit()
        
    def search(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        
        query_result = [ dict(line) for line in [ zip([ column[0] for column in self.cursor.description ], row) for row in self.cursor.fetchall() ] ]
        return query_result
            
    def updateRow(self, tableName, newValue, condition):
        self.cursor.execute(f'''UPDATE {tableName} SET {newValue} WHERE {condition}''')
        self.conn.commit()

    

    
    
            
    
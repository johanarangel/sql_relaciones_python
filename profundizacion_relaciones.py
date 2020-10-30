#! usr/bin/ env python

'''
SQL Introducción [Python]
Ejemplos de clase
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para mostrar ejemplos prácticos de los visto durante la clase
'''

__author__ = "Johana Rangel"
__email__ = "johanarang@hotmail.com"
__version__ = "1.1"

import sqlite3
import csv

def create_schema():
     
    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()

    c.execute("""
                DROP TABLE IF EXISTS autor;
            """)

    c.execute("""
                DROP TABLE IF EXISTS libro;
            """)

    c.execute("""
            CREATE TABLE autor(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT
            );
            """)
    
    c.execute("""
            CREATE TABLE libro(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [title] TEXT NOT NULL,
                [pags] INTEGER NOT NULL,
                [fk_autor_id] INTEGER NOT NULL REFERENCES autor(id) 
            );
            """)

   
    conn.commit()
    conn.close()

def fill():

    with open('libreria_autor.csv', 'r') as archivo:
        data = list(csv.DictReader(archivo))
    
        autores = []
        for x in range(len(data)):    
            author = data[x]['autor']
            autores.append((x+1,author))
        
    conn = sqlite3.connect('libreria.db')
    conn.execute("PRAGMA foreign_keys= 1")
    c = conn.cursor()

    c.executemany("""
        INSERT INTO autor (id, author)
        VALUES(?,?);""", autores) 

    conn.commit()
    conn.close()

with open('libreria_libro.csv', 'r') as archivo:
    data = list(csv.DictReader(archivo))

    libros = []
    for x in range(len(data)):    
        titulo = data[x]['titulo']
        pags = int(data[x]['cantidad_paginas'])
        author = data[x]['autor']
        libros.append((x+1,titulo, pags, author))
    
    conn = sqlite3.connect('libreria.db')
    conn.execute("PRAGMA foreign_keys= 1")
    c = conn.cursor()

    c.executemany("""
        INSERT INTO libro (id, title, pags, fk_author_id)
        SELECT ?,?,?, a.id
        FROM autor as a
        WHERE a.id = fk_author_id;""", libros)

    conn.commit()
    conn.close()

if __name__ == "__main__":
  
  create_schema()
  #fill()

#   # Leer filas 
#   fetch()  # Ver todo el contenido de la DB
#   fetch(3)  # Ver la fila 3
#   fetch(20)  # Ver la fila 20

#   # Buscar autor
#   print(search_author('Relato de un naufrago'))
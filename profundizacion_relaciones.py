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


import csv
import sqlite3


def create_schema():
    
    conn = sqlite3.connect('biblioteca.db')
    c = conn.cursor()

    c.execute("""
                DROP TABLE IF EXISTS escritor;
            """)
    
    c.execute("""
                DROP TABLE IF EXISTS libro;
            """)


    c.execute("""
            CREATE TABLE escritor(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT NOT NULL
            );
            """)
    
    c.execute("""
            CREATE TABLE libro(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [title] TEXT NOT NULL,
                [pags] INTEGER NOT NULL,
                [fk_author_id] INTEGER NOT NULL REFERENCES escritor(id)
            );
            """)

    conn.commit()
    conn.close()

def insert_libros():
    pass

def fill():

    with open('libreria_autor.csv', 'r') as archivo:
        data = list(csv.DictReader(archivo))

        autores = []
        for x in range(len(data)):   
            autor = data[x]['autor']
            autores.append(autor)

    conn = sqlite3.connect('biblioteca.db')
    conn.execute("PRAGMA foreign_keys = 1") 
    c = conn.cursor()
    
    
    for x in autores:
        c.execute("""
            INSERT INTO escritor(name)
            VALUES(?);
            """, (x,))

    conn.commit()
    conn.close()


    with open('libreria_libro.csv', 'r') as archivo:
        data = list(csv.DictReader(archivo))
    
        libros = []
        for x in range(len(data)):    
            titulo = data[x]['titulo']
            pags = int(data[x]['cantidad_paginas'])
            author = data[x]['autor']
            libros.append((titulo, pags, author))
    
    
    conn = sqlite3.connect('biblioteca.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    try:
        for x in libros:
            c.execute("""
                INSERT INTO libro (title, pags, fk_author_id)
                SELECT ?,?, e.id
                FROM escritor as e
                WHERE e.name =?;""", x)
    
    except sqlite3.Error as err:
        print(err)

    conn.commit()
    conn.close()

def fetch(id):
    
    if id == 0:
        
        conn = sqlite3.connect('biblioteca.db')
        conn.execute("PRAGMA foreign_keys = 1")
        c = conn.cursor()
        
        c.execute("""SELECT * FROM libro;""")
        
        while True:
            row = c.fetchone()
            
            if row is None:
                break
            
            else:
                print(row)

        conn.commit()
        conn.close()

    elif id > 0:
        
        conn = sqlite3.connect('biblioteca.db')
        conn.execute("PRAGMA foreign_keys = 1")
        c = conn.cursor()

        for row in c.execute("""SELECT title, pags, fk_author_id as autor_id FROM libro WHERE id=?;""", (id,)):
            print('Fila:', id, 'resultado:', row)

        c.execute("""
                SELECT l.id, l.title, l.pags, e.name as name_autor
                FROM libro as l, escritor as e 
                WHERE l.fk_author_id = e.id;
                """)
        
        while True:
            row = c.fetchone()
            
            if row is None:
                print('No existe fila para el id', id, 'ingresado')
                break
            
            else:
                print(row)
          
        conn.commit()
        conn.close()  

def search_author(book_title):
    
    conn = sqlite3.connect('biblioteca.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    for row in c.execute("""SELECT e.name 
                            FROM libro as l, escritor as e
                            WHERE l.fk_author_id = e.id AND title=?;""", (book_title,)):
        return row
        
    
    conn.commit()
    conn.close()

def update(id, nuevo_autor):
    
    conn = sqlite3.connect('biblioteca.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    rowcount = c.execute("UPDATE escritor SET name = ? WHERE id =?",
                        (nuevo_autor, id)).rowcount

    print('Filas actualizadas:', rowcount)
        
    c.execute("""
        SELECT l.id, l.title, l.pags, e.name as autor_name
        FROM libro as l, escritor as e 
        WHERE l.fk_author_id = e.id AND e.id=?;""", (id,))

    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row)
        
    conn.commit()
    conn.close()

def delete(titulo):
    
    conn = sqlite3.connect('biblioteca.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    rowcount = c.execute("DELETE FROM libro WHERE title = ?", (titulo,)).rowcount            

    print('Filas actualizadas:', rowcount)
    
    for row in c.execute("""SELECT * FROM libro;"""):
        print(row)
        
    conn.commit()
    conn.close()


if __name__ == "__main__":
    #------CREAR TABLA--------
    create_schema()
    
    #---------LEER FILAS------
    fill()
    fetch(0) 
    fetch(3)  
    fetch(20) 

    # #---------BUSCAR AUTHOR POR TITLE-------- 
    print(search_author('Relato de un naufrago'))

    #---------ACTUALIZAR LA INFO-------- 
    id = 5
    nuevo_autor = 'Garrido'

    update(id, nuevo_autor)

    #---------BORRAR LIBRO POR TITLE-------- 
    delete('Cien anios de soledad')
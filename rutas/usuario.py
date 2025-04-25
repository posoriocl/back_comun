from fastapi import APIRouter
from  modelos.usuario import Usuario
from config import load_config
from connect import connect
from crypto import encriptar_variable
import psycopg2


ruta=APIRouter()

config = load_config ('app_config.ini', 'postgresql')
conn=connect(config)

@ruta.get('/login/{username}/{password}')
def login_usuario(username: str, password: str):
    try:
        with conn.cursor() as cur:     
                sql = 'SELECT * FROM usuario where username = ' + "'" + username + "'"
                cur.execute(sql)
                rows= (cur.fetchall())
                msg = "No existe usuario " + username
                if rows:
                      password_encriptada = encriptar_variable(password.encode('utf-8'))
                      password_encriptada = password_encriptada.decode('utf-8')
                      msg = "password incorrecta"
                      if password_encriptada == rows[0][2]:
                         msg = "Usuario OK"
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)    
    finally:
            return msg

@ruta.get('/usuario/{id}')
def usuario_una(id: int):
    try:
        with conn.cursor() as cur:     
                sql = 'SELECT * FROM usuario where id = ' + str(id)
                cur.execute(sql)
                rows= (cur.fetchall())
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)    
    finally:
            return rows



@ruta.get('/usuario')
def usuario_todas():
    try:
        with conn.cursor() as cur:     
                sql="SELECT * FROM usuario;"
                cur.execute(sql)
                rows=(cur.fetchall())
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)    
    finally:
            return rows


@ruta.post('/usuario')
def usuario_inserta(usuario: Usuario):
    id=None
    usuario.password = encriptar_variable(usuario.password.encode('utf-8'))
    usuario.password = usuario.password.decode('utf-8')
    print (usuario.password)
    try:
        with conn.cursor() as cur:     
                sql_fields="INSERT INTO usuario ( username, password, activo, email, fono) VALUES (%s,%s,%s,%s,%s) RETURNING id;" 
                sql_values= [ usuario.username, usuario.password, usuario.activo, usuario.email, usuario.fono]
                print (sql_fields, sql_values)
                cur.execute(sql_fields, (sql_values),)
                rows = cur.fetchone()
                if rows:
                    id = rows[0]
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return id        
    
    
@ruta.put('/usuario')
def usuario_modifica(id: int, usuario: Usuario):
    updated_row_count = 0
    try:
        with conn.cursor() as cur:     
                sql_fields="UPDATE usuario SET username=%s, password=%s, activo=%s, fono=%s, email=%s WHERE id = %s;" 
                sql_values= [ usuario.username, usuario.password, usuario.activo, usuario.fono, usuario.email, id]
                print (sql_fields, sql_values)
                cur.execute(sql_fields, (sql_values),)
                updated_row_count = cur.rowcount
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return updated_row_count
    
@ruta.delete('/usuario')
def usuario_borra(id: int):
    try:
        with conn.cursor() as cur:     
                sql="DELETE FROM usuario WHERE id = %s;" 
                print (sql, str(id))
                cur.execute(sql, (id,))
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)    
    finally:
            return "borrado"
    
import models.model as model

def get_login(usuario,password):
    query = f"SELECT * FROM usuario where usuario ='{usuario}' and password='{password}'"
    response = model.get(query)
    return response

def get_usuario(usuario):
    query = f"SELECT a.usuario,b.nombre,b.apellido,b.telefono,c.nombre 'nombre_rol' FROM usuario a,perfil b,rol c where a.id_perfil =b.id_perfil and a.id_rol=c.id_rol and a.usuario='{usuario}'"
    response = model.get(query)
    return response
def get_usuario_all(nombre_rol):
    query = f"SELECT a.id_usuario,a.usuario,b.nombre,b.apellido,b.telefono,c.nombre 'nombre_rol' FROM usuario a,perfil b,rol c where a.id_perfil =b.id_perfil and a.id_rol=c.id_rol and c.nombre <>'{nombre_rol}' and a.id_usuario NOT IN (SELECT id_usuario from categoria_producto)"
    response = model.get(query)
    return response
def get_usuario_categoria_productos(usuario):
    query = f"SELECT a.usuario,b.nombre,b.apellido,c.id_producto,c.nombre 'nombre_producto', d.nombre 'nombre_categoria' FROM usuario a,perfil b,producto c,categoria_producto d where a.id_perfil =b.id_perfil and a.id_usuario=d.id_usuario and d.id_categoria_producto=c.id_categoria_producto and a.usuario='{usuario}'"
    response = model.get(query)
    return response

def get_usuario_categoria_productos_all():
    query = f"SELECT a.usuario,b.nombre,b.apellido,c.id_producto,c.nombre 'nombre_producto', d.nombre 'nombre_categoria' FROM usuario a,perfil b,producto c,categoria_producto d where a.id_perfil =b.id_perfil and a.id_usuario=d.id_usuario and d.id_categoria_producto=c.id_categoria_producto"
    response = model.get(query)
    return response

def get_busqueda_producto (usuario,busqueda):
    query = f"SELECT a.usuario,b.nombre,b.apellido,c.id_producto,c.nombre 'nombre_producto', d.nombre 'nombre_categoria' FROM usuario a,perfil b,producto c,categoria_producto d where a.id_perfil =b.id_perfil and a.id_usuario=d.id_usuario and d.id_categoria_producto=c.id_categoria_producto and a.usuario='{usuario}' and c.nombre LIKE '%{busqueda}%'"
    response = model.get(query)
    return response

def get_busqueda_producto_all (busqueda):
    query = f"SELECT a.usuario,b.nombre,b.apellido,c.id_producto,c.nombre 'nombre_producto', d.nombre 'nombre_categoria' FROM usuario a,perfil b,producto c,categoria_producto d where a.id_perfil =b.id_perfil and a.id_usuario=d.id_usuario and d.id_categoria_producto=c.id_categoria_producto and c.nombre LIKE '%{busqueda}%'"
    response = model.get(query)
    return response

def get_categorias():
    query = f"SELECT id_categoria_producto,nombre FROM categoria_producto"
    response = model.get(query)
    return response

def update_producto (id_producto, nombre,id_categoria_producto):
    query=f"UPDATE producto SET nombre='{nombre}',id_categoria_producto={id_categoria_producto} WHERE id_producto={id_producto}"
    response=model.update_delete(query)
    return response

def delete_producto (id_producto):
    query = f"DELETE FROM producto WHERE id_producto={id_producto}"
    response = model.update_delete(query)
    return response

def create_producto (nombre,id_categoria_producto):
    query = f"INSERT INTO producto (nombre,id_categoria_producto) VALUES ('{nombre}',{id_categoria_producto})"
    response = model.insert(query)
    return response

def insert_perfil (nombre, apellido, direccion, telefono):
    query = f"INSERT INTO perfil (nombre, apellido, direccion, telefono) VALUES ('{nombre}', '{apellido}', '{direccion}', '{telefono}')"
    response = model.insert(query)
    return response

def insert_categoria (nombre, id_usuario):
    query = f"INSERT INTO categoria_producto (nombre, id_usuario) VALUES ('{nombre}', {id_usuario})"
    response = model.insert(query)
    return response

def register_usuario (username, password, nombre, apellido, direccion, telefono):
    id_perfil = insert_perfil(nombre, apellido, direccion, telefono)
    query = f"INSERT INTO usuario (usuario,password,id_perfil,id_rol) VALUES ('{username}','{password}',{id_perfil},2)"
    response = model.insert(query)
    return response
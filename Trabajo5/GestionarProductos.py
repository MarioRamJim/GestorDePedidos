import mongita
from mongita import MongitaClientDisk

cliente = MongitaClientDisk()
my_db = cliente.a_db
productos = my_db.productos

def EliminarProducto(producto):
    x = productos.delete_one(producto)

def añadirProducto(producto):
    x = productos.insert_one(producto)

if(__name__=="__main__"):
    for x in productos.find():
        EliminarProducto(x)
import mongita
from mongita import MongitaClientDisk

cliente = MongitaClientDisk()
my_db = cliente.a_db
pedidos = my_db.pedidos

def EliminarPedido(pedido):
    x = pedidos.delete_one(pedido)

def añadirPedido(pedido):
    x = pedidos.insert_one(pedido)

if(__name__=="__main__"):
    for x in pedidos.find():
        EliminarPedido(x)
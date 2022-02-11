# Guía de referencia
En esta guía se explicará el funcionamiento de la aplicación internamente y cuales son sus principales funciones y clases.</br></br>
## CLase Ui_MainWindow
En esta clase se define como será la ventana sobre la cual se desarrollará la aplicación (cuales son los componentes con los que contará la ventana principal, como se llamarán y se define su posición en pantalla), aunque no se le añade ninguna funcionalidad. </br></br>
## GestionarProductos.py y GestionarPedidos.py
Ambas clases son clases de mongita, las cuales son las clases que se encargan de la inserción y del borrado de objetos en la base de datos. GestionarProductos y GestionarPedidos cuentan con los métodos 
"EliminarProducto"/"InsertarProducto" y "EliminarPedido"/"InsertarPedido" respectivamente. Se tiene que tener en cuenta que los Productos deben seguir la siguiente estructura:<br></br>
`{"id":"","nombre":"","precio":""}`</br></br>
Y los pedidos, la siguiente:</br></br>
`{"id":"","idProducto":"","cantidad":"","dia":""}`</br></br>

## Clase MainWindow
Esta clase será la clase en la que se le da la funcionalidad a la aplicación. </br></br>
Al crearse un objeto de esta clase, el objeto carga la ventana definida en "Ui_MainWindow" y crea los wizards que serán usados en las diferentes funcionalidades de la aplicación, ademas de conectar los botones a las funciones que realizaran al pulsarse.</br>
A continuación se definirán los metodos mas importantes de esta clase:</br></br>

`def generarpdf(self):`--> Existen varios métodos como este en la clase, como `def wizardGenPDF(self):`,`def wizardInsertarPedido(self):` y `def wizardEliminarDia(self):`, entre otros y su función es enseñar el wizard pertinente en cada ocasión (se ejecutan al ser pulsado el botón que esta a su lado en la aplicación).</br></br>
`def FailureDialog(self):`--> Este método genera un diálogo de error génerico. Se llamará a este método por lo general cuando el usuario introduzca valores invalidos a los métodos de inserción/borrado.</br></br>
`def insertarProd(self):`--> Este método se ejecuta dentro del wizard de inserción de productos y se encarga de tomar los valores introducidos por el usuario, comprobar que sean validos y en caso de serlos, introducir en la base de datos un objeto con los valores introducidos. Analogamente a este método existen los métodos existen los métodos 
`def insertarPedido(self):`,`def eliminarPedido(self):`, `def eliminarProd(self):` y `def eliminarDia(self):` (Este último se encarga de eliminar todos los productos de la base de datos que tengan como paramentro "día" el valor introducido por el usuario).</br></br>
`def consultarInfo(self):`--> Este método obtiene los datos de la tabla seleccionada de la base de datos y introduce los valores recogidos en un listWidget.</br></br>
`def genPdf(self):`--> Este método se encarga de generar el PDF así como la gráfica que va incrustada en el.</br></br> 
`def generarpdf(self):`--> Este método se encuentra actualmente en desarrollo.

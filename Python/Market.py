import unittest
class ElProductoNoExiste(Exception):
    pass

class CompraFinalizada(Exception):
    pass

class CompraVacia(Exception):
    pass

class PagoInsuficiente(Exception):
    pass


class Producto (object):
    def __init__ (self,price,cod,name,desc):
        self.price = price
        self.cod = cod
        self.name = name 
        self.desc = desc

    def aplicar_descuento(self):
        if self.desc != 0:
            return (self.price * (1-(self.desc/100)))
        else:
            return self.price

    def shows_cod(self):
        return self.cod

class Caja (object):
    def __init__(self):
        self.lista_productos = []

    def add_To_List(self,producto):
        self.lista_productos.append(producto)

    def isEmpty(self):
        return (len(self.lista_productos) == 0) 

    def total_compra(self, pago):
        total = 0
        for i in range(len(self.lista_productos)):
            total += self.lista_productos[i].aplicar_descuento()
        if total > pago:
            raise PagoInsuficiente("El pago debe ser mayor al total de la compra.")
        return pago - total
    
    def buscador(self, buscado):
        productos_filtrados = list(filter(lambda p: p.shows_cod() == buscado, self.lista_productos))
        if not productos_filtrados:
            raise ElProductoNoExiste("El producto con cÃ³digo {} no existe".format(buscado))
        return True

    def finalizar_compra(self):
        if self.finished:
            raise CompraFinalizada("La compra ya se encuentra finalizada")
        if not self.lista_productos:
            raise CompraVacia("La compra no tenÃ­a productos")
        self.finished = True


class test_Producto(unittest.TestCase):
    def setUp(self):
        self.product = Producto(100,"# 000", "Objeto_1", 0)

    def test_descuento(self):
        self.product = Producto(90,"# 000", "Objeto_1", 0)
        self.assertEqual(90,self.product.aplicar_descuento())
    
    def test_no_aplica_descuento(self):
        self.product = Producto(100,"# 000", "Objeto_1", 0)
        self.assertEqual(100,self.product.aplicar_descuento())

    def test_mostrar_cod(self):
        self.product = Producto(100,"# 000", "Objeto_1", 0)
        self.assertEqual("# 000",self.product.shows_cod())
        pass

class test_Caja(unittest.TestCase):
    def setUp(self):
        self.caja = Caja()

    def test_caja_vacia(self):
        self.caja = Caja()
        self.assertEqual(True,self.caja.isEmpty())

    def test_caja_no_vacia(self):
        self.caja = Caja()
        self.caja.add_To_List(Producto(100,"# 000", "Objeto_1", 0))
        self.assertEqual(False,self.caja.isEmpty())
    
    def test_total_compra_da_vuelto(self):
        self.caja = Caja()
        self.caja.add_To_List(Producto(100,"# 000", "Objeto_1", 0))
        self.caja.add_To_List(Producto(50,"# 001", "Objeto_2", 10))
        self.assertEqual(55,self.caja.total_compra(200))

    def test_buscador(self):
        self.caja = Caja()
        self.caja.add_To_List(Producto(100,"# 000", "Objeto_1", 0))
        self.caja.add_To_List(Producto(50,"# 001", "Objeto_2", 10))
        self.assertEqual(True,self.caja.buscador("# 001"))

    def test_elemento_no_encontrado(self):
        self.caja = Caja()
        buscado = "# 003"
        self.caja.add_To_List(Producto(100,"# 000", "Objeto_1", 0))
        self.caja.add_To_List(Producto(50,"# 001", "Objeto_2", 10))
        self.assertRaises(ElProductoNoExiste,self.caja.buscador, buscado)


    def test_finalizar_compra(self):
        self.caja = Caja()
        self.caja.add_To_List(Producto(100,"# 000", "Objeto_1", 0))
        self.caja.add_To_List(Producto(50,"# 001", "Objeto_2", 10))

if __name__ == '__main__':
    unittest.main()
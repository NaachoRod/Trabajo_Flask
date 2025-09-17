from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .usuario import Usuario
from .cliente import Cliente
from .producto import Producto
from .factura import Factura
from .detalle_factura import DetalleFactura

__all__ = ["db", "Usuario", "Cliente", "Producto", "Factura", "DetalleFactura"]

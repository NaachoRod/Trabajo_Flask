from . import db

class Producto(db.Model):
    __tablename__ = "productos"
    id_producto = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    marca = db.Column(db.String(100))
    color = db.Column(db.String(80))
    base = db.Column(db.String(50))
    presentacion_litros = db.Column(db.Float, default=1.0)
    codigo_barra = db.Column(db.String(64))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    detalles = db.relationship("DetalleFactura", backref="producto", lazy=True)

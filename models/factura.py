from datetime import datetime
from . import db

class Factura(db.Model):
    __tablename__ = "facturas"
    id_factura = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False, default=0)

    detalles = db.relationship(
        "DetalleFactura",
        back_populates="factura",
        lazy=True,
        cascade="all, delete-orphan",
        single_parent=True,
    )

    cliente = db.relationship("Cliente", back_populates="facturas")

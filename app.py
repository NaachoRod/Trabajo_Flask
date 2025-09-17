from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from functools import wraps
from config import Config
from models import db, Usuario, Cliente, Producto, Factura, DetalleFactura

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_request
def proteger_todo():
    rutas_publicas = ("login", "register", "static")
    if request.endpoint not in rutas_publicas and not session.get("user_id"):
        flash("Tenés que iniciar sesión", "warning")
        return redirect(url_for("login"))


@app.before_request
def load_logged_in_user():
    uid = session.get("user_id")
    g.user = Usuario.query.get(uid) if uid else None

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
        print("Tablas creadas correctamente")

@app.get("/")
def index():
    if session.get("user_id"):
        return render_template("index.html", titulo="Inicio")
    return redirect(url_for("register"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        if not nombre or not email or not password:
            flash("Completá todos los campos", "danger")
            return redirect(url_for("register"))

        if Usuario.query.filter_by(email=email).first():
            flash("Ese email ya está registrado", "danger")
            return redirect(url_for("register"))

        user = Usuario(nombre=nombre, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Usuario creado. Ahora iniciá sesión.", "success")
        return redirect(url_for("login"))

    return render_template("auth/register.html", titulo="Registro")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = Usuario.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Email o contraseña incorrectos", "danger")
            return redirect(url_for("login"))

        session.clear()
        session["user_id"] = user.id_usuario
        flash(f"Bienvenido {user.nombre}", "success")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("auth/login.html", titulo="Login")

@app.get("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("login"))

@app.get("/clientes")
def clientes_listar():
    clientes = Cliente.query.order_by(Cliente.id_cliente.desc()).all()
    return render_template("clientes/listar.html", clientes=clientes, titulo="Clientes")

@app.route("/clientes/crear", methods=["GET","POST"])
def clientes_crear():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        if not nombre:
            flash("El nombre es obligatorio", "danger")
            return redirect(url_for("clientes_crear"))
        c = Cliente(
            nombre=nombre,
            direccion=request.form.get("direccion"),
            telefono=request.form.get("telefono"),
            email=request.form.get("email"),
        )
        db.session.add(c)
        db.session.commit()
        flash("Cliente creado", "success")
        return redirect(url_for("clientes_listar"))
    return render_template("clientes/crear.html", titulo="Nuevo Cliente")

@app.route("/clientes/<int:id>/editar", methods=["GET","POST"])
def clientes_editar(id):
    c = Cliente.query.get_or_404(id)
    if request.method == "POST":
        c.nombre = request.form.get("nombre")
        c.direccion = request.form.get("direccion")
        c.telefono = request.form.get("telefono")
        c.email = request.form.get("email")
        db.session.commit()
        flash("Cliente actualizado", "success")
        return redirect(url_for("clientes_listar"))
    return render_template("clientes/editar.html", cliente=c, titulo="Editar Cliente")

@app.post("/clientes/<int:id>/eliminar")
def clientes_eliminar(id):
    c = Cliente.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash("Cliente eliminado", "info")
    return redirect(url_for("clientes_listar"))

@app.get("/productos")
def productos_listar():
    productos = Producto.query.order_by(Producto.id_producto.desc()).all()
    return render_template("productos/listar.html", productos=productos, titulo="Productos")

@app.route("/productos/crear", methods=["GET","POST"])
def productos_crear():
    if request.method == "POST":
        desc = request.form.get("descripcion")
        precio = request.form.get("precio", type=float)
        if not desc or precio is None:
            flash("Descripción y precio son obligatorios", "danger")
            return redirect(url_for("productos_crear"))
        p = Producto(
            descripcion=desc,
            marca=request.form.get("marca"),
            color=request.form.get("color"),
            base=request.form.get("base"),
            presentacion_litros=request.form.get("presentacion_litros", type=float),
            codigo_barra=request.form.get("codigo_barra"),
            precio=precio,
            stock=request.form.get("stock", type=int) or 0
        )
        db.session.add(p)
        db.session.commit()
        flash("Producto creado", "success")
        return redirect(url_for("productos_listar"))
    return render_template("productos/crear.html", titulo="Nuevo Producto")

@app.route("/productos/<int:id>/editar", methods=["GET","POST"])
def productos_editar(id):
    p = Producto.query.get_or_404(id)
    if request.method == "POST":
        p.descripcion = request.form.get("descripcion")
        p.marca = request.form.get("marca")
        p.color = request.form.get("color")
        p.base = request.form.get("base")
        p.presentacion_litros = request.form.get("presentacion_litros", type=float)
        p.codigo_barra = request.form.get("codigo_barra")
        p.precio = request.form.get("precio", type=float)
        p.stock = request.form.get("stock", type=int) or 0
        db.session.commit()
        flash("Producto actualizado", "success")
        return redirect(url_for("productos_listar"))
    return render_template("productos/editar.html", producto=p, titulo="Editar Producto")

@app.post("/productos/<int:id>/eliminar")
def productos_eliminar(id):
    p = Producto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash("Producto eliminado", "info")
    return redirect(url_for("productos_listar"))

@app.get("/facturas")
def facturas_listar():
    facturas = Factura.query.order_by(Factura.id_factura.desc()).all()
    return render_template("facturas/listar.html", facturas=facturas, titulo="Facturas")

@app.route("/facturas/crear", methods=["GET","POST"])
def facturas_crear():
    if request.method == "POST":
        id_cliente = request.form.get("id_cliente", type=int)
        ids = request.form.getlist("id_producto")
        cants = request.form.getlist("cantidad")

        if not id_cliente or not ids:
            flash("Cliente y al menos un producto son obligatorios", "danger")
            return redirect(url_for("facturas_crear"))

        f = Factura(id_cliente=id_cliente, total=0)
        db.session.add(f)
        db.session.flush()

        total = 0
        for i, idp in enumerate(ids):
            if not idp:
                continue
            prod = Producto.query.get(int(idp))
            cant = int(cants[i] or 1)
            if not prod or cant <= 0:
                continue
            if prod.stock < cant:
                db.session.rollback()
                flash(f"Sin stock para {prod.descripcion}", "danger")
                return redirect(url_for("facturas_crear"))

            prod.stock -= cant
            det = DetalleFactura(
                id_factura=f.id_factura,
                id_producto=prod.id_producto,
                cantidad=cant,
                precio_unitario=prod.precio,
                subtotal=prod.precio * cant
            )
            db.session.add(det)
            total += det.subtotal

        f.total = total
        db.session.commit()
        flash("Factura emitida", "success")
        return redirect(url_for("facturas_listar"))

    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return render_template("facturas/crear.html", clientes=clientes, productos=productos, titulo="Nueva Factura")

if __name__ == "__main__":
    app.run(debug=True)

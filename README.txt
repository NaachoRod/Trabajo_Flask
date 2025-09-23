# Pinturería (TP_Flask)

1) Crear venv e instalar
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt

2) Crear DB
   CREATE DATABASE pintureria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

3) Configurar .env (Poner tus datos):
   SECRET_KEY=
   MYSQL_USER=
   MYSQL_PASSWORD=
   MYSQL_HOST=
   MYSQL_PORT=
   MYSQL_DB=

4) Inicializar tablas
   .\.venv\Scripts\python.exe -m flask --app app.py init-db

5) Correr
   .\.venv\Scripts\python.exe -m flask --app app.py run

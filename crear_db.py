import psycopg2

conexion = psycopg2.connect(
    host="localhost",
    user="soporte",
    password="soporte",
    dbname="bd_arte_en_papel",
    port="5432"
)

cursor=conexion.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, " \
"usuario VARCHAR(50) UNIQUE NOT NULL, " \
"correo VARCHAR(100) UNIQUE NOT NULL, contraseña VARCHAR(255) NOT NULL, " \
"fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

conexion.commit()
cursor.close()
conexion.close()

print("Base de datos creada exitosamente")
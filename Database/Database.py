
# Importa SQLite para crear y manejar la base de datos.
import sqlite3
# Importa herramientas para trabajar con rutas y carpetas.
import os

# Clase encargada de administrar la conexión y la creación de las tablas de la base de datos.
class Database:
  # Método estático: # se puede usar sin crear un objeto de la clase Database.
    @staticmethod
    # Obtiene la ruta donde se almacenará la base de datos.
    def get_db_path():
        base_dir = os.path.dirname(os.path.dirname(__file__))
        db_dir = os.path.join(base_dir, "Database")
        os.makedirs(db_dir, exist_ok=True)
        return os.path.join(db_dir, "autoseguro.db")
 # Crea una conexión con la base de datos.
    @staticmethod
    def conectar():
        conn = sqlite3.connect(Database.get_db_path())
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
# Crea todas las tablas del sistema si aún no existen. 
    @staticmethod
    def crear_tablas():
         # Obtiene la conexión con la base de datos.
        conn = Database.conectar()
        # Crea un cursor para ejecutar instrucciones SQL.
        cursor = conn.cursor()

# Tabla que almacena la información de los clientes.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            rut TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT NOT NULL,
            fecha_nacimiento TEXT NOT NULL
        )
        """)

      # Tabla que almacena los vehículos registrados.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehiculos (
            patente TEXT PRIMARY KEY,
            chasis TEXT,
            motor TEXT,
            marca TEXT,
            modelo TEXT,
            color TEXT,
            anio INTEGER,
            rut_cliente TEXT,
            FOREIGN KEY (rut_cliente)
                REFERENCES clientes(rut)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
        """)


     # Tabla que almacena la información de los agentes.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agentes (
           rut TEXT PRIMARY KEY,
           nombre TEXT NOT NULL,
           telefono TEXT NOT NULL
         )
          """)

     # Tabla que almacena las pólizas de los clientes.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS polizas (
            numero INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            monto_cobertura REAL NOT NULL DEFAULT 3000,
            estado TEXT NOT NULL,
            rut_cliente TEXT NOT NULL,
            patente TEXT UNIQUE,
            rut_conductor TEXT NOT NULL,
            relacion TEXT NOT NULL,
            rut_agente TEXT NOT NULL,
            nombre_conductor TEXT NOT NULL,
            fecha_nacimiento_conductor TEXT NOT NULL,
            FOREIGN KEY (rut_cliente)
                REFERENCES clientes(rut)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (patente)
                REFERENCES vehiculos(patente)
                ON DELETE CASCADE,
            FOREIGN KEY (rut_agente)
                REFERENCES agentes(rut)
        )
        """)

     # Tabla que almacena los siniestros registrados.
     
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS siniestros (
            numero INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT,
            fecha TEXT,
            fecha_reparacion TEXT,
            taller_direccion TEXT,
            monto_reparacion REAL,
            poliza_id INTEGER NOT NULL,
            rut_conductor TEXT,
            FOREIGN KEY (poliza_id)
                REFERENCES polizas(numero)
                ON DELETE CASCADE
        )
        """)



# Guarda los cambios en la base de datos.
        conn.commit()

 # Cierra la conexión con la base de datos.
        conn.close() 

        
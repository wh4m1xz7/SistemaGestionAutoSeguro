from termcolor import colored
import sys
import os
import re
from datetime import datetime
import time
from Database.Database import Database



# Clase con funciones de utilidad.
class Helpers:

   # se usa para limpiar la pantalla ya sea windows o linux
    @staticmethod
    def limpiar_pantalla():
        os.system("cls" if os.name == "nt" else "clear")

# se usa para el control de salida al presionar CTRL + C
    @staticmethod   
    def control_De_salida(sig, frame):
        print(colored("\n\n[!] Saliendo...\n", "red"))
        sys.exit(0)
# Muestra el mensaje de salida del sistema.
    @staticmethod
    def salida_sistema():
        Helpers.limpiar_pantalla()

        print("\nCerrando sistema...")
        time.sleep(1)

        print("Guardando datos...")
        time.sleep(1)

        print("Finalizando procesos...")
        time.sleep(1)

        Helpers.limpiar_pantalla()

        print("\n==================================================")
        print("   SISTEMA AUTO SEGURO S.A")
        print("   Sesión finalizada correctamente")
        print("   Gracias por usar el sistema 👋")
        print("==================================================")

        time.sleep(2)
        Helpers.limpiar_pantalla()

# Clase con funciones para gestionar los clientes.

class Functions_Clients:    

  # Validacione del rut
    @staticmethod
    def validar_rut(rut: str) -> bool:
        pattern = r"^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$"
        return bool(re.match(pattern, rut))

    @staticmethod
    def validar_fecha(fecha: str) -> bool:
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            return True
        except ValueError:
            return False

   # Registra un cliente.
    @staticmethod
    def registrar_cliente():
        print(colored("\n=== REGISTRAR CLIENTE ===", "green"))

        conn = Database.conectar()
        cursor = conn.cursor()

        rut = input("RUT: ").strip()

        if not Functions_Clients.validar_rut(rut):
            print(colored("RUT inválido", "red"))
            input()
            return

        cursor.execute("SELECT rut FROM clientes WHERE rut = ?", (rut,))
        if cursor.fetchone():
            print(colored("Cliente ya existe", "yellow"))
            input()
            return

        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        telefono = input("Teléfono: ").strip()
        direccion = input("Dirección: ").strip()
        fecha = input("Fecha nacimiento (DD/MM/AAAA): ").strip()

        if not Functions_Clients.validar_fecha(fecha):
            print(colored("Fecha inválida", "red"))
            input()
            return

        cursor.execute("""
            INSERT INTO clientes (rut, nombre, apellido, telefono, direccion, fecha_nacimiento)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (rut, nombre, apellido, telefono, direccion, fecha))

        conn.commit()
        conn.close()

        print(colored("Cliente registrado ✔", "green"))
        input()

  # Consulta un cliente por su RUT.
    @staticmethod
    def consultar_cliente():
        print(colored("\n=== CONSULTAR CLIENTE ===", "green"))

        conn = Database.conectar()
        cursor = conn.cursor()

        rut = input("RUT: ").strip()

        cursor.execute("SELECT * FROM clientes WHERE rut = ?", (rut,))
        c = cursor.fetchone()

        conn.close()

        if not c:
            print(colored("Cliente no encontrado", "yellow"))
            input()
            return

        print(colored("\n=== DATOS CLIENTE ===", "cyan"))
        print(f"RUT: {c[0]}")
        print(f"Nombre: {c[1]}")
        print(f"Apellido: {c[2]}")
        print(f"Teléfono: {c[3]}")
        print(f"Dirección: {c[4]}")
        print(f"Fecha nacimiento: {c[5]}")

        input()

   # listar  a los clientes
    @staticmethod
    def listar_cliente():
        Helpers.limpiar_pantalla()
        print(colored("\n=== CONSULTAR CLIENTE ===", "green", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        rut = input("RUT: ").strip()

        cursor.execute("SELECT * FROM clientes WHERE rut = ?", (rut,))
        c = cursor.fetchone()

        if not c:
            print(colored("Cliente no encontrado", "yellow"))
            conn.close()
            input("\nENTER para volver...")
            return

        print(colored("\n=== DATOS CLIENTE ===", "cyan"))
        print(f"RUT: {c[0]}")
        print(f"Nombre: {c[1]} {c[2]}")
        print(f"Teléfono: {c[3]}")
        print(f"Dirección: {c[4]}")
        print(f"Fecha nacimiento: {c[5]}")

        cursor.execute("""
            SELECT patente, chasis, motor, marca, modelo, color, anio
            FROM vehiculos
            WHERE rut_cliente = ?
        """, (rut,))
        vehiculos = cursor.fetchall()

        print(colored("\n=== VEHÍCULOS ===", "yellow"))
        if vehiculos:
            for v in vehiculos:
                print(f"Patente: {v[0]}")
                print(f"Chasis: {v[1]}")
                print(f"Motor: {v[2]}")
                print(f"Marca: {v[3]}")
                print(f"Modelo: {v[4]}")
                print(f"Color: {v[5]}")
                print(f"Año: {v[6]}")
                print("-" * 35)
        else:
            print("Sin vehículos")

        cursor.execute("""
            SELECT numero, tipo, estado, patente, rut_conductor, relacion, rut_agente
            FROM polizas
            WHERE rut_cliente = ?
        """, (rut,))
        polizas = cursor.fetchall()

        print(colored("\n=== PÓLIZAS ===", "magenta"))
        if polizas:
            for p in polizas:
                print(f"Número: {p[0]}")
                print(f"Tipo: {p[1]}")
                print(f"Estado: {p[2]}")
                print(f"Patente: {p[3] if p[3] else 'No aplica'}")
                print(f"RUT Conductor: {p[4]}")
                print(f"Relación: {p[5]}")
                print(f"RUT Agente: {p[6]}")
                print("-" * 35)
        else:
            print("Sin pólizas")

        cursor.execute("""
            SELECT s.numero, s.descripcion, s.fecha, s.fecha_reparacion,
                   s.taller_direccion, s.monto_reparacion, s.poliza_id, s.rut_conductor
            FROM siniestros s
            JOIN polizas p ON s.poliza_id = p.numero
            WHERE p.rut_cliente = ?
        """, (rut,))
        siniestros = cursor.fetchall()

        print(colored("\n=== SINIESTROS ===", "red"))
        if siniestros:
            for s in siniestros:
                print(f"Número: {s[0]}")
                print(f"Descripción: {s[1]}")
                print(f"Fecha siniestro: {s[2]}")
                print(f"Fecha reparación: {s[3]}")
                print(f"Taller: {s[4]}")
                print(f"Monto reparación: ${s[5]:,.0f}")
                print(f"Póliza ID: {s[6]}")
                print(f"RUT Conductor: {s[7]}")
                print("-" * 35)
        else:
            print("Sin siniestros")

        conn.close()
        input("\nENTER para volver...")

# Clase con funciones para gestionar los vehículos.

class Functions_Cars:

    @staticmethod
    def registrar_vehiculo():
        Helpers.limpiar_pantalla()
        print(colored("\n=== REGISTRAR VEHÍCULO ===", "yellow"))

        conn = Database.conectar()
        cursor = conn.cursor()

        rut = input("RUT cliente: ").strip()

        if not Functions_Clients.validar_rut(rut):
            print("RUT inválido")
            input()
            return

        cursor.execute("SELECT rut FROM clientes WHERE rut = ?", (rut,))
        if not cursor.fetchone():
            print("Cliente no existe")
            input()
            return

        patente = input("Patente: ").strip().upper()

        cursor.execute("SELECT patente FROM vehiculos WHERE patente = ?", (patente,))
        if cursor.fetchone():
            print("Vehículo ya existe")
            input()
            return

        chasis = input("Chasis: ")
        motor = input("Motor: ")
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        color = input("Color: ")
        anio = input("Año: ")

        cursor.execute("""
            INSERT INTO vehiculos
            (patente, chasis, motor, marca, modelo, color, anio, rut_cliente)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (patente, chasis, motor, marca, modelo, color, anio, rut))

        conn.commit()
        conn.close()

        print(colored("Vehículo registrado ✔", "green"))
        input()

  # Consulta la información de un vehículo.

    @staticmethod
    def consultar_vehiculo():
        Helpers.limpiar_pantalla()
        print(colored("\n=== CONSULTAR VEHÍCULO ===", "yellow", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        patente = input("Patente: ").strip().upper().replace(" ", "")

        cursor.execute(
            "SELECT patente, chasis, motor, marca, modelo, color, anio, rut_cliente "
            "FROM vehiculos WHERE UPPER(REPLACE(patente,' ','')) = ?",
            (patente,)
        )

        v = cursor.fetchone()

        conn.close()

        if v is None:
            print(colored("Vehículo no encontrado", "red"))
            input("\nENTER para volver...")
            return

        print(colored(f"\nPatente: {v[0]}", "cyan"))
        print(f"Chasis: {v[1]}")
        print(f"Motor: {v[2]}")
        print(f"Marca: {v[3]}")
        print(f"Modelo: {v[4]}")
        print(f"Color: {v[5]}")
        print(f"Año: {v[6]}")
        print(f"RUT cliente: {v[7]}")

        input("\nENTER para volver...")

 # Lista los vehículos registrados.
    @staticmethod
    def listar_vehiculos():
        Helpers.limpiar_pantalla()
        print(colored("\n=== LISTA DE VEHÍCULOS ===", "yellow", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM vehiculos")
        vehiculos = cursor.fetchall()

        conn.close()

        if not vehiculos:
            print(colored("No hay vehículos registrados", "red"))
            input("\nENTER para volver...")
            return

        for v in vehiculos:
            print(colored("\n" + "=" * 40, "cyan"))
            print(colored(f"Patente: {v[0]}", "cyan"))
            print(f"Chasis: {v[1]}")
            print(f"Motor: {v[2]}")
            print(f"Marca: {v[3]}")
            print(f"Modelo: {v[4]}")
            print(f"Color: {v[5]}")
            print(f"Año: {v[6]}")
            print(f"RUT cliente: {v[7]}")

        print(colored("\n" + "=" * 40, "cyan"))
        input("\nENTER para volver...")

# Clase con funciones para administrar las pólizas

class Functions_Polizas:

    @staticmethod
    def registrar_poliza():
        Helpers.limpiar_pantalla()
        print(colored("\n=== REGISTRAR PÓLIZA ===", "blue", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        rut_cliente = input("RUT cliente: ").strip()

        if not Functions_Clients.validar_rut(rut_cliente):
            print(colored("RUT inválido", "red"))
            conn.close()
            input()
            return

        cursor.execute("SELECT rut FROM clientes WHERE rut = ?", (rut_cliente,))
        if not cursor.fetchone():
            print(colored("Cliente no existe", "red"))
            conn.close()
            input()
            return

        print("\nTipo de póliza:")
        print("[1] Automotriz")
        print("[2] Vida")

        op = input("Opción: ").strip()

        if op == "1":
            tipo = "Automotriz"
        elif op == "2":
            tipo = "Vida"
        else:
            print(colored("Tipo inválido", "red"))
            conn.close()
            input()
            return

        patente = None

        if tipo == "Automotriz":
            patente = input("Patente vehículo: ").strip().upper()

            cursor.execute("SELECT patente FROM vehiculos WHERE patente = ?", (patente,))
            if not cursor.fetchone():
                print(colored("Vehículo no existe", "red"))
                conn.close()
                input()
                return

            cursor.execute("SELECT patente FROM polizas WHERE patente = ?", (patente,))
            if cursor.fetchone():
                print(colored("Este vehículo ya tiene póliza", "red"))
                conn.close()
                input()
                return

        estado = input("Estado (Alta / Baja / Suspensión): ").strip()
        rut_conductor = input("RUT conductor: ").strip()
        nombre_conductor = input("Nombre conductor: ").strip()
        fecha_nacimiento_conductor = input("Fecha nacimiento conductor (DD/MM/AAAA): ").strip()
        relacion = input("Relación con cliente: ").strip()
        rut_agente = input("RUT agente de ventas: ").strip()

        cursor.execute("SELECT rut FROM agentes WHERE rut = ?", (rut_agente,))
        if cursor.fetchone() is None:
            print(colored("Agente no registrado", "red"))
            conn.close()
            input("\nENTER para volver...")
            return

        cursor.execute("""
            INSERT INTO polizas (
                tipo, estado, rut_cliente, patente,
                rut_conductor, nombre_conductor,
                fecha_nacimiento_conductor, relacion, rut_agente
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tipo, estado, rut_cliente, patente,
            rut_conductor, nombre_conductor,
            fecha_nacimiento_conductor, relacion, rut_agente
        ))

        conn.commit()
        conn.close()

        print(colored("\n✔ Póliza registrada correctamente", "green"))
        input("\nENTER para volver...")

    @staticmethod
    def consultar_poliza():
        Helpers.limpiar_pantalla()
        print(colored("\n=== CONSULTAR PÓLIZA ===", "magenta", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        numero = input("Número de póliza: ").strip()

        if not numero.isdigit():
            print(colored("Número inválido", "red"))
            conn.close()
            input("\nENTER para volver...")
            return

        cursor.execute("""
            SELECT numero, tipo, estado, rut_cliente, patente,
                   rut_conductor, nombre_conductor,
                   fecha_nacimiento_conductor, relacion, rut_agente
            FROM polizas
            WHERE numero = ?
        """, (numero,))

        p = cursor.fetchone()
        conn.close()

        if p is None:
            print(colored("Póliza no encontrada", "red"))
            input("\nENTER para volver...")
            return

        print(colored("\n=== DETALLE DE PÓLIZA ===", "cyan"))
        print(f"Número: {p[0]}")
        print(f"Tipo: {p[1]}")
        print(f"Estado: {p[2]}")
        print(f"RUT Cliente: {p[3]}")
        print(f"Patente: {p[4] if p[4] else 'No aplica'}")
        print(f"RUT Conductor: {p[5]}")
        print(f"Nombre Conductor: {p[6]}")
        print(f"Fecha nacimiento conductor: {p[7]}")
        print(f"Relación: {p[8]}")
        print(f"RUT Agente: {p[9]}")

        input("\nENTER para volver...")

    @staticmethod
    def listar_polizas():
        Helpers.limpiar_pantalla()
        print(colored("\n=== LISTA DE PÓLIZAS ===", "magenta", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT numero, tipo, estado, rut_cliente, patente,
                   rut_conductor, nombre_conductor,
                   fecha_nacimiento_conductor, relacion, rut_agente
            FROM polizas
        """)

        polizas = cursor.fetchall()
        conn.close()

        if not polizas:
            print(colored("No hay pólizas registradas.", "red"))
            input("\nENTER para volver...")
            return

        for p in polizas:
            print(colored("=" * 45, "cyan"))
            print(f"Número de póliza : {p[0]}")
            print(f"Tipo             : {p[1]}")
            print(f"Estado           : {p[2]}")
            print(f"RUT Cliente      : {p[3]}")
            print(f"Patente          : {p[4] if p[4] else 'No aplica'}")
            print(f"RUT Conductor    : {p[5]}")
            print(f"Nombre Conductor : {p[6]}")
            print(f"Fecha Nacimiento : {p[7]}")
            print(f"Relación         : {p[8]}")
            print(f"RUT Agente       : {p[9]}")

        print(colored("=" * 45, "cyan"))
        input("\nENTER para volver...")

    @staticmethod
    def total_polizas():
        Helpers.limpiar_pantalla()
        print(colored("\n=== TOTAL PÓLIZAS VENDIDAS ===", "cyan", attrs=["bold"]))

        VALOR_UF = 39000

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM polizas WHERE tipo='Automotriz'")
        auto = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM polizas WHERE tipo='Vida'")
        vida = cursor.fetchone()[0]

        total_auto = auto * 100 * VALOR_UF
        total_vida = vida * 30 * VALOR_UF

        print(f"\nAutomotriz: {auto} póliza(s)")
        print(f"Total: ${total_auto:,}")

        print(f"\nVida: {vida} póliza(s)")
        print(f"Total: ${total_vida:,}")

        print("\n----------------------------")
        print(f"TOTAL GENERAL: ${total_auto + total_vida:,}")

        conn.close()
        input("\nENTER para volver...")

# Clase con funciones para registrar y consultar siniestros
class Functions_Siniestros: 

    @staticmethod
    def registrar_siniestro():
        Helpers.limpiar_pantalla()
        print(colored("\n=== REGISTRAR SINIESTRO ===", "red", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        try:
            poliza_id = int(input("Número de póliza: "))
        except ValueError:
            print("Número inválido")
            input()
            return

        cursor.execute("SELECT numero FROM polizas WHERE numero = ?", (poliza_id,))
        if cursor.fetchone() is None:
            print(colored("Póliza no existe", "red"))
            input()
            return

        descripcion = input("Descripción del siniestro: ")
        fecha = input("Fecha del siniestro (YYYY-MM-DD): ")
        fecha_reparacion = input("Fecha de reparación (YYYY-MM-DD): ")
        taller = input("Dirección del taller: ")

        try:
            monto = float(input("Monto reparación: "))
        except ValueError:
            print("Monto inválido")
            input()
            return

        rut_conductor = input("RUT conductor: ").strip()

        cursor.execute("""
            INSERT INTO siniestros
            (
                descripcion,
                fecha,
                fecha_reparacion,
                taller_direccion,
                monto_reparacion,
                poliza_id,
                rut_conductor
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            descripcion,
            fecha,
            fecha_reparacion,
            taller,
            monto,
            poliza_id,
            rut_conductor
        ))

        conn.commit()
        conn.close()

        print(colored("Siniestro registrado ✔", "green"))
        input()

    @staticmethod
    def consultar_siniestro():
        Helpers.limpiar_pantalla()
        print(colored("\n=== CONSULTAR SINIESTRO ===", "red", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        try:
            numero = int(input("Número de siniestro: "))
        except ValueError:
            print(colored("Número inválido", "red"))
            input("\nENTER para volver...")
            return

        cursor.execute("""
            SELECT numero, descripcion, fecha, fecha_reparacion,
                   taller_direccion, monto_reparacion, poliza_id, rut_conductor
            FROM siniestros
            WHERE numero = ?
        """, (numero,))

        s = cursor.fetchone()
        conn.close()

        if s is None:
            print(colored("Siniestro no encontrado", "red"))
            input("\nENTER para volver...")
            return

        print(colored("\n=== DETALLE SINIESTRO ===", "cyan", attrs=["bold"]))
        print(colored(f"Número: {s[0]}", "cyan"))
        print(f"Descripción: {s[1]}")
        print(f"Fecha siniestro: {s[2]}")
        print(f"Fecha reparación: {s[3]}")
        print(f"Taller: {s[4]}")
        print(f"Monto reparación: ${s[5]:,.0f}")
        print(f"Póliza ID: {s[6]}")
        print(f"RUT Conductor: {s[7]}")

        input("\nENTER para volver...")

    @staticmethod
    def listar_siniestros():
        Helpers.limpiar_pantalla()
        print(colored("\n=== LISTA DE SINIESTROS ===", "red", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT numero, descripcion, fecha, fecha_reparacion, monto_reparacion, poliza_id, rut_conductor
            FROM siniestros
        """)

        siniestros = cursor.fetchall()
        conn.close()

      # Valida que el campo no esté vacío.
        if not siniestros:
            print(colored("No hay siniestros registrados", "red"))
            input("\nENTER para volver...")
            return

       # Muestra la lista de registros.
        for s in siniestros:
            print(colored("\n-----------------------------", "yellow"))
            print(colored(f"Número: {s[0]}", "cyan"))
            print(f"Descripción: {s[1]}")
            print(f"Fecha: {s[2]}")
            print(f"Fecha reparación: {s[3]}")
            print(f"Monto reparación: ${s[4]:,.0f}")
            print(f"Póliza ID: {s[5]}")
            print(f"RUT Conductor: {s[6]}")

        input("\nENTER para volver...")

# Clase con funciones para generar reportes
class Functions_reportes:
    @staticmethod
    def reporte_polizas_por_tipo():
        Helpers.limpiar_pantalla()
        print(colored("\n=== TOTAL PÓLIZAS POR TIPO ===", "cyan", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tipo, COUNT(*)
            FROM polizas
            GROUP BY tipo
        """)

        datos = cursor.fetchall()
        conn.close()

        if not datos:
            print(colored("No hay pólizas registradas", "red"))
            input()
            return

        total_general = 0

        for tipo, cantidad in datos:
            print(colored(f"{tipo}: {cantidad} pólizas", "white"))
            total_general += cantidad

        print(colored("\n-----------------------------", "cyan"))
        print(colored(f"TOTAL GENERAL: {total_general} pólizas", "green", attrs=["bold"]))

        input("\nENTER para volver...")

    @staticmethod
    def total_siniestros_pagados():
        Helpers.limpiar_pantalla()
        print(colored("\n=== TOTAL DINERO PAGADO EN SINIESTROS ===", "cyan", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(monto_reparacion)
            FROM siniestros
        """)

        total = cursor.fetchone()[0]
        conn.close()

        if total is None:
            total = 0

        print(colored(f"\nMonto total pagado: ${total:,.0f}", "green", attrs=["bold"]))

        input("\nENTER para volver...")

     
    @staticmethod
    def cantidad_clientes():
        Helpers.limpiar_pantalla()
        print(colored("\n=== CANTIDAD DE CLIENTES REGISTRADOS ===", "cyan", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM clientes
        """)

        cantidad = cursor.fetchone()[0]

        conn.close()

        print(colored(f"\nCantidad de clientes registrados: {cantidad}", "green", attrs=["bold"]))

        input("\nENTER para volver...")

    
    @staticmethod
    def cantidad_vehiculos():
        Helpers.limpiar_pantalla()
        print(colored("\n=== CANTIDAD DE VEHÍCULOS REGISTRADOS ===", "cyan", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM vehiculos
        """)

        cantidad = cursor.fetchone()[0]

        conn.close()

        print(colored(f"\nCantidad de vehículos registrados: {cantidad}", "green", attrs=["bold"]))

        input("\nENTER para volver...")

    @staticmethod
    def cantidad_polizas():
        Helpers.limpiar_pantalla()
        print(colored("\n=== CANTIDAD TOTAL DE PÓLIZAS ===", "cyan", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM polizas
        """)

        cantidad = cursor.fetchone()[0]

        conn.close()

        print(colored(f"\nCantidad total de pólizas: {cantidad}", "green", attrs=["bold"]))

        input("\nENTER para volver...")

# Clase con funciones para administrar los agentes
class Functions_Agentes:

    @staticmethod
    def registrar_agente():
        Helpers.limpiar_pantalla()
        print(colored("\n=== REGISTRAR AGENTE ===", "blue", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        rut = input("RUT agente: ").strip()

        if not Functions_Clients.validar_rut(rut):
            print(colored("RUT inválido", "red"))
            conn.close()
            input("\nENTER para volver...")
            return

        cursor.execute("SELECT rut FROM agentes WHERE rut = ?", (rut,))
        if cursor.fetchone():
            print(colored("El agente ya está registrado", "yellow"))
            conn.close()
            input("\nENTER para volver...")
            return

        nombre = input("Nombre: ").strip()
        telefono = input("Teléfono: ").strip()

        if nombre == "" or telefono == "":
            print(colored("Debe completar todos los datos", "red"))
            conn.close()
            input("\nENTER para volver...")
            return

        cursor.execute("""
            INSERT INTO agentes (rut, nombre, telefono)
            VALUES (?, ?, ?)
        """, (rut, nombre, telefono))

        conn.commit()
        conn.close()

        print(colored("\n✔ Agente registrado correctamente", "green"))
        input("\nENTER para volver...")

    @staticmethod
    def consultar_agente():
        Helpers.limpiar_pantalla()
        print(colored("\n=== CONSULTAR AGENTE ===", "blue", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        rut = input("RUT agente: ").strip()

        cursor.execute("""
            SELECT rut, nombre, telefono
            FROM agentes
            WHERE rut = ?
        """, (rut,))

        agente = cursor.fetchone()
        conn.close()

        if agente is None:
            print(colored("Agente no encontrado", "red"))
            input("\nENTER para volver...")
            return

        print(colored("\n=== DATOS DEL AGENTE ===", "cyan", attrs=["bold"]))
        print(f"RUT: {agente[0]}")
        print(f"Nombre: {agente[1]}")
        print(f"Teléfono: {agente[2]}")

        input("\nENTER para volver...")

    @staticmethod
    def listar_agentes():
        Helpers.limpiar_pantalla()
        print(colored("\n=== LISTA DE AGENTES ===", "blue", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT rut, nombre, telefono
            FROM agentes
        """)

        agentes = cursor.fetchall()
        conn.close()

        if not agentes:
            print(colored("No hay agentes registrados", "red"))
            input("\nENTER para volver...")
            return

        for a in agentes:
            print(colored("=" * 40, "cyan"))
            print(f"RUT: {a[0]}")
            print(f"Nombre: {a[1]}")
            print(f"Teléfono: {a[2]}")

        print(colored("=" * 40, "cyan"))
        input("\nENTER para volver...")

# Funciones para administrar los registros del sistem
class Functions_Admin:  
    @staticmethod
    def validar_rut(rut: str) -> bool:
        pattern = r"^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$"
        return bool(re.match(pattern, rut))

    @staticmethod
    def editar_cliente():
        rut = input("RUT del cliente: ").strip()

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM clientes WHERE rut = ?", (rut,))
        cliente = cursor.fetchone()

        if not cliente:
            print("Cliente no encontrado")
            input()
            conn.close()
            return

        cursor.execute("PRAGMA table_info(clientes)")
        columnas = cursor.fetchall()

        campos = [col[1] for col in columnas]
        valores = list(cliente)

        while True:
            Helpers.limpiar_pantalla()

            print("=== EDITAR CLIENTE ===")
            print(f"RUT ORIGINAL: {rut}\n")

            for i in range(len(campos)):
                print(f"[{i+1}] {campos[i]}: {valores[i]}")

            print(f"[{len(campos)+1}] Guardar cambios")
            print(f"[{len(campos)+2}] Salir sin guardar")

            op = input("→TEST")

            if not op.isdigit():
                continue

            op = int(op)

          # Edita los campos del registro.
            if 1 <= op <= len(campos):
                nuevo = input(f"Nuevo {campos[op-1]}: ").strip()
                valores[op-1] = nuevo

         
            # Guardar
          
            elif op == len(campos) + 1:

                nuevo_rut = valores[0].strip()

                # Validar el rut
                if not Functions_Admin.validar_rut(nuevo_rut):
                    print("❌ Formato de RUT inválido")
                    input()
                    continue

                # Si el rut cambia y no es el mismo
                if nuevo_rut != rut:

                    cursor.execute("SELECT rut FROM clientes WHERE rut = ?", (nuevo_rut,))
                    if cursor.fetchone():
                        print("❌ Ese RUT ya existe")
                        input()
                        continue

                   # Elimina los registros relacionados manualmente.
                    cursor.execute("""
                        UPDATE vehiculos
                        SET rut_cliente = ?
                        WHERE rut_cliente = ?
                    """, (nuevo_rut, rut))

                    cursor.execute("""
                        UPDATE polizas
                        SET rut_cliente = ?
                        WHERE rut_cliente = ?
                    """, (nuevo_rut, rut))

                    cursor.execute("""
                        UPDATE siniestros
                        SET rut_conductor = ?
                        WHERE rut_conductor = ?
                    """, (nuevo_rut, rut))

               # Actualiza los datos del cliente.

                set_query = ", ".join([f"{campos[i]} = ?" for i in range(len(campos))])

                cursor.execute(
                    f"UPDATE clientes SET {set_query} WHERE rut = ?",
                    (*valores, rut)
                )

                conn.commit()
                conn.close()

                print("✔ Cliente actualizado correctamente")
                input()
                return

            
            # Salir
        
            elif op == len(campos) + 2:
                conn.close()
                return
            
    @staticmethod
    def eliminar_cliente():
        rut = input("RUT del cliente a eliminar: ").strip()

        conn = Database.conectar()
        cursor = conn.cursor()

        # Verificar si existe
        cursor.execute("SELECT * FROM clientes WHERE rut = ?", (rut,))
        cliente = cursor.fetchone()

        if not cliente:
            print("❌ Cliente no encontrado")
            input()
            conn.close()
            return

        print("\n⚠ CLIENTE A ELIMINAR:")
        print(cliente)

        confirm = input("\n¿Seguro que deseas eliminarlo? (s/n): ").strip().lower()

        if confirm != "s":
            print("Cancelado")
            input()
            conn.close()
            return

        try:
           # Elimina los registros relacionados.
            cursor.execute("DELETE FROM vehiculos WHERE rut_cliente = ?", (rut,))
            cursor.execute("DELETE FROM polizas WHERE rut_cliente = ?", (rut,))
            cursor.execute("DELETE FROM siniestros WHERE rut_conductor = ?", (rut,))

            cursor.execute("DELETE FROM clientes WHERE rut = ?", (rut,))

            conn.commit()

            print("✔ Cliente eliminado correctamente")

        except Exception as e:
            print("❌ Error:", e)

        finally:
            conn.close()
            input()
    @staticmethod

    #Modificar vehiculos

    def editar_vehiculo():
        patente = input("Patente del vehículo: ").strip()

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM vehiculos WHERE patente = ?", (patente,))
        vehiculo = cursor.fetchone()

        if not vehiculo:
            print("❌ Vehículo no encontrado")
            input()
            conn.close()
            return

        cursor.execute("PRAGMA table_info(vehiculos)")
        columnas = cursor.fetchall()

        campos = [col[1] for col in columnas]
        valores = list(vehiculo)

        while True:
            Helpers.limpiar_pantalla()

            print("=== EDITAR VEHÍCULO ===")
            print(f"PATENTE ORIGINAL: {patente}\n")

            for i in range(len(campos)):
                print(f"[{i+1}] {campos[i]}: {valores[i]}")

            print(f"[{len(campos)+1}] Guardar cambios")
            print(f"[{len(campos)+2}] Salir sin guardar")

            op = input("→ ")

            if not op.isdigit():
                continue

            op = int(op)

       
            # Modificar Campos
           
            if 1 <= op <= len(campos):

                campo = campos[op - 1]

                # ❌ NO EDITAR RUT CLIENTE
                if campo == "rut_cliente":
                    print("❌ No puedes cambiar el cliente del vehículo aquí")
                    input()
                    continue

                nuevo = input(f"Nuevo {campo}: ").strip()
                valores[op - 1] = nuevo

           # Guardar

            elif op == len(campos) + 1:

                nuevo_patente = valores[0]

                if nuevo_patente != patente:
                    cursor.execute("SELECT patente FROM vehiculos WHERE patente = ?", (nuevo_patente,))
                    if cursor.fetchone():
                        print("❌ Esa patente ya existe")
                        input()
                        continue

                set_query = ", ".join([f"{campos[i]} = ?" for i in range(len(campos))])

                cursor.execute(
                    f"UPDATE vehiculos SET {set_query} WHERE patente = ?",
                    (*valores, patente)
                )

                conn.commit()
                conn.close()

                print("✔ Vehículo actualizado")
                input()
                return

         # Salir
            elif op == len(campos) + 2:
                conn.close()
                return           
    @staticmethod
    def eliminar_vehiculo():

        patente = input("Patente del vehículo a eliminar: ").strip()

        conn = Database.conectar()
        cursor = conn.cursor()

        # Verificar si existe
        cursor.execute("SELECT * FROM vehiculos WHERE patente = ?", (patente,))
        vehiculo = cursor.fetchone()

        if not vehiculo:
            print("❌ Vehículo no encontrado")
            input()
            conn.close()
            return

        print("\n⚠ VEHÍCULO A ELIMINAR:")
        print(vehiculo)

        confirm = input("¿Seguro que deseas eliminarlo? (s/n): ").strip().lower()

        if confirm != "s":
            print("Cancelado")
            input()
            conn.close()
            return

        try:
            cursor.execute("DELETE FROM vehiculos WHERE patente = ?", (patente,))
            conn.commit()

            print("✔ Vehículo eliminado correctamente")

        except Exception as e:
            print("❌ Error:", e)

        finally:
            conn.close()
            input()

    @staticmethod
    def editar_poliza():
        numero = input("Número de póliza: ").strip()

        if not numero.isdigit():
            print("❌ Debe ser un número")
            input()
            return

        numero = int(numero)

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM polizas WHERE numero = ?", (numero,))
        poliza = cursor.fetchone()

        if not poliza:
            print("❌ Póliza no encontrada")
            input()
            conn.close()
            return

        cursor.execute("PRAGMA table_info(polizas)")
        columnas = cursor.fetchall()

        campos = [col[1] for col in columnas]
        valores = list(poliza)

        # Campos que no se pueden editar
        NO_EDITABLE = {"numero", "rut_cliente"}

        while True:
            Helpers.limpiar_pantalla()

            print("=== EDITAR PÓLIZA ===")
            print(f"NÚMERO ORIGINAL: {numero}\n")

            for i in range(len(campos)):
                print(f"[{i+1}] {campos[i]}: {valores[i]}")

            print(f"[{len(campos)+1}] Guardar cambios")
            print(f"[{len(campos)+2}] Salir sin guardar")

            op = input("→ ")

            if not op.isdigit():
                continue

            op = int(op)

            # Edita los campos del registro.

            if 1 <= op <= len(campos):

                campo = campos[op - 1]

                if campo in NO_EDITABLE:
                    print(f"❌ El campo '{campo}' no se puede editar.")
                    input()
                    continue

                nuevo = input(f"Nuevo {campo}: ").strip()
                valores[op - 1] = nuevo

           
            # Guardar
            
            elif op == len(campos) + 1:

                set_query = ", ".join([f"{campo} = ?" for campo in campos])

                try:
                    cursor.execute(
                        f"UPDATE polizas SET {set_query} WHERE numero = ?",
                        (*valores, numero)
                    )

                    conn.commit()
                    print("✔ Póliza actualizada correctamente")

                except Exception as e:
                    print("❌ Error:", e)

                conn.close()
                input()
                return

            
            # Salir
          
            elif op == len(campos) + 2:
                conn.close()
                return
       
    @staticmethod
    def eliminar_poliza():
        numero = input("Número de póliza a eliminar: ").strip()

        if not numero.isdigit():
            print("❌ Debe ingresar un número válido.")
            input()
            return

        numero = int(numero)

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM polizas WHERE numero = ?", (numero,))
        poliza = cursor.fetchone()

        if not poliza:
            print("❌ Póliza no encontrada.")
            conn.close()
            input()
            return

        Helpers.limpiar_pantalla()

        print("=== ELIMINAR PÓLIZA ===")
        print(f"Número: {poliza[0]}")
        print(f"Tipo: {poliza[1]}")
        print(f"Cliente: {poliza[4]}")
        print(f"Patente: {poliza[5]}")

        confirmar = input("\n¿Está seguro de eliminar esta póliza? (S/N): ").strip().upper()

        if confirmar != "S":
            conn.close()
            print("Operación cancelada.")
            input()
            return

        try:
            cursor.execute("DELETE FROM polizas WHERE numero = ?", (numero,))
            conn.commit()
            print("✔ Póliza eliminada correctamente.")

        except Exception as e:
            print("❌ Error:", e)

        conn.close()
        input()
 
    @staticmethod
    def editar_siniestro():
        numero = input("Número del siniestro: ").strip()

        if not numero.isdigit():
            print("❌ Debe ingresar un número válido.")
            input()
            return

        numero = int(numero)

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM siniestros WHERE numero = ?", (numero,))
        siniestro = cursor.fetchone()

        if not siniestro:
            print("❌ Siniestro no encontrado.")
            conn.close()
            input()
            return

        cursor.execute("PRAGMA table_info(siniestros)")
        columnas = cursor.fetchall()

        campos = [col[1] for col in columnas]
        valores = list(siniestro)

        # Campos que no se pueden editar
        NO_EDITABLE = {"numero", "poliza_id"}

        while True:
            Helpers.limpiar_pantalla()

            print("=== EDITAR SINIESTRO ===")
            print(f"NÚMERO ORIGINAL: {numero}\n")

            for i in range(len(campos)):
                print(f"[{i+1}] {campos[i]}: {valores[i]}")

            print(f"[{len(campos)+1}] Guardar cambios")
            print(f"[{len(campos)+2}] Salir sin guardar")

            op = input("→ ")

            if not op.isdigit():
                continue

            op = int(op)

            # Edita los campos del registro.

            if 1 <= op <= len(campos):

                campo = campos[op - 1]

                if campo in NO_EDITABLE:
                    print(f"❌ El campo '{campo}' no se puede editar.")
                    input()
                    continue

                nuevo = input(f"Nuevo {campo}: ").strip()
                valores[op - 1] = nuevo

           
            # Guardar
          
            elif op == len(campos) + 1:

                set_query = ", ".join([f"{campo} = ?" for campo in campos])

                try:
                    cursor.execute(
                        f"UPDATE siniestros SET {set_query} WHERE numero = ?",
                        (*valores, numero)
                    )

                    conn.commit()
                    print("✔ Siniestro actualizado correctamente.")

                except Exception as e:
                    print("❌ Error:", e)

                conn.close()
                input()
                return

           
            # Salir
          
            elif op == len(campos) + 2:
                conn.close()
                return
            
    @staticmethod
    def eliminar_siniestro():
        numero = input("Número del siniestro a eliminar: ").strip()

        if not numero.isdigit():
            print("❌ Debe ingresar un número válido.")
            input()
            return

        numero = int(numero)

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM siniestros WHERE numero = ?", (numero,))
        siniestro = cursor.fetchone()

        if not siniestro:
            print("❌ Siniestro no encontrado.")
            conn.close()
            input()
            return

        Helpers.limpiar_pantalla()

        print("=== ELIMINAR SINIESTRO ===")
        print(f"Número: {siniestro[0]}")
        print(f"Descripción: {siniestro[1]}")
        print(f"Fecha: {siniestro[2]}")
        print(f"Monto reparación: ${siniestro[4]}")

        confirmar = input("\n¿Está seguro de eliminar este siniestro? (S/N): ").strip().upper()

        if confirmar != "S":
            conn.close()
            print("Operación cancelada.")
            input()
            return

        try:
            cursor.execute(
                "DELETE FROM siniestros WHERE numero = ?",
                (numero,)
            )

            conn.commit()
            print("✔ Siniestro eliminado correctamente.")

        except Exception as e:
            print("❌ Error:", e)

        conn.close()
        input()

    @staticmethod
    def editar_agente():
        Helpers.limpiar_pantalla()
        print(colored("\n=== EDITAR AGENTE ===", "blue", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        rut = input("RUT actual del agente: ").strip()

        cursor.execute("""
            SELECT rut, nombre, telefono
            FROM agentes
            WHERE rut = ?
        """, (rut,))

        agente = cursor.fetchone()

        if agente is None:
            print(colored("Agente no encontrado", "red"))
            conn.close()
            input("\nENTER para volver...")
            return

        print(f"\nRUT actual : {agente[0]}")
        print(f"Nombre     : {agente[1]}")
        print(f"Teléfono   : {agente[2]}")

        nuevo_rut = input("\nNuevo RUT: ").strip()

        if not Functions_Clients.validar_rut(nuevo_rut):
            print(colored("RUT inválido", "red"))
            conn.close()
            input("\nENTER para volver...")
            return

        if nuevo_rut != rut:
            cursor.execute(
                "SELECT rut FROM agentes WHERE rut = ?",
                (nuevo_rut,)
            )

            if cursor.fetchone():
                print(colored("Ese RUT ya existe", "red"))
                conn.close()
                input("\nENTER para volver...")
                return

        nuevo_nombre = input("Nuevo nombre: ").strip()
        nuevo_telefono = input("Nuevo teléfono: ").strip()

        if nuevo_nombre == "":
            nuevo_nombre = agente[1]

        if nuevo_telefono == "":
            nuevo_telefono = agente[2]

        cursor.execute("""
            UPDATE agentes
            SET rut = ?, nombre = ?, telefono = ?
            WHERE rut = ?
        """, (
            nuevo_rut,
            nuevo_nombre,
            nuevo_telefono,
            rut
        ))

        cursor.execute("""
            UPDATE polizas
            SET rut_agente = ?
            WHERE rut_agente = ?
        """, (
            nuevo_rut,
            rut
        ))

        conn.commit()
        conn.close()

        print(colored("\n✔ Agente actualizado correctamente", "green"))
        input("\nENTER para volver...")

    @staticmethod
    def eliminar_agente():  
        Helpers.limpiar_pantalla()
        print(colored("\n=== ELIMINAR AGENTE ===", "red", attrs=["bold"]))

        conn = Database.conectar()
        cursor = conn.cursor()

        rut = input("RUT del agente: ").strip()

        cursor.execute("""
            SELECT rut, nombre, telefono
            FROM agentes
            WHERE rut = ?
        """, (rut,))

        agente = cursor.fetchone()

        if agente is None:
            print(colored("Agente no encontrado", "red"))
            conn.close()
            input("\nENTER para volver...")
            return

        cursor.execute("""
            SELECT COUNT(*)
            FROM polizas
            WHERE rut_agente = ?
        """, (rut,))

        if cursor.fetchone()[0] > 0:
            print(colored("No se puede eliminar.", "red"))
            print(colored("El agente tiene pólizas asociadas.", "red"))
            conn.close()
            input("\nENTER para volver...")
            return

        print(colored("\n=== AGENTE ===", "cyan"))
        print(f"RUT      : {agente[0]}")
        print(f"Nombre   : {agente[1]}")
        print(f"Teléfono : {agente[2]}")

        confirmar = input("\n¿Eliminar? (S/N): ").strip().upper()

        if confirmar == "S":
            cursor.execute(
                "DELETE FROM agentes WHERE rut = ?",
                (rut,)
            )

            conn.commit()

            print(colored("\n✔ Agente eliminado correctamente", "green"))
        else:
            print(colored("\nOperación cancelada", "yellow"))

        conn.close()
        input("\nENTER para volver...")
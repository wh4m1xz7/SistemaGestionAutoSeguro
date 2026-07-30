# Importa la conexión a la base de datos.
from Database.Database import Database
from termcolor import colored
import re
import os

# Clase encargada de gestionar las operaciones relacionadas con los clientes.

class ClientManager:

 # Limpia la pantalla de la consola.

    @staticmethod
    def limpiar():
        os.system("cls" if os.name == "nt" else "clear")

# Valida el formato del RUT.
    @staticmethod
    def validar_rut(rut: str) -> bool:
        pattern = r"^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$"
        return bool(re.match(pattern, rut))

# Elimina espacios innecesarios del RUT.
    @staticmethod
    def normalizar_rut(rut: str) -> str:
        return rut.strip()

# Valida y normaliza el RUT ingresado.

    @staticmethod
    def validar_y_normalizar_rut(rut: str):
        rut = ClientManager.normalizar_rut(rut)
        if not ClientManager.validar_rut(rut):
            print(colored("❌ RUT inválido", "red"))
            return None
        return rut

   # Consulta un cliente  con toda la informacion

    @staticmethod
    def cliente_completo():
        ClientManager.limpiar()
        print(colored("\n=== CLIENTE COMPLETO ===", "cyan", attrs=["bold"]))

        rut = input("RUT cliente: ").strip()
        rut = ClientManager.validar_y_normalizar_rut(rut)

        if not rut:
            input("ENTER...")
            return

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM clientes WHERE rut=?", (rut,))
        cliente = cursor.fetchone()

        if not cliente:
            print("❌ Cliente no encontrado")
            conn.close()
            input("ENTER...")
            return

        print(colored("\n👤 CLIENTE", "green"))
        print(f"RUT: {cliente[0]}")
        print(f"Nombre: {cliente[1]}")
        print(f"Apellido: {cliente[2]}")
        print(f"Teléfono: {cliente[3]}")
        print(f"Dirección: {cliente[4]}")
        print(f"Fecha nacimiento: {cliente[5]}")

        cursor.execute("SELECT * FROM vehiculos WHERE rut_cliente=?", (rut,))
        vehiculos = cursor.fetchall()

        print(colored("\n🚗 VEHÍCULOS", "yellow"))
        if vehiculos:
            for v in vehiculos:
                print(f"- {v[0]} | {v[3]} {v[4]} | {v[5]} {v[6]}")
        else:
            print("Sin vehículos")

        cursor.execute("SELECT * FROM polizas WHERE rut_cliente=?", (rut,))
        polizas = cursor.fetchall()

        print(colored("\n📄 PÓLIZAS", "blue"))
        if polizas:
            for p in polizas:
                print(f"- N°{p[0]} | {p[1]} | {p[2]} UF | {p[3]}")
        else:
            print("Sin pólizas")

        cursor.execute("""
            SELECT s.*
            FROM siniestros s
            JOIN polizas p ON s.poliza_id = p.numero
            WHERE p.rut_cliente=?
        """, (rut,))
        siniestros = cursor.fetchall()

        print(colored("\n🚨 SINIESTROS", "red"))
        if siniestros:
            for s in siniestros:
                print(f"- N°{s[0]} | {s[1]} | ${s[4]}")
        else:
            print("Sin siniestros")

        cursor.execute("SELECT SUM(monto_cobertura) FROM polizas WHERE rut_cliente=?", (rut,))
        total_polizas = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT SUM(s.monto_reparacion)
            FROM siniestros s
            JOIN polizas p ON s.poliza_id = p.numero
            WHERE p.rut_cliente=?
        """, (rut,))
        total_siniestros = cursor.fetchone()[0] or 0

        print(colored("\n💰 RESUMEN", "magenta"))
        print(f"Total pólizas: {total_polizas} UF")
        print(f"Total siniestros: ${total_siniestros}")

        conn.close()
        input("\nENTER para volver...")


  # Consulta un cliente por su RUT.
    @staticmethod
    def consultar_cliente():
        ClientManager.limpiar()

        rut = input("RUT: ").strip()
        rut = ClientManager.validar_y_normalizar_rut(rut)

        if not rut:
            input()
            return

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM clientes WHERE rut=?", (rut,))
        c = cursor.fetchone()

        conn.close()

        if not c:
            print("❌ No existe")
        else:
            print(c)

        input()

   
  # Elimina un cliente de forma segura.
    @staticmethod
    def borrar_cliente():
        ClientManager.limpiar()

        rut = input("RUT: ").strip()
        rut = ClientManager.validar_y_normalizar_rut(rut)

        if not rut:
            input()
            return

        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM clientes WHERE rut=?", (rut,))
        cliente = cursor.fetchone()

        if not cliente:
            print("❌ Cliente no existe")
            input()
            conn.close()
            return

        print("⚠ CLIENTE:", cliente)
        confirm = input("¿Seguro que deseas eliminarlo? (s/n): ")

        if confirm.lower() != "s":
            conn.close()
            return

        try:
            cursor.execute("DELETE FROM clientes WHERE rut=?", (rut,))
            conn.commit()
            print("✔ Eliminado correctamente")

        except Exception as e:
            print("Error:", e)

        finally:
            conn.close()
            input()
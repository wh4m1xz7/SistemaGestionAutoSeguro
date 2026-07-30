from termcolor import colored
from Modules.Utilities import (
    Helpers,
    Functions_Admin
)

# Clase de Administracion que engloba todas la funciones para el menu para gestionar la base de dato
class Administracion:

    # Menu de Administrar la base de dato
    def menu_administracion(self):
        while True:
            Helpers.limpiar_pantalla()

            print(colored("=" * 60, "yellow"))
            print(colored("     ADMINISTRACIÓN DE DATOS", "yellow", attrs=["bold"]))
            print(colored("=" * 60, "yellow"))

            print(colored("[1] Clientes", "white"))
            print(colored("[2] Vehículos", "white"))
            print(colored("[3] Pólizas", "white"))
            print(colored("[4] Siniestros", "white"))
            print(colored("[5] Agentes", "white"))
            print(colored("[6] Volver", "green", attrs=["bold"]))

            print(colored("=" * 60, "yellow"))

            op = input("👉 Elige una opción → ")

            if op == "1":
                self.admin_clientes()

            elif op == "2":
                self.admin_vehiculos()

            elif op == "3":
                self.admin_polizas()

            elif op == "4":
                self.admin_siniestros()

            elif op == "5":
                self.admin_agentes()

            elif op == "6":
                break

# Gestionar la Base de dato de Clientes

    def admin_clientes(self):
        while True:
            Helpers.limpiar_pantalla()

            print(colored("=== ADMIN CLIENTES ===", "green"))
            print(colored("[1] Editar cliente", "green"))
            print(colored("[2] Eliminar cliente", "green"))
            print(colored("[3] Volver", "red"))

            op = input("👉 Elige una opción → ")

            if op == "1":
                Functions_Admin.editar_cliente()

            elif op == "2":
                Functions_Admin.eliminar_cliente()

            elif op == "3":
                break

# Gestionar la Base de Vehiculos
    def admin_vehiculos(self):
        while True:
            Helpers.limpiar_pantalla()

            print(colored("=== ADMIN VEHÍCULOS ===", "yellow"))
            print(colored("[1] Editar vehículo", "yellow"))
            print(colored("[2] Eliminar vehículo", "yellow"))
            print(colored("[3] Volver", "red"))

            op = input("👉 Elige una opción → ")

            if op == "1":
                Functions_Admin.editar_vehiculo()

            elif op == "2":
                Functions_Admin.eliminar_vehiculo()

            elif op == "3":
                break

 # Gestionar la Base de dato Poliza
    def admin_polizas(self):
        while True:
            Helpers.limpiar_pantalla()

            print(colored("=== ADMIN PÓLIZAS ===", "magenta"))
            print(colored("[1] Editar póliza", "magenta"))
            print(colored("[2] Eliminar póliza", "magenta"))
            print(colored("[3] Volver", "red"))

            op = input("👉 Elige una opción → ")

            if op == "1":
                Functions_Admin.editar_poliza()

            elif op == "2":
                Functions_Admin.eliminar_poliza()

            elif op == "3":
                break

  # Gestionar la Base de dato Siniestros
    def admin_siniestros(self):
        while True:
            Helpers.limpiar_pantalla()

            print(colored("=== ADMIN SINIESTROS ===", "red"))
            print(colored("[1] Editar siniestro", "red"))
            print(colored("[2] Eliminar siniestro", "red"))
            print(colored("[3] Volver", "red"))

            op = input("👉 Elige una opción → ")

            if op == "1":
                Functions_Admin.editar_siniestro()

            elif op == "2":
                Functions_Admin.eliminar_siniestro()

            elif op == "3":
                break

   # Gestionar la Base de dato de agentes
    def admin_agentes(self):
        while True:
            Helpers.limpiar_pantalla()

            print(colored("=== ADMIN AGENTES ===", "blue"))
            print(colored("[1] Editar agente", "blue"))
            print(colored("[2] Eliminar agente", "blue"))
            print(colored("[3] Volver", "red"))

            op = input("👉 Elige una opción → ")

            if op == "1":
             Functions_Admin.editar_agente()

            elif op == "2":
                Functions_Admin.eliminar_agente()
            elif op == "3":
                break
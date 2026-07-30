from termcolor import colored

from Modules.Utilities import Helpers , Functions_Clients , Functions_Cars ,  Functions_Polizas,Functions_Siniestros, Functions_reportes,Functions_Admin,Functions_Agentes
from Database.CustomerManager import ClientManager
import time
from Modules.administration import Administracion


# Clase que  tiene dentro todas las funciones del menus

class Menu_principal:

    # Se crea una instancia de la clase Administracion para poder acceder
    # a todos los submenús y funciones de administración desde el menú principal 
    def __init__(self):
        self.admin = Administracion()
   
# Menu Principal

    def main_menu(self):
        while True:
            Helpers.limpiar_pantalla()

            print(colored("=" * 60, "cyan"))
            print(colored("        SISTEMA AUTO SEGURO S.A", "cyan", attrs=["bold"]))
            print(colored("=" * 60, "cyan"))

            print(colored("[1] Clientes", "cyan"))
            print(colored("[2] Vehículos", "cyan"))
            print(colored("[3] Pólizas", "cyan"))
            print(colored("[4] Siniestros", "cyan"))
            print(colored("[5] Agente", "cyan"))
            print(colored("[6] Reportes", "cyan"))
            print(colored("[7] Administración de datos", "cyan"))
            print(colored("[8] Vista general", "cyan"))
            print(colored("[9] Salir", "red"))

            print(colored("=" * 60, "cyan"))

            op = input(colored("Seleccione opción: ", "cyan"))

            if op == "1":
                self.menu_clientes()

            elif op == "2":
                self.menu_vehiculos()

            elif op == "3":
                self.menu_polizas()

            elif op == "4":
                self.menu_siniestros()

            elif op == "5":
                self.menu_agentes() 

            elif op == "6":
                self.menu_reportes()

            elif op == "7":
               self.admin.menu_administracion()

            elif op == "8":
                self.vista_general()

            elif op == "9":
                Helpers.salida_sistema()
                break

  # Menu de vista general
    def vista_general(self):
        Helpers.limpiar_pantalla()

        print(colored("=" * 60, "magenta"))
        print(colored("     VISTA GENERAL DEL SISTEMA", "magenta", attrs=["bold"]))
        print(colored("=" * 60, "magenta"))

        print(colored("👤 Clientes        → Personas aseguradas", "magenta"))
        print(colored("🚗 Vehículos       → Autos registrados", "magenta"))
        print(colored("📄 Pólizas         → Seguros contratados", "magenta"))
        print(colored("👨 Agentes         → Ejecutivos de ventas", "magenta"))
        print(colored("🚨 Siniestros      → Accidentes registrados", "magenta"))
        print(colored("📊 Reportes        → Estadísticas y totales", "magenta"))
        print(colored("⚙ Administración  → Editar y eliminar registros", "magenta"))
              

        print(colored("=" * 60, "magenta"))      
        input(colored("\nENTER para volver...", "magenta"))

   # Menu de clients
    def menu_clientes(self):
        while True:
            Helpers.limpiar_pantalla()

            print(colored("=" * 50, "green"))
            print(colored("        CLIENTES", "green", attrs=["bold"]))
            print(colored("=" * 50, "green"))

            print(colored("[1] Registrar cliente", "green"))
            print(colored("[2] Buscar cliente", "green"))
            print(colored("[3] Ficha del cliente (completa)", "green"))
            print(colored("[4] Volver", "red"))

            print(colored("=" * 50, "green"))

            op = input(colored("Opción: ", "green"))

            if op == "1":
                Functions_Clients.registrar_cliente()

            elif op == "2":
                Functions_Clients.consultar_cliente()

            elif op == "3":
                ClientManager.cliente_completo()

            elif op == "4":
                break


  
  # Menu de vehiculos
    def menu_vehiculos(self):
      while True:
        Helpers.limpiar_pantalla()

        print(colored("=" * 50, "yellow"))
        print(colored("        VEHÍCULOS", "yellow", attrs=["bold"]))
        print(colored("=" * 50, "yellow"))

        print(colored("[1] Registrar vehículo", "yellow"))
        print(colored("[2] Consultar vehículo por patente", "yellow"))
        print(colored("[3] Listar vehículos", "yellow"))
        print(colored("[4] Volver", "red"))

        print(colored("=" * 50, "yellow"))

        op = input(colored("Opción: ", "yellow"))

        if op == "1":
            Functions_Cars.registrar_vehiculo()

        elif op == "2":
           Functions_Cars.consultar_vehiculo()

        elif op == "3":
            Functions_Cars.listar_vehiculos()

        elif op == "4":
            break

  # Menu polizas
    def menu_polizas(self):
       while True:
        Helpers.limpiar_pantalla()

        print(colored("=" * 50, "magenta"))
        print(colored("          PÓLIZAS", "magenta", attrs=["bold"]))
        print(colored("=" * 50, "magenta"))

        print(colored("[1] Registrar póliza", "magenta"))
        print(colored("[2] Consultar póliza por número", "magenta"))
        print(colored("[3] Listar pólizas", "magenta"))
        print(colored("[4] Total de pólizas vendidas", "magenta"))
        print(colored("[5] Volver", "red"))

        print(colored("=" * 50, "magenta"))

        op = input(colored("Opción: ", "magenta"))

        if op == "1":
            Functions_Polizas.registrar_poliza()

        elif op == "2":
            Functions_Polizas.consultar_poliza()

        elif op == "3":
            Functions_Polizas.listar_polizas()
 
        elif op == "4":
            Functions_Polizas.total_polizas()


        elif op == "5":
            break

    # Menu siniestros

    def menu_siniestros(self):
        while True:
            Helpers.limpiar_pantalla()

            print(colored("=" * 50, "red"))
            print(colored("        SINIESTROS", "red", attrs=["bold"]))
            print(colored("=" * 50, "red"))

            print(colored("[1] Registrar siniestro", "red"))
            print(colored("[2] Consultar siniestro por número", "red"))
            print(colored("[3] Listar siniestros", "red"))
            print(colored("[4] Volver", "yellow"))

            print(colored("=" * 50, "red"))

            op = input(colored("Opción: ", "red"))

            if op == "1":
                Functions_Siniestros.registrar_siniestro()

            elif op == "2":
                Functions_Siniestros.consultar_siniestro()

            elif op == "3":
                Functions_Siniestros.listar_siniestros()

            elif op == "4":
                break

  
    # Menu reportes
    
    def menu_reportes(self):
       while True:
        Helpers.limpiar_pantalla()

        print(colored("=" * 55, "cyan"))
        print(colored("             PANEL DE REPORTES", "green", attrs=["bold"]))
        print(colored("=" * 55, "cyan"))

        print(colored("[1] Monto total en pesos por tipo de póliza", "white"))
        print(colored("[2] Total de siniestros Pagados", "white"))
        print(colored("[3] Cantidad de clientes registrados", "white"))
        print(colored("[4] Cantidad de vehículos registrados", "white"))
        print(colored("[5] Cantidad total de pólizas registradas", "white"))

        print(colored("[6] Volver", "green", attrs=["bold"]))

        print(colored("=" * 55, "cyan"))

        op = input(colored("Selecciona opción → ", "green"))

        if op == "1":
            Functions_reportes.reporte_polizas_por_tipo()

        elif op == "2":
            Functions_reportes.total_siniestros_pagados()
        elif op == "3":
            Functions_reportes.cantidad_clientes()

        elif op == "4":
            Functions_reportes.cantidad_vehiculos()
            input()

        elif op == "5":
            Functions_reportes.cantidad_polizas()
       
        elif op == "6":
            break

   # Menu de agentes
    @staticmethod
    def menu_agentes():
      while True:
        Helpers.limpiar_pantalla()
        print(colored("\n=== MENÚ AGENTES ===", "blue", attrs=["bold"]))

        print(colored("[1] Registrar agente", "green"))
        print(colored("[2] Consultar agente", "green"))
        print(colored("[3] Listar agentes", "green"))
        print(colored("[4] Volver", "red"))

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
             Functions_Agentes.registrar_agente()
 
        elif opcion == "2":
            Functions_Agentes.consultar_agente()

        elif opcion == "3":
            Functions_Agentes.listar_agentes()

        elif opcion == "4":
            break

        else:
            print(colored("Opción inválida", "red"))
            input("\nENTER para continuar...")



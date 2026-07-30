from Modules.menu import Menu_principal
from Database.Database import Database
from Modules.Utilities import Helpers
import signal




  # Inicia progama
if __name__ == "__main__":
   
   
   #crea la tabla 
    Database.crear_tablas()

      # Ctrl + C
    signal.signal(signal.SIGINT, Helpers.control_De_salida)
     
   # Crea una instancia del menú principal.
    app = Menu_principal()
   # Inicia el menú principal.
    app.main_menu() 
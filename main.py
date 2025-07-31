"""
===============================================================================
Sistema de Gestión de Viajes Corporativos Multimodales
===============================================================================

Descripción:
Este sistema simula una aplicación de escritorio por consola que permite 
gestionar viajes empresariales combinando múltiples medios de transporte 
(avión, tren, taxi, colectivo, etc.), registrar gastos, planificar itinerarios 
y controlar presupuestos.

Modo de uso:
1. Asegúrese de tener Python 3 instalado en su computadora.
2. Ejecute el archivo con el comando: python main.py
3. Siga las instrucciones del menú para navegar por el sistema.

Autores:
- Juan Pablo Mercado

Fecha de inicio: Julio 2025
Versión: Prototipo funcional - Semana 2
"""

def main():
    print("A continuación se presentan las diferentes opciones del sistema")
    print("Pr favor, seleccione una opción:")
    try: 
        
        while True:
            print("1 - Registrar una empresa")
            print("2 - Registrar un empleado")
            print("3 - Registrar un viaje")
            print("4 - Listar destinos")
            print("5 - Historial de cambios")
            print("0 - Salir")
            opcion = input("Ingrese su opción: ")

            if opcion == "1":
                pass
            elif opcion == "2":
                pass
            elif opcion == "3":
                pass
            elif opcion == "4":
                pass
            elif opcion == "5":
                pass
            elif opcion == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")

    except Exception as e:
        print(f"Se ha producido un error: {e}")

if __name__ == "__main__":
    main()
else:
    print("Este script debe ejecutarse directamente, no como un módulo importado.")



















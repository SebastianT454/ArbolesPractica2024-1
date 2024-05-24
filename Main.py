from Arboles import *
from ExpresionAlgebraica import *

class Operacion:
    def __init__(self) -> None:
        self.Expresion = None
        self.Arbol = None

Operacion_actual = Operacion()

def crear_expresion():
  cadena = input("Ingrese la expresion algebraica: ")

  if not cadena:
    print("No se ingreso nada..")
    return
  
  Operacion_actual.Expresion = ExpresionAlgebraica(cadena)
  Expresion_valida = Operacion_actual.Expresion.esValidaExpresion()

  if not Expresion_valida:
    return

  print(Operacion_actual.Expresion.lista_terminos)

  ArbolGenerado = Operacion_actual.Expresion.construirExpresion(Operacion_actual.Expresion.lista_terminos)

  Operacion_actual.Arbol = ArbolGenerado

def visualizar_arbol_expresiones():
  if not Operacion_actual.Arbol:
    print("El arbol no existe aùn, grave!")

  Operacion_actual.Arbol.print(Operacion_actual.Arbol.root)

def evaluar_arbol_expresiones():
  if Operacion_actual.Arbol.root is None or not Operacion_actual.Arbol:
    print("No hay nada en el Arbol o no existe!")

  print(f"El resultado de la operacion del arbol fue: {Operacion_actual.Arbol.evaluate(Operacion_actual.Arbol.root)}")

while True:
  print("\nMenú de Expresiones:")
  print("1. Crear Expresión")
  print("2. Visualizar Árbol de Expresiones")
  print("3. Evaluar Árbol de Expresiones")
  print("4. Nueva Operacion")
  print("5. Salir")

  opcion = input("Ingrese su opción: ")

  if opcion == "1":
    crear_expresion()
  elif opcion == "2":
    visualizar_arbol_expresiones()
  elif opcion == "3":
    evaluar_arbol_expresiones()
  elif opcion == "4":
    Operacion_actual.Expresion = None
    Operacion_actual.Arbol = None
    crear_expresion()
  elif opcion == "5":
    print("Saliendo del programa...")
    break
  else:
    print("Opción no válida. Intente de nuevo.")

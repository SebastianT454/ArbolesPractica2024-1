import re

from Arboles import *
from Verificaciones import *

class ExpresionAlgebraica:
    def __init__(self, expresion) -> None:
        self.expresion = expresion
        self.lista_terminos = None
        self.resultado = None

    def esValidaExpresion(self):
        try:
            terminosValidos(self.expresion)
            expresionIncompleta(self.expresion)
            parentesisValidos(self.expresion)
            operadoresValidos(self.expresion)

            return True
        except Exception as err:
            print(err)
            return False
    
    def separarTerminos(self, terminos_validos = ["*", "/", "+","-", "(",")"]):
        if not self.expresion:
            raise Exception(f"No hay expresión!")
        
        elementos = []
        elemento_actual = ''
        
        for caracter in self.expresion:
            if caracter == ' ':
                continue

            elif caracter in terminos_validos:
                if elemento_actual:
                    elementos.append(elemento_actual)
                    elemento_actual = ''
                elementos.append(caracter)

            elif caracter.isdigit() or caracter is ".":
                elemento_actual += caracter
        
        if elemento_actual:
            elementos.append(elemento_actual)
        
        self.lista_terminos = elementos

    def cnt_operadorEnExpresion(self, operador, contador = 0):
        for termino in self.lista_terminos:
            if termino == operador:
                contador += 1
        return contador

    def verificarLadoIzquierdoOperacion(self, indx_operando, operadores_visitados, indices = 1, terminos_invalidos = ["*", "/", "+","-",")"]):
        indice_actual = indx_operando - indices

        if indice_actual == 0 or indice_actual in operadores_visitados:
            return True
        
        if self.lista_terminos[indice_actual] in terminos_invalidos:
            return False
        
        return self.verificarLadoIzquierdoOperacion(indx_operando, operadores_visitados, indices + 1)

    def verificarLadoDerechoOperacion(self, indx_operando, operadores_visitados, indices = 1, terminos_invalidos = ["*", "/", "+","-","("]):
        indice_actual = indx_operando + indices

        if indice_actual == len(self.lista_terminos)-1 or indice_actual in operadores_visitados:
            return True
        
        if self.lista_terminos[indice_actual] in terminos_invalidos:
            return False
            
        return self.verificarLadoDerechoOperacion(indx_operando, operadores_visitados, indices + 1)

    def construirArbolExpresion(self, operadores = ["-","+","/","*"]):
        arbol = ExpressionAnalysisTree()
        indices_totales_visitados = []

        for operador in operadores:
            indices_visitados = []

            for _ in range(self.cnt_operadorEnExpresion(operador)):

                for indx_termino in range(len(self.lista_terminos) - 1, -1, -1):

                    if self.lista_terminos[indx_termino] == operador and indx_termino not in indices_visitados:

                        termino_izquierdo_valido = self.verificarLadoIzquierdoOperacion(indx_termino, indices_totales_visitados)
                        termino_derecho_valido = self.verificarLadoDerechoOperacion(indx_termino, indices_totales_visitados)

                        arbol.insert(arbol.root, indx_termino, self.lista_terminos[indx_termino])

                        indices_visitados.append(indx_termino)
                        indices_totales_visitados.append(indx_termino)

                        if termino_izquierdo_valido:
                            indx_operando_izquierdo = indx_termino - 1
                            arbol.insert(arbol.root, indx_operando_izquierdo, self.lista_terminos[indx_operando_izquierdo])

                        if termino_derecho_valido:
                            indx_operando_derecho = indx_termino + 1
                            arbol.insert(arbol.root, indx_operando_derecho, self.lista_terminos[indx_operando_derecho])

        return arbol
    
    def parentesisEnExpresion(self, parentesis = ["(",")"]):
        for termino in self.expresion:
            if termino in parentesis:
                return True
        return False
    
    def evaluar_subexpresiones(self):
        while '(' in self.expresion:
            subexpresion = re.search(r'\([^()]*\)', self.expresion)

            if subexpresion:
                print("Expresion actualizada:", self.expresion, "subexpresion:", subexpresion.group(0))
                subexpresion_evaluada = self.desarollarParentesisInterno( subexpresion.group(0) )

                self.expresion = self.expresion[:subexpresion.start()] + subexpresion_evaluada + self.expresion[subexpresion.end():]
    
    def obtenerExpresionParentesis(self, expresion, agrupacion = ["(",")"]):
        expresion_interna = ""
        
        for termino in expresion:
            if termino not in agrupacion:
                expresion_interna += termino
        
        return expresion_interna
    
    def desarollarParentesisInterno(self, expresion):
        expresion_sin_parentesis = self.obtenerExpresionParentesis(expresion)

        expresion_actual = ExpresionAlgebraica(expresion_sin_parentesis)
        expresion_actual.separarTerminos()

        #print("Terminos actual: ", expresion_actual.lista_terminos)

        if len(expresion_actual.lista_terminos) <= 2:
            return expresion_sin_parentesis

        ArbolGenerado = expresion_actual.construirArbolExpresion()

        #print("Arbol Expresion Parentesis:")
        #ArbolGenerado.print(ArbolGenerado.root)

        return str( ArbolGenerado.evaluate( ArbolGenerado.root ) )

    def construirExpresion(self):
        existenParentesis = self.parentesisEnExpresion()

        if not existenParentesis:
            self.separarTerminos()
            return
        
        self.evaluar_subexpresiones()
        self.separarTerminos()

        print("Expresion final:", self.expresion, "Lista de terminos:", self.lista_terminos)

        if len(self.lista_terminos) <= 2:
            self.resultado = self.expresion
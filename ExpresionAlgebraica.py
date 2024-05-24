from Arboles import *

class ExpresionAlgebraica:
    def __init__(self, expresion) -> None:
        self.expresion = expresion
        self.lista_terminos = None

    def esValidaExpresion(self):
        try:
            self.separarTerminos()
            self.expresionIncompleta()
            self.parentesisValidos()
            self.operadoresValidos()

            return True
        except Exception as err:
            print(err)
            return False

    def parentesisValidos(self):
        lista_parentesis = []
        estructura_parentesis = {")" : "("}

        cadena_solo_parentesis = []

        for termino in self.lista_terminos:
            if termino in ["(",")"]:
                cadena_solo_parentesis.append(termino)

        for termino in cadena_solo_parentesis:
            if termino in estructura_parentesis:
                if lista_parentesis and lista_parentesis[-1] == estructura_parentesis[termino]:
                    lista_parentesis.pop()
                else:
                    raise Exception(f"Parentesis desbalanceados!")
            else:
                lista_parentesis.append(termino)
        
        if lista_parentesis:
            raise Exception(f"Parentesis desbalanceados!") 
    
    def expresionIncompleta(self):
        if len(self.lista_terminos) < 3:
            raise Exception(f"Expresion no tiene al menos 1 operador y dos operandos!") 
    
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

            elif caracter.isdigit():
                elemento_actual += caracter
        
        if elemento_actual:
            elementos.append(elemento_actual)
        
        self.lista_terminos = elementos
    
    def operadoresValidos(self, operadores = ["*", "/", "+","-"]):
        for operador in operadores:
            for indx_termino in range(len(self.lista_terminos)):

                if self.lista_terminos[indx_termino] == operador:
                    indx_operando_izquierdo = indx_termino - 1
                    indx_operando_derecho = indx_termino + 1

                    if indx_operando_izquierdo < 0:
                        raise Exception(f"Operador o invalido faltante entre dos operandos!")
                    
                    if indx_operando_derecho == len(self.lista_terminos):
                        raise Exception(f"Operador faltante o invalido entre dos operandos!")
                    
                    if self.lista_terminos[indx_operando_izquierdo] in operadores or self.lista_terminos[indx_operando_izquierdo] == "(":
                        raise Exception(f"Operador faltante o invalido entre dos operandos!")
                    
                    if self.lista_terminos[indx_operando_derecho] in operadores or self.lista_terminos[indx_operando_derecho] == ")":
                        raise Exception(f"Operador faltante o invalido entre dos operandos!")

    def separarParentesis(self, indx_apertura_parentesis = None, indx_cerradura_parentesis = None, elementos_parentesis = [], elementos_indice = []):
        for indx_termino in range(len(self.lista_terminos)):
            if self.lista_terminos[indx_termino] == "(":
                indx_apertura_parentesis = indx_termino

            if self.lista_terminos[indx_termino] == ")":
                indx_cerradura_parentesis = indx_termino
                break

        for indx_termino_parentesis in range(indx_apertura_parentesis + 1, indx_cerradura_parentesis):
            elementos_parentesis.append(self.lista_terminos[indx_termino_parentesis])
            elementos_indice.append(self.lista_terminos.index(self.lista_terminos[indx_termino_parentesis]))
        
        elementos_indice.append(indx_apertura_parentesis)
        elementos_indice.append(indx_cerradura_parentesis)

        return [elementos_parentesis, elementos_indice]
    
    def parentesisEnExpresion(self, parentesis = ["(",")"]):
        for termino in self.lista_terminos:
            if termino in parentesis:
                return True
        return False

    def cnt_operadorEnExpresion(self, lista_terminos_expresion, operador, contador = 0):
        for termino in lista_terminos_expresion:
            if termino == operador:
                contador += 1
        return contador

    def verificarLadoIzquierdoOperacion(self, lista_terminos_expresion, indx_operando, operadores_visitados, indices = 1, terminos_invalidos = ["*", "/", "+","-",")"]):
        indice_actual = indx_operando - indices

        if indice_actual == 0 or indice_actual in operadores_visitados:
            return True
        
        if lista_terminos_expresion[indice_actual] in terminos_invalidos:
            return False
        
        return self.verificarLadoIzquierdoOperacion(lista_terminos_expresion, indx_operando, operadores_visitados, indices + 1)

    def verificarLadoDerechoOperacion(self, lista_terminos_expresion, indx_operando, operadores_visitados, indices = 1, terminos_invalidos = ["*", "/", "+","-","("]):
        indice_actual = indx_operando + indices

        if indice_actual == len(lista_terminos_expresion)-1 or indice_actual in operadores_visitados:
            return True
        
        if lista_terminos_expresion[indice_actual] in terminos_invalidos:
            return False
            
        return self.verificarLadoDerechoOperacion(lista_terminos_expresion, indx_operando, operadores_visitados, indices + 1)

    def construirExpresion(self, lista_terminos_expresion, operadores = ["-","+","/","*"]):
        arbol = ExpressionAnalysisTree()
        indices_totales_visitados = []

        for operador in operadores:
            indices_visitados = []

            for _ in range(self.cnt_operadorEnExpresion(lista_terminos_expresion, operador)):

                for indx_termino in range(len(lista_terminos_expresion) - 1, -1, -1):

                    if lista_terminos_expresion[indx_termino] == operador and indx_termino not in indices_visitados:

                        termino_izquierdo_valido = self.verificarLadoIzquierdoOperacion(lista_terminos_expresion, indx_termino, indices_totales_visitados)
                        termino_derecho_valido = self.verificarLadoDerechoOperacion(lista_terminos_expresion, indx_termino, indices_totales_visitados)

                        arbol.insert(arbol.root, indx_termino, lista_terminos_expresion[indx_termino])
                        indices_visitados.append(indx_termino)
                        indices_totales_visitados.append(indx_termino)

                        if termino_izquierdo_valido:
                            indx_operando_izquierdo = indx_termino - 1
                            arbol.insert(arbol.root, indx_operando_izquierdo, lista_terminos_expresion[indx_operando_izquierdo])

                        if termino_derecho_valido:
                            indx_operando_derecho = indx_termino + 1
                            arbol.insert(arbol.root, indx_operando_derecho, lista_terminos_expresion[indx_operando_derecho])

        return arbol

    def construirArbolDeExpresion(self, arbol_general):
        while self.parentesisEnExpresion():
            parentesis = self.separarParentesis()
            parentesis_terminos = parentesis[0]
            parentesis_indices = parentesis[1]

"""
# Ejemplo de uso
cadena = "(10 / 2) + 32 - 12 - (900 + 8)"
Expresion = ExpresionAlgebraica(cadena)
print(Expresion.esValidaExpresion())
print(Expresion.lista_terminos)
Arbol = Expresion.construirExpresion(Expresion.lista_terminos)
Arbol.print(Arbol.root)
print(Arbol.evaluate(Arbol.root))
"""
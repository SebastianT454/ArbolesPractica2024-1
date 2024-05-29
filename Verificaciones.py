def parentesisValidos(expresion):
    lista_parentesis = []
    estructura_parentesis = {")" : "("}

    cadena_solo_parentesis = []

    for termino in expresion:
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
    
def operadoresValidos(expresion, operadores = ["*", "/", "+","-"]):
    lista_terminos = obtenerListaTerminos(expresion)

    for operador in operadores:
        for indx_termino in range(len(lista_terminos)):

            if lista_terminos[indx_termino] == operador:
                indx_operando_izquierdo = indx_termino - 1
                indx_operando_derecho = indx_termino + 1

                if indx_operando_izquierdo < 0:
                    raise Exception(f"Operador o invalido faltante entre dos operandos!")
                
                if indx_operando_derecho == len(lista_terminos):
                    raise Exception(f"Operador faltante o invalido entre dos operandos!")
                
                if lista_terminos[indx_operando_izquierdo] in operadores or lista_terminos[indx_operando_izquierdo] == "(":
                    raise Exception(f"Operador faltante o invalido entre dos operandos!")
                
                if lista_terminos[indx_operando_derecho] in operadores or lista_terminos[indx_operando_derecho] == ")":
                    raise Exception(f"Operador faltante o invalido entre dos operandos!")
                
def expresionIncompleta(expresion):
    lista_terminos = obtenerListaTerminos(expresion)
    if len(lista_terminos) < 3:
        raise Exception(f"Expresion no tiene al menos 1 operador y dos operandos!")
    
def terminosValidos(expresion, terminos_validos = ["*", "/", "+", "-", "(", ")"]):
    for elemento in expresion:
        if elemento != " ":
            if not elemento.isdigit() and elemento not in terminos_validos:
                raise ValueError(f"Elemento no valido: {elemento}")
            
def obtenerListaTerminos(expresion):
    lista_terminos = []

    for elemento in expresion:
        if elemento != " ":
            lista_terminos.append(elemento)

    return lista_terminos
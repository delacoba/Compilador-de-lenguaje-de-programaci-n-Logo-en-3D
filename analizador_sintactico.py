import ply.yacc as yacc
from analizador_lexico import tokens
from analizador_semantico import *

listaVariablesInicializadas=set()
listaFuncionesDefinidas=set()

#definimos la precedencia de nuestros tokens y cuales se deben analizar por la izquierda o por la derecha
precedence = (
    #tokens de menor precedencia
    ('right', 'IGUAL'),
    ('left', 'MAS'),
    ('left', 'MENOS'),
    ('left', 'MULTIPLICAR'),
    ('left', 'DIVIDIR'),
    ('left', 'PARENTESIS_IZDA', 'PARENTESIS_DCHA'),
    ('left', 'LITERAL_ENTERO'),
    #tokens de mayor precedencia
)

#estableemos las producciones. Indicando las reglas gramatical

# <programa> ::= PROGRAM <identificador> <bloque>
def p_programa(p):
    '''programa : PROGRAM IDENTIFICADOR bloque'''
    p[0] =  programa(p[2], p[3])
    
# <bloque> ::= <declaracion_funciones> <instrucciones> 
def p_bloque(p):
    '''bloque : declaracion_funciones instrucciones'''
    p[0] = bloque(p[1], p[2])    


# <declaracion_funciones> ::= <declaracion_funcion>  <declaracion_funciones> | e
# <declaracion_funcion> ::= PARA <identificador> <parametros> <instrucciones> FIN 
def p_declaracion_funciones(p):
    '''declaracion_funciones : declaracion_funcion declaracion_funciones'''
    p[0] = declaracion_funciones(p[1], p[2])

def p_declaracion_funciones_empty(p):
    '''declaracion_funciones : empty'''
    p[0] = declaracion_funciones_empty()


def p_declaracion_funcion(p):
    '''declaracion_funcion : PARA IDENTIFICADOR parametros instrucciones FIN'''
    p[0] = declaracion_funcion(p[2], p[3], p[4])

    nombreFuncion=p[2]
    global listaFuncionesDefinidas, listaVariablesInicializadas

    if nombreFuncion in listaFuncionesDefinidas:
        yacc.yacc.erroresSemanticosDetectados.append(f"ERROR SEMANTICO, FUNCIÓN {p[2]} EN LINEA {p.lineno(2)} YA ESTÁ DEFINIDA PREVIAMENTE") 
        yacc.yacc.numErroresSemanticos += 1
    else:
        # SE ALMACENA EL NOMBRE DE LA FUNCIÓN, PARA QUE SI SE DEFINE UNA SEGUNDA VEZ SE DETECTE
        listaFuncionesDefinidas.add(nombreFuncion)
    listaVariablesInicializadas=set()


# <parametros> ::= ( <lista_parametros> ) | e
# <lista_parametro> ::= VARIABLE | VARIABLE COMA <lista_parametros>
def p_parametros(p):
    '''parametros : PARENTESIS_IZDA lista_parametros PARENTESIS_DCHA'''
    p[0] = parametros(p[2])

def p_parametros_empty(p):
    '''parametros : empty'''
    p[0] = parametros_empty()

def p_lista_parametros_uno(p):
    '''lista_parametros : VARIABLE'''
    p[0] = lista_parametros_uno(p[1])

    nombreParametro=p[1]
    global listaVariablesInicializadas
    listaVariablesInicializadas.add(nombreParametro)

def p_lista_parametros_varios(p):
    '''lista_parametros : VARIABLE COMA lista_parametros'''
    p[0] = lista_parametros_varios(p[1], p[3])

    nombreParametro=p[1]
    global listaVariablesInicializadas
    listaVariablesInicializadas.add(nombreParametro)

# <instrucciones> ::= <instruccion> | <instrucciones> <instruccion>
def p_instrucciones_empty(p):
    '''instrucciones : empty'''
    p[0] = instrucciones_empty()

def p_instrucciones(p):
    '''instrucciones : instruccion instrucciones '''
    p[0] = instrucciones(p[1], p[2])

# <instruccion> ::= <perspectiva> | <movimiento> | <giro> | <cambiocolor> | <bucle> | <guardar> | <llamada_funcion>
def p_instruccion_perspectiva(p):
    '''instruccion : PERSPECTIVA '''
    p[0] = instruccion_perspectiva(p[1])

def p_instruccion_movimiento(p):
    '''instruccion : movimiento '''
    p[0] = instruccion_movimiento(p[1])

def p_instruccion_giro(p):
    '''instruccion : giro '''
    p[0] = instruccion_giro(p[1])

def p_instruccion_cambiocolorlapiz(p):
    '''instruccion : cambiocolorlapiz '''
    p[0] = instruccion_cambiocolorlapiz(p[1])

def p_instruccion_cambiocolorfondo(p):
    '''instruccion : cambiocolorfondo '''
    p[0] = instruccion_cambiocolorfondo(p[1])

def p_instruccion_bucle(p):
    '''instruccion : bucle '''
    p[0] = instruccion_bucle(p[1])

def p_instruccion_goma(p):
    '''instruccion : GOMA '''
    p[0] = instruccion_goma()

def p_instruccion_centro(p):
    '''instruccion : CENTRO '''
    p[0] = instruccion_centro()

def p_instruccion_subelapiz(p):
    '''instruccion : SUBELAPIZ '''
    p[0] = instruccion_subelapiz()

def p_instruccion_bajalapiz(p):
    '''instruccion : BAJALAPIZ '''
    p[0] = instruccion_bajalapiz()

def p_instruccion_asignacion(p):
    '''instruccion : asignacion '''
    p[0] = instruccion_asignacion(p[1])

def p_instruccion_call(p):
    '''instruccion : llamada_funcion '''
    p[0] = instruccion_call(p[1])

def p_expression_plus(p):
    '''expresion : expresion MAS termino'''
    p[0] = expression_plus(p[1], p[3])

def p_expression_minus(p):
    '''expresion : expresion MENOS termino'''
    p[0] = expression_minus(p[1], p[3])

def p_expresion_termino(p):
    '''expresion : termino'''
    p[0] = expresion_termino(p[1])

def p_term_multiplicar(p):
    '''termino : termino MULTIPLICAR factor'''
    p[0] = term_multiplicar(p[1], p[3])

def p_term_dividir(p):
    '''termino : termino DIVIDIR factor'''
    p[0] = term_dividir(p[1], p[3])

def p_term_factor(p):
    '''termino : factor'''
    p[0] = term_factor(p[1])

def p_factor_num_entero(p):
    '''factor : LITERAL_ENTERO'''
    p[0] = factor_num_entero(p[1])

def p_factor_num_decimal(p):
    '''factor : LITERAL_DECIMAL'''
    p[0] = factor_num_decimal(p[1])

def p_factor_variable(p):
    '''factor : VARIABLE'''
    p[0] = factor_variable(p[1])

    nombreVariable=p[1]
    global listaVariablesInicializadas

    if not (nombreVariable in listaVariablesInicializadas):
        yacc.yacc.erroresSemanticosDetectados.append(f"ERROR SEMANTICO, VARIABLE UTILIZADA EN LINEA {p.lineno(1)} SIN HABERSE INICIALIZADO PREVIAMENTE.")
        yacc.yacc.numErroresSemanticos += 1

def p_factor_expresion_color(p):
    '''factor : expresion_color'''
    p[0] = factor_expresion_color(p[1])

def p_factor_parentesis(p):
    '''factor : PARENTESIS_IZDA expresion PARENTESIS_DCHA'''
    p[0] = factor_parentesis(p[2])

def p_factor_num_entero_negativo(p):
    '''factor : MENOS LITERAL_ENTERO'''
    p[0] = factor_num_entero_negativo(p[2])

# <movimiento> ::= AV <expresion> | AVANZA <expresion> | RE <expresion> | RETROCEDE <expresion>
def p_movimiento_avanza(p):
    '''movimiento : AVANZA expresion'''
    p[0] = movimiento_avanza(p[2])

def p_movimiento_retrocede(p):
    '''movimiento : RETROCEDE expresion'''
    p[0] = movimiento_retrocede(p[2])

# <giro> ::= GIRA_DERECHA <expresion> | GIRA_IZQUIERDA <expresion> | CABECEA_ARRIBA <expresion> | CABECEA_ABAJO" <expresion> | DERIVADERECHA <expresion> | DERIVAIZQUIERDA" <expresion>
def p_giro_dcha(p):
    '''giro : GIRADERECHA expresion'''
    p[0] = giro_dcha(p[2])

def p_giro_izda(p):
    '''giro : GIRAZQUIERDA expresion'''
    p[0] = giro_izda(p[2])

def p_giro_arriba(p):
    '''giro : CABECEAARRIBA expresion'''
    p[0] = giro_arriba(p[2])

def p_giro_abajo(p):
    '''giro : CABECEAABAJO expresion'''
    p[0] = giro_abajo(p[2])

def p_giro_deriva_dcha(p):
    '''giro : DERIVADERECHA expresion'''
    p[0] = giro_deriva_dcha(p[2])

def p_giro_deriva_izda(p):
    '''giro : DERIVAIZQUIERDA expresion'''
    p[0] = giro_deriva_izda(p[2])

def p_cambiocolor_lapiz(p):
    '''cambiocolorlapiz : COLORLAPIZ expresion_color'''
    p[0] = cambiocolor_lapiz(p[1], p[2])

def p_cambiocolor_fondo(p):
    '''cambiocolorfondo : COLORFONDO expresion_color'''
    p[0] = cambiocolor_fondo(p[1], p[2])

# <expresion_color> ::= <color_basico> | [ <componente-color> <componente-color> <componente-color> ] | variable
# <color_basico> ::= NEGRO | AZUL | VERDE | AZULCLARO | ROJO | ROSA | AMARILLO | BLANCO | CAFE | CAFECLARO | VERDEMEDIO | VERDEAZUL | SALMON | LILA | NARANJA | GRIS 
# componente-color ::= <numero entero entre 0 y 255>

def p_expresion_color_basico(p):
    '''expresion_color : COLOR'''
    p[0] = expresion_color(p[1])
 
def p_expresion_color_componentes(p):
    '''expresion_color : CORCHETE_IZDA componente_color COMA componente_color COMA componente_color CORCHETE_DCHA'''    
    p[0] = expresion_color_componentes(p[2], p[4], p[6])

    if not (0<=p[2].valor<=255):        
        yacc.yacc.erroresSemanticosDetectados.append(f"ERROR SEMANTICO, COMPONENTE DE COLOR ROJO NO VALIDA: {p[2].valor} EN LINEA {p.lineno(2)}")
        yacc.yacc.numErroresSemanticos += 1

    if not (0<=p[4].valor<=255):        
        yacc.yacc.erroresSemanticosDetectados.append(f"ERROR SEMANTICO, COMPONENTE DE COLOR VERDE NO VALIDA: {p[4].valor} EN LINEA {p.lineno(4)}")
        yacc.yacc.numErroresSemanticos += 1

    if not (0<=p[6].valor<=255):        
        yacc.yacc.erroresSemanticosDetectados.append(f"ERROR SEMANTICO, COMPONENTE DE COLOR AZUL NO VALIDA: {p[6].valor} EN LINEA {p.lineno(6)}") 
        yacc.yacc.numErroresSemanticos += 1
        
def p_expresion_color_variable(p):
    '''expresion_color : VARIABLE'''
    p[0] = expresion_color_variable(p[1])

def p_expresion_color_expresion(p):
    '''componente_color : expresion'''
    p[0] = expresion_color_expresion(p[1])

def p_bucle(p):
    '''bucle : REPITE expresion CORCHETE_IZDA instrucciones CORCHETE_DCHA'''
    p[0] = bucle(p[2], p[4])

    if (p[2].valor<0):        
        yacc.yacc.erroresSemanticosDetectados.append(f"ERROR SEMANTICO, BUCLE CON CONTADOR NEGATIVO EN LINEA {p.lineno(2)}")
        yacc.yacc.numErroresSemanticos += 1

def p_llamada_funcion(p):
    '''llamada_funcion : CALL IDENTIFICADOR argumentos'''
    p[0] = llamada_funcion(p[2], p[3])

# <argumentos> ::= ( <lista_argumentos> ) | e
# <lista_argumentos> ::= expresion | expresion COMA <lista_argumentos>
def p_argumentos_lista(p):
    '''argumentos : PARENTESIS_IZDA lista_argumentos PARENTESIS_DCHA'''
    p[0] = argumentos_lista(p[2])

def p_argumentos_empty(p):
    '''argumentos : empty'''
    p[0] = argumentos_empty()

def p_lista_argumentos_uno(p):
    '''lista_argumentos : expresion'''
    p[0] = lista_argumentos_uno(p[1])

def p_lista_argumentos_varios(p):
    '''lista_argumentos : expresion COMA lista_argumentos'''
    p[0] = lista_argumentos_varios(p[1], p[3])

def p_asignacion(p):
    '''asignacion : VARIABLE IGUAL expresion'''
    p[0] = asignacion(p[1], p[3])

    nombreVariable=p[1]

    global listaVariablesInicializadas
    listaVariablesInicializadas.add(nombreVariable)
    
def p_empty(p):
    '''empty :'''
    p[0] = empty()

def p_error(p):    
    if p:
        yacc.yacc.erroresSintacticosDetectados.append(f"ERROR SINTACTICO AL LEER EL ELEMENTO '{p.value}' ({p.type}) EN LA LINEA {p.lineno}")        
    else:
        yacc.yacc.erroresSintacticosDetectados.append("ERROR. SE HA ALCANZADO EL FINAL DE FICHERO ANTES DE TIEMPO")        
    yacc.yacc.numErroresSintacticos += 1


# INICIALIZAMOS NUESTRO ANALIZADOR SINTACTICO
parser = yacc.yacc("LALR")

yacc.yacc.numErroresSintacticos = 0
yacc.yacc.erroresSintacticosDetectados = []

yacc.yacc.numErroresSemanticos = 0
yacc.yacc.erroresSemanticosDetectados = []
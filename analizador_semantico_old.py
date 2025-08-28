import ply.yacc as yacc
from os import remove, path
import generador

# DEFINIMOS TODAS LAS CLASES QUE CORREPONDEN A CADA UNO DE LAS PRODUCCIONES
# CLASE DE LA QUE HEREDAN TODAS

COLOR_BASICO_NEGRO = [0,0,0]
COLOR_BASICO_AZUL = [0,0,1]
COLOR_BASICO_VERDE = [0,1,0]
COLOR_BASICO_AZULCLARO = [0,1,1]
COLOR_BASICO_ROJO = [1,0,0]
COLOR_BASICO_ROSA = [1,0,1]
COLOR_BASICO_AMARILLO = [1,1,0]
COLOR_BASICO_BLANCO= [1,1,1]
COLOR_BASICO_CAFE = [128/255,0,0]
COLOR_BASICO_CAFECLARO = [128/255,64/255,0]
COLOR_BASICO_VERDEMEDIO = [0,128/255,0]
COLOR_BASICO_VERDEAZUL = [0,128/255,128/255]
COLOR_BASICO_SALMON = [128/255,0,128/255]
COLOR_BASICO_LILA = [0,0,128/255]
COLOR_BASICO_NARANJA = [26/255,127/255,239/255]
COLOR_BASICO_GRIS = [192/255,192/255,192/255]

class base():

    def __init__(self):
        pass

    def generar(self, tabulaciones, contenido):                        
        try:            
            #print(contenido, end=" ")

            with open (generador.destino,"at") as fichero: 
                if tabulaciones > 0:
                    for _ in range(tabulaciones):
                        fichero.write("\t")                    
                fichero.write(f"{contenido}")
        except:
            print(tabulaciones)
            print(f"SE HA PRODUCIDO UN ERROR AL INTENTAR ESCRIBIR {contenido} EN EL FICHERO {generador.destino}.")
        

    def obtener(self, tabulaciones, contenido):                        
        aux=""
        if tabulaciones > 0:
            for _ in range(tabulaciones):
                aux += "\t"
        aux+=f"{contenido}"
        return aux




class programa(base):
    def __init__(self, nombre, bloque):
        self.nombre = nombre
        generador.nombreAplicacion=nombre

        self.bloque = bloque
        pass        

    def generar(self, tabulaciones):   

        #Generamos el código previo a nuestro programa. Incluye los requires, clases, constantes y funciones necesarias
        super().generar(tabulaciones, generador.generarCodigoPrevio())        

        #Generamos la funcion que hace el programa que estamos compilando
        self.bloque.generar(tabulaciones)

        #Generamos el final del programa
        super().generar(tabulaciones, generador.generarCodigoPosterior())
               


class bloque(base):
    def __init__(self, declaracion_funciones, instrucciones):
        self.declaracion_funciones = declaracion_funciones
        self.instrucciones = instrucciones
        
    def generar(self, tabulaciones):
        self.declaracion_funciones.generar(tabulaciones)
        super().generar(tabulaciones,f"\n")
        super().generar(tabulaciones,f"def programa():\n")
        self.instrucciones.generar(tabulaciones+1)
        

class declaracion_funciones(base):
    def __init__(self, declaracion_funcion=None, declaracion_funciones=None):
        self.declaracion_funcion = declaracion_funcion
        self.declaracion_funciones = declaracion_funciones

    def generar(self, tabulaciones):
        self.declaracion_funcion.generar(tabulaciones)
        self.declaracion_funciones.generar(tabulaciones)

class declaracion_funciones_empty(base):
    def __init__(self):
        pass

    def generar(self, tabulaciones):
        pass

class declaracion_funcion(base):
    def __init__(self, identificador,  parametros, instrucciones):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        super().generar(tabulaciones,f"def fun_{self.identificador.lower()}(")
        if self.parametros != None:            
            self.parametros.generar(0)
        super().generar(0,f"):\n")        
        self.instrucciones.generar(tabulaciones+1)
        

class parametros(base):
    def __init__(self, lista_parametros):
        self.lista_parametros = lista_parametros

    def generar(self, tabulaciones):        
        self.lista_parametros.generar(tabulaciones)
        

class parametros_empty(base):
    def __init__(self):        
        pass

    def generar(self, tabulaciones):
        pass

class lista_parametros_uno(base):
    def __init__(self, variable):
        self.variable = variable

    def generar(self, tabulaciones):
        super().generar(tabulaciones, f"var_{self.variable.lower()}")

class lista_parametros_varios(base):
    def __init__(self, variable, lista_parametros):
        self.variable = variable
        self.lista_parametros = lista_parametros

    def generar(self, tabulaciones):
        super().generar(tabulaciones, f"var_{self.variable.lower()}, ")                
        self.lista_parametros.generar(0)
 

class instrucciones_empty(base):
    def __init__(self):
        pass

    def generar(self, tabulaciones):
        pass

class instrucciones(base):
    def __init__(self, instruccion, instrucciones):
        self.instruccion = instruccion
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        self.instruccion.generar(tabulaciones)
        self.instrucciones.generar(tabulaciones)

class instruccion_perspectiva(base):
    def __init__(self, perspectiva, instrucciones):
        self.perspectiva = perspectiva
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        if(self.perspectiva =="VISTA_ARRIBA"):
            super().generar(tabulaciones, "proyeccion(proyecciones.arriba)\n")
        elif(self.perspectiva =="VISTA_ABAJO"):
            super().generar(tabulaciones, "proyeccion(proyecciones.abajo)\n")
        elif(self.perspectiva =="VISTA_DERECHA"):
            super().generar(tabulaciones, "proyeccion(proyecciones.derecha)\n")
        elif(self.perspectiva =="VISTA_IZQUIERDA"):
            super().generar(tabulaciones, "proyeccion(proyecciones.izquierda)\n")
        elif(self.perspectiva =="VISTA_ANTERIOR"):
            super().generar(tabulaciones, "proyeccion(proyecciones.delantera)\n")
        elif(self.perspectiva =="VISTA_POSTERIOR"):
            super().generar(tabulaciones, "proyeccion(proyecciones.trasera)\n")
        elif(self.perspectiva =="VISTA_GABINETE"):
            super().generar(tabulaciones, "proyeccion(proyecciones.gabinete)\n")
        elif(self.perspectiva =="VISTA_PERSPECTIVA"):
            super().generar(tabulaciones, "proyeccion(proyecciones.isometrica)\n")
        self.instrucciones.generar(tabulaciones)

class instruccion_movimiento(base):
    def __init__(self, movimiento, instrucciones):
        self.movimiento = movimiento
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        self.movimiento.generar(tabulaciones)
        self.instrucciones.generar(tabulaciones)

class instruccion_giro(base):
    def __init__(self, giro, instrucciones):
        self.giro = giro
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        self.giro.generar(tabulaciones)
        self.instrucciones.generar(tabulaciones)

class instruccion_cambiocolorlapiz(base):
    def __init__(self, cambiocolorlapiz, instrucciones):
        self.cambiocolorlapiz = cambiocolorlapiz
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):        
        self.cambiocolorlapiz.generar(tabulaciones)
        self.instrucciones.generar(tabulaciones)

class instruccion_cambiocolorfondo(base):
    def __init__(self, cambiocolorfondo, instrucciones):
        self.cambiocolorfondo = cambiocolorfondo
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        self.cambiocolorfondo.generar(tabulaciones)
        self.instrucciones.generar(tabulaciones)

class instruccion_bucle(base):
    def __init__(self, bucle, instrucciones):
        self.bucle = bucle
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        self.bucle.generar(tabulaciones)
        self.instrucciones.generar(tabulaciones)


class instruccion_goma(base):
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        '''
        super().generar(tabulaciones, f"glColor3f({generador.colorFondo[0]}/255, {generador.colorFondo[1]}/255, {generador.colorFondo[2]}/255)\n")


        if type(self.expresion)==expresion_color_componentes:            
            super().generar(tabulaciones, f"glColor3f({generador.colorFondo[0]}/255, {generador.colorFondo[1]}/255, {generador.colorFondo[2]}/255)\n")
        else:            
            super().generar(tabulaciones, f"glColor3fv({generador.colorFondo[0]}, {generador.colorFondo[1]}, {generador.colorFondo[2]})\n")
        '''

        super().generar(tabulaciones, f"glColor3fv({generador.colorFondo})\n")


        self.instrucciones.generar(tabulaciones)

class instruccion_centro(base):
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "glLoadIdentity()\n")
        self.instrucciones.generar(tabulaciones)

class instruccion_subelapiz(base):
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):        
        super().generar(tabulaciones, "subeLapiz()\n")        
        self.instrucciones.generar(tabulaciones)

class instruccion_bajalapiz(base):
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "bajaLapiz()\n")        
        self.instrucciones.generar(tabulaciones)

class instruccion_asignacion(base):
    def __init__(self, asignacion, instrucciones):
        self.asignacion = asignacion
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        self.asignacion.generar(tabulaciones)
        self.instrucciones.generar(tabulaciones)

class instruccion_call(base):
    def __init__(self, llamada_funcion, instrucciones):
        self.llamada_funcion = llamada_funcion
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        self.llamada_funcion.generar(tabulaciones)
        self.instrucciones.generar(tabulaciones)

class expression_plus(base):
    def __init__(self, expresion, termino):
        self.expresion = expresion
        self.termino = termino
        self.valor = expresion.valor + termino.valor

    def generar(self, tabulaciones):        
        self.expresion.generar(tabulaciones)
        super().generar(0, "+")        
        self.termino.generar(0)
        

class expression_minus(base):
    def __init__(self, expresion, termino):
        self.expresion = expresion
        self.termino = termino
        self.valor = expresion.valor - termino.valor

    def generar(self, tabulaciones):        
        self.expresion.generar(tabulaciones)    
        super().generar(0, "-")        
        self.termino.generar(0)
        


class expresion_termino(base):
    def __init__(self, termino):
        self.termino = termino        
        self.valor = termino.valor
        
    def generar(self, tabulaciones):
        self.termino.generar(tabulaciones)


class term_multiplicar(base):
    def __init__(self, termino, factor):
        self.termino = termino
        self.factor = factor
        self.valor = termino.valor * factor.valor

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "(")
        self.termino.generar(0)        
        super().generar(0, "*")    
        self.factor.generar(0)
        super().generar(0, ")")

class term_dividir(base):
    def __init__(self, termino, factor):
        self.termino = termino
        self.factor = factor
        self.valor = termino.valor / factor.valor

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "(")
        self.termino.generar(0)        
        super().generar(0, "/")    
        self.factor.generar(0)
        super().generar(0, ")")

class term_factor(base):
    def __init__(self, factor):
        self.factor = factor
        self.valor = factor.valor

    def generar(self, tabulaciones):
        self.factor.generar(tabulaciones)

class factor_num_entero(base):
    def __init__(self, entero):
        self.entero = int(entero)
        self.valor=int(entero)

    def generar(self, tabulaciones):
        super().generar(tabulaciones, self.entero)

class factor_num_decimal(base):
    def __init__(self, decimal):
        self.decimal = decimal
        self.valor=decimal

    def generar(self, tabulaciones):
        super().generar(tabulaciones, self.decimal)

class factor_variable(base):
    def __init__(self, variable):
        self.variable = variable        
        self.valor = 0

    def generar(self, tabulaciones):
        super().generar(tabulaciones, f"var_{self.variable.lower()}")

class factor_expresion_color(base):
    def __init__(self, expresion_color):
        self.expresion_color = expresion_color
        self.valor = expresion_color.valor

    def generar(self, tabulaciones):
        self.expresion_color.generar(tabulaciones) 

class factor_expresion_color_variable(base):
    def __init__(self, expresion_color):
        self.expresion_color = expresion_color
        self.valor = expresion_color.valor

    def generar(self, tabulaciones):
        self.expresion_color.generar(tabulaciones) 


class factor_parentesis(base):
    def __init__(self, expresion):
        self.expresion = expresion    
        self.valor = expresion.valor    

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "(")
        self.expresion.generar(0)
        super().generar(0, ")")

class movimiento_avanza(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "avanza(")
        self.expresion.generar(0)
        super().generar(0, ")\n")
        

class movimiento_retrocede(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "avanza(-")
        self.expresion.generar(0)
        super().generar(0, ")\n")        
        

class giro_dcha(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "glRotate(")
        self.expresion.generar(0)
        super().generar(0, ",0, 0, -1)\n")   

class giro_izda(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "glRotate(")
        self.expresion.generar(0)
        super().generar(0, ", 0, 0, 1)\n")   

class giro_arriba(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "glRotate(")
        self.expresion.generar(0)
        super().generar(0, ", 1, 0, 0)\n")   

class giro_abajo(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        super().generar(tabulaciones, "glRotate(")
        self.expresion.generar(0)
        super().generar(0, ", -1, 0, 0)\n")   

class cambiocolor_lapiz(base):
    def __init__(self, colorlapiz, expresion):
        self.colorlapiz = colorlapiz
        self.expresion = expresion

    def generar(self, tabulaciones):  
        
        if type(self.expresion)==expresion_color_componentes:
            super().generar(tabulaciones, "glColor3f(")
        else:
            super().generar(tabulaciones, "glColor3fv(")
        
        self.expresion.generar(0)
        super().generar(0, ")\n")   

class cambiocolor_fondo(base):
    def __init__(self, colorfondo, expresion):
        self.colorfondo = colorfondo
        self.expresion = expresion
        #independiente de las veces que establezcamos un color de fondo se establecerá la última        
        #utiles.establecerColorFondo(expresion.valor)
        generador.colorFondo=expresion.valor
        

    def generar(self, tabulaciones):
        # no genera codigo 
        return

class expresion_color(base):
    def __init__(self, expresioncolor):
        self.expresioncolor = expresioncolor
        self.valor =  eval(f"COLOR_BASICO_{self.expresioncolor}")

    def generar(self, tabulaciones):
        super().generar(tabulaciones, f"COLOR_BASICO_{self.expresioncolor}")
        

class expresion_color_variable(base):
    def __init__(self, expresion_color_variable):
        self.expresioncolor = expresion_color_variable
        self.valor=expresion_color_variable

    def generar(self, tabulaciones):
        super().generar(tabulaciones, f"var_{self.expresioncolor.lower()}")




class expresion_color_componentes(base):
    def __init__(self, componente_color_rojo, componente_color_verde, componente_color_azul):
        self.componente_color_rojo = componente_color_rojo
        self.componente_color_verde = componente_color_verde
        self.componente_color_azul = componente_color_azul
        self.valor = [self.componente_color_rojo.valor, self.componente_color_verde.valor, self.componente_color_azul.valor]
        

    def generar(self, tabulaciones):        
        self.componente_color_rojo.generar(0)
        super().generar(0, "/255, ")
        self.componente_color_verde.generar(0)
        super().generar(0, "/255, ")
        self.componente_color_azul.generar(0)
        super().generar(0, "/255")

class expresion_color_expresion(base):
    def __init__(self, expresion):
        self.expresion = expresion
        self.valor= expresion.valor

    def generar(self, tabulaciones):
        self.expresion.generar(tabulaciones)



class bucle(base):
    def __init__(self, expresion, instrucciones):
        self.expresion = expresion
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        super().generar(tabulaciones, f"for _ in range(")
        self.expresion.generar(0)
        super().generar(0,"):\n")
        self.instrucciones.generar(tabulaciones+1)
        super().generar(tabulaciones, "\n")        

class llamada_funcion(base):
    def __init__(self, identificador, parametros):
        self.identificador = identificador
        self.parametros = parametros

    def generar(self, tabulaciones):
        super().generar(tabulaciones, f"fun_{self.identificador.lower()}(")
        self.parametros.generar(0)
        super().generar(0, ")\n")

class argumentos_lista(base):
    def __init__(self, lista_argumentos):
        self.lista_argumentos = lista_argumentos

    def generar(self, tabulaciones):        
        self.lista_argumentos.generar(tabulaciones)
    

class argumentos_empty(base):
    def __init__(self):
        pass

    def generar(self, tabulaciones):
        pass

class lista_argumentos_uno(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        self.expresion.generar(tabulaciones)

class lista_argumentos_varios(base):
    def __init__(self, expresion, lista_argumentos):
        self.expresion = expresion
        self.lista_argumentos = lista_argumentos

    def generar(self, tabulaciones):
        self.expresion.generar(tabulaciones)
        super().generar(tabulaciones, ",")
        self.lista_argumentos.generar(tabulaciones)

class asignacion(base):
    def __init__(self, variable, expresion):

        self.variable = variable
        self.expresion = expresion

    def generar(self, tabulaciones):
        super().generar(tabulaciones, f"var_{self.variable.lower()} = ")        
        self.expresion.generar(0)
        super().generar(0, "\n")        

class empty(base):
    def __init__(self):        
        pass

    def generar(self, tabulaciones):
        pass





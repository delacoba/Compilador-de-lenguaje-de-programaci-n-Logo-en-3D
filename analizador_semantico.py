import ply.yacc as yacc
from generador import componentes_colores

from os import remove, path
import generador

# DEFINIMOS TODAS LAS CLASES QUE CORREPONDEN A CADA UNO DE LAS PRODUCCIONES
# TODAS ELLAS HEREDAN DE LA CLASE BASE.
# EL METODO INIT SE ENCARGARÁ DE CONSTRUIR EL ARBOL SEMANTICO, MIENTRAS QUE 
# EL METODO GENERAR SE ENCARGARÁ DE PRODUCIR EL CÓDIGO CORRESPONDIENTE

class base():

    def __init__(self):
        pass

    def generar(self, tabulaciones, contenido):                        
        aux=""
        if tabulaciones > 0:
            for _ in range(tabulaciones):
                aux +="\t"
        aux += f"{contenido}"
        return aux
        


class programa(base):
    def __init__(self, nombre, bloque):
        self.nombre = nombre
        generador.nombreAplicacion=nombre

        self.bloque = bloque
        pass        

    def generar(self, tabulaciones):   
        aux=""

        #Generamos el código previo a nuestro programa. Incluye los imports, clases, constantes y funciones necesarias
        aux += super().generar(tabulaciones, generador.generarCodigoPrevio())                  

        #Generamos la funcion que hace el programa que estamos compilando
        aux += self.bloque.generar(tabulaciones)

        #Generamos el final del programa
        aux += super().generar(tabulaciones, generador.generarCodigoPosterior())

        return aux
               


class bloque(base):
    def __init__(self, declaracion_funciones, instrucciones):
        self.declaracion_funciones = declaracion_funciones
        self.instrucciones = instrucciones
        
    def generar(self, tabulaciones):
        aux=self.declaracion_funciones.generar(tabulaciones)
        aux +=super().generar(tabulaciones,f"\n")
        aux +=super().generar(tabulaciones,f"def programa():\n")
        aux +=self.instrucciones.generar(tabulaciones+1)
        return aux

class declaracion_funciones(base):
    def __init__(self, declaracion_funcion=None, declaracion_funciones=None):
        self.declaracion_funcion = declaracion_funcion
        self.declaracion_funciones = declaracion_funciones

    def generar(self, tabulaciones):
        aux=self.declaracion_funcion.generar(tabulaciones)
        aux +=self.declaracion_funciones.generar(tabulaciones)
        return aux

class declaracion_funciones_empty(base):
    def __init__(self):
        pass

    def generar(self, tabulaciones):
        return ""        

class declaracion_funcion(base):
    def __init__(self, identificador,  parametros, instrucciones):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones,f"def fun_{self.identificador.lower()}(")
        if self.parametros != None:            
            aux+=self.parametros.generar(0)
        aux+=super().generar(0,f"):\n")        
        aux+=self.instrucciones.generar(tabulaciones+1)
        return aux

class parametros(base):
    def __init__(self, lista_parametros):
        self.lista_parametros = lista_parametros

    def generar(self, tabulaciones):        
        return self.lista_parametros.generar(tabulaciones)
        

class parametros_empty(base):
    def __init__(self):        
        pass

    def generar(self, tabulaciones):
        return ""

class lista_parametros_uno(base):
    def __init__(self, variable):
        self.variable = variable

    def generar(self, tabulaciones):
        return super().generar(tabulaciones, f"var_{self.variable.lower()}")

class lista_parametros_varios(base):
    def __init__(self, variable, lista_parametros):
        self.variable = variable
        self.lista_parametros = lista_parametros

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, f"var_{self.variable.lower()}, ")                
        aux+=self.lista_parametros.generar(0)
        return aux
 

class instrucciones_empty(base):
    def __init__(self):
        pass

    def generar(self, tabulaciones):
        return ""

class instrucciones(base):
    def __init__(self, instruccion, instrucciones):
        self.instruccion = instruccion
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        aux=self.instruccion.generar(tabulaciones)
        aux+=self.instrucciones.generar(tabulaciones)
        return aux

class instruccion_perspectiva(base):
    def __init__(self, perspectiva):
        self.perspectiva = perspectiva        

    def generar(self, tabulaciones):                
        if(self.perspectiva =="VISTA_ANTERIOR"):
            generador.tipoProyeccion=0            
        elif(self.perspectiva =="VISTA_POSTERIOR"):
            generador.tipoProyeccion=1                    
        elif(self.perspectiva =="VISTA_ARRIBA"):
            generador.tipoProyeccion=2
        elif(self.perspectiva =="VISTA_ABAJO"):
            generador.tipoProyeccion=3                    
        elif(self.perspectiva =="VISTA_DERECHA"):
            generador.tipoProyeccion=4            
        elif(self.perspectiva =="VISTA_IZQUIERDA"):
            generador.tipoProyeccion=5                                
        elif(self.perspectiva =="VISTA_GABINETE"):
            generador.tipoProyeccion=6                                
        else: # self.perspectiva =="VISTA_PERSPECTIVA"
            generador.tipoProyeccion=7     

        return ""                           
        
    
class instruccion_movimiento(base):
    def __init__(self, movimiento):
        self.movimiento = movimiento        

    def generar(self, tabulaciones):
        return self.movimiento.generar(tabulaciones)        

class instruccion_giro(base):
    def __init__(self, giro):
        self.giro = giro
        
    def generar(self, tabulaciones):
        return self.giro.generar(tabulaciones)
        

class instruccion_cambiocolorlapiz(base):
    def __init__(self, cambiocolorlapiz):
        self.cambiocolorlapiz = cambiocolorlapiz
        
    def generar(self, tabulaciones):        
        return self.cambiocolorlapiz.generar(tabulaciones)
        
    
class instruccion_cambiocolorfondo(base):
    def __init__(self, cambiocolorfondo):
        self.cambiocolorfondo = cambiocolorfondo

    def generar(self, tabulaciones):
        return self.cambiocolorfondo.generar(tabulaciones)

class instruccion_bucle(base):
    def __init__(self, bucle):
        self.bucle = bucle        

    def generar(self, tabulaciones):
        return self.bucle.generar(tabulaciones)
        


class instruccion_goma(base):
    def __init__(self):
        pass        

    def generar(self, tabulaciones):        
        return super().generar(tabulaciones, f"glColor3fv({generador.colorFondo})\n")
        

        
class instruccion_centro(base):
    def __init__(self):
        pass
        

    def generar(self, tabulaciones):
        return super().generar(tabulaciones, "glLoadIdentity()\n")
        
class instruccion_subelapiz(base):
    def __init__(self):
        pass
        

    def generar(self, tabulaciones):        
        return super().generar(tabulaciones, "subeLapiz()\n")        
        

class instruccion_bajalapiz(base):
    def __init__(self):
        pass

    def generar(self, tabulaciones):
        return super().generar(tabulaciones, "bajaLapiz()\n")        
        

class instruccion_asignacion(base):
    def __init__(self, asignacion):
        self.asignacion = asignacion
        

    def generar(self, tabulaciones):
        return self.asignacion.generar(tabulaciones)
        

class instruccion_call(base):
    def __init__(self, llamada_funcion):
        self.llamada_funcion = llamada_funcion        

    def generar(self, tabulaciones):
        return self.llamada_funcion.generar(tabulaciones)
        

class expression_plus(base):
    def __init__(self, expresion, termino):
        self.expresion = expresion
        self.termino = termino
        self.valor = expresion.valor + termino.valor

    def generar(self, tabulaciones):        
        aux=self.expresion.generar(tabulaciones)
        aux+=super().generar(0, "+")        
        aux+=self.termino.generar(0)
        return aux
        

class expression_minus(base):
    def __init__(self, expresion, termino):
        self.expresion = expresion
        self.termino = termino
        self.valor = expresion.valor - termino.valor

    def generar(self, tabulaciones):        
        aux=self.expresion.generar(tabulaciones)    
        aux+=super().generar(0, "-")        
        aux+=self.termino.generar(0)
        return aux
        

class expresion_termino(base):
    def __init__(self, termino):
        self.termino = termino        
        self.valor = termino.valor
        
    def generar(self, tabulaciones):
        return self.termino.generar(tabulaciones)


class term_multiplicar(base):
    def __init__(self, termino, factor):
        self.termino = termino
        self.factor = factor
        self.valor = termino.valor * factor.valor

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "(")
        aux+=self.termino.generar(0)        
        aux+=super().generar(0, "*")    
        aux+=self.factor.generar(0)
        aux+=super().generar(0, ")")
        return aux

class term_dividir(base):
    def __init__(self, termino, factor):
        self.termino = termino
        self.factor = factor
        self.valor = termino.valor / factor.valor

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "(")
        aux+=self.termino.generar(0)        
        aux+=super().generar(0, "/")    
        aux+=self.factor.generar(0)
        aux+=super().generar(0, ")")
        return aux

class term_factor(base):
    def __init__(self, factor):
        self.factor = factor
        self.valor = factor.valor

    def generar(self, tabulaciones):
        return self.factor.generar(tabulaciones)

class factor_num_entero(base):
    def __init__(self, entero):
        self.entero = int(entero)
        self.valor=int(entero)

    def generar(self, tabulaciones):
        return super().generar(tabulaciones, self.entero)


class factor_num_entero_negativo(base):
    def __init__(self, entero):
        self.entero = - int(entero)
        self.valor= - int(entero)

    def generar(self, tabulaciones):
        return super().generar(tabulaciones, self.entero)





class factor_num_decimal(base):
    def __init__(self, decimal):
        self.decimal = decimal
        self.valor=decimal

    def generar(self, tabulaciones):
        return super().generar(tabulaciones, self.decimal)

class factor_variable(base):
    def __init__(self, variable):
        self.variable = variable        
        self.valor = 0

    def generar(self, tabulaciones):
        return super().generar(tabulaciones, f"var_{self.variable.lower()}")

class factor_expresion_color(base):
    def __init__(self, expresion_color):
        self.expresion_color = expresion_color
        self.valor = expresion_color.valor

    def generar(self, tabulaciones):
        return self.expresion_color.generar(tabulaciones) 


class factor_parentesis(base):
    def __init__(self, expresion):
        self.expresion = expresion    
        self.valor = expresion.valor    

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "(")
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, ")")
        return aux

class movimiento_avanza(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "avanza(")
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, ")\n")
        return aux
        

class movimiento_retrocede(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "avanza(-")
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, ")\n")        
        return aux
        

class giro_dcha(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "glRotate(")
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, ",0, 0, -1)\n")   
        return aux

class giro_izda(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "glRotate(")
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, ", 0, 0, 1)\n")   
        return aux

class giro_arriba(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "glRotate(")
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, ", 1, 0, 0)\n")   
        return aux

class giro_abajo(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "glRotate(")
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, ", -1, 0, 0)\n")   
        return aux


class giro_deriva_dcha(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "glRotate(")
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, ", 0, 1, 0)\n")   
        return aux




class giro_deriva_izda(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, "glRotate(")
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, ", 0, -1, 0)\n")   
        return aux







class cambiocolor_lapiz(base):
    def __init__(self, colorlapiz, expresion):
        self.colorlapiz = colorlapiz
        self.expresion = expresion

    def generar(self, tabulaciones):  
        
        if type(self.expresion)==expresion_color_componentes:
            aux=super().generar(tabulaciones, "glColor3f(")
        else:
            aux=super().generar(tabulaciones, "glColor3fv(")
        
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, ")\n")   
        return aux

class cambiocolor_fondo(base):
    def __init__(self, colorfondo, expresion):
        self.colorfondo = colorfondo
        self.expresion = expresion
        #independiente de las veces que establezcamos un color de fondo se establecerá la última               
        generador.colorFondo=expresion.valor


    def generar(self, tabulaciones):
        return "" # no genera codigo ya que se cambie el color del fondo solo 1 vez por programa
        

class expresion_color(base):
    def __init__(self, expresioncolor):
        self.expresioncolor = expresioncolor
        self.valor = componentes_colores[self.expresioncolor]

    def generar(self, tabulaciones):
        return super().generar(tabulaciones, f"COLOR_BASICO_{self.expresioncolor}")
        

class expresion_color_variable(base):
    def __init__(self, expresion_color_variable):
        self.expresioncolor = expresion_color_variable
        self.valor=expresion_color_variable

    def generar(self, tabulaciones):
        return super().generar(tabulaciones, f"var_{self.expresioncolor.lower()}")


class expresion_color_componentes(base):
    def __init__(self, componente_color_rojo, componente_color_verde, componente_color_azul):
        self.componente_color_rojo = componente_color_rojo
        self.componente_color_verde = componente_color_verde
        self.componente_color_azul = componente_color_azul
        self.valor = [self.componente_color_rojo.valor/255, self.componente_color_verde.valor/255, self.componente_color_azul.valor/255]        

    def generar(self, tabulaciones):        
        aux=self.componente_color_rojo.generar(0)
        aux+=super().generar(0, "/255, ")
        aux+=self.componente_color_verde.generar(0)
        aux+=super().generar(0, "/255, ")
        aux+=self.componente_color_azul.generar(0)
        aux+=super().generar(0, "/255")
        return aux

class expresion_color_expresion(base):
    def __init__(self, expresion):
        self.expresion = expresion
        self.valor= expresion.valor

    def generar(self, tabulaciones):
        return self.expresion.generar(tabulaciones)



class bucle(base):
    def __init__(self, expresion, instrucciones):
        self.expresion = expresion
        self.instrucciones = instrucciones

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, f"for _ in range(")
        aux+=self.expresion.generar(0)
        aux+=super().generar(0,"):\n")
        aux+=self.instrucciones.generar(tabulaciones+1)
        aux+=super().generar(tabulaciones, "\n")        
        return aux

class llamada_funcion(base):
    def __init__(self, identificador, parametros):
        self.identificador = identificador
        self.parametros = parametros

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, f"fun_{self.identificador.lower()}(")
        aux+=self.parametros.generar(0)
        aux+=super().generar(0, ")\n")
        return aux

class argumentos_lista(base):
    def __init__(self, lista_argumentos):
        self.lista_argumentos = lista_argumentos

    def generar(self, tabulaciones):        
        return self.lista_argumentos.generar(tabulaciones)
    

class argumentos_empty(base):
    def __init__(self):
        pass

    def generar(self, tabulaciones):
        return ""

class lista_argumentos_uno(base):
    def __init__(self, expresion):
        self.expresion = expresion

    def generar(self, tabulaciones):
        return self.expresion.generar(tabulaciones)

class lista_argumentos_varios(base):
    def __init__(self, expresion, lista_argumentos):
        self.expresion = expresion
        self.lista_argumentos = lista_argumentos

    def generar(self, tabulaciones):
        aux=self.expresion.generar(tabulaciones)
        aux+=super().generar(tabulaciones, ",")
        aux+=self.lista_argumentos.generar(tabulaciones)
        return aux

class asignacion(base):
    def __init__(self, variable, expresion):

        self.variable = variable
        self.expresion = expresion

    def generar(self, tabulaciones):
        aux=super().generar(tabulaciones, f"var_{self.variable.lower()} = ")        
        aux+=self.expresion.generar(0)
        aux+=super().generar(0, "\n")        
        return aux

class empty(base):
    def __init__(self):        
        pass

    def generar(self, tabulaciones):
        return ""





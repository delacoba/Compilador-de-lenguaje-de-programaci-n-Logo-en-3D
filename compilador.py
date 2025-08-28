import ply.lex as lex
import ply.yacc as yacc
import sys
import os

from analizador_lexico import *
from analizador_sintactico import *
from analizador_semantico import *


def AnalizadorLexico(programa, verLexemas): 
    '''
    Esta función analiza el programa que le pasadmos y devuelve TRUE y lista de tokens obtenidos.
    En caso de error, devuelve FALSE y lista de errores obtenidos.
    '''

    # INICIALIZAMOS NUESTRO ANALIZADOR LEXICO
    analizadorLexico  = lex.lexer

    
    # LE PASAMOS EL PROGRAMA AL ANALIZADOR LEXICO
    analizadorLexico.input(programa)

    # INICIALIZAMOS LAS LISTAS EN LAS QUE ALMACENAMOS LOS TOKENS DETECTADOS    
    resultado=[]

    # VAMOS OBTENIENDO CADA UNO DE LOS TOKEN
    token  = analizadorLexico.token()
    while token:
        resultado.append(token)
        # AUNQUE SE DETECTE UN ERROR, SEGUIMOS ANALIZANDO PARA DETECTAR EL MAXIMO NUMERO DE ERRORES POSIBLES
        token  = analizadorLexico.token()

    # UNA VEZ FINALIZADO EL ANALISIS LEXICO VEMOS EL RESULTADO.
    if(analizadorLexico.numErroresLexicos == 0):
        print("ANALISIS LEXICO CORRECTO.")
        if verLexemas:
            print("TOKENS DETECTADOS:")
            for token in resultado:
                linea=token.lineno
                tipo=token.type
                valor=token.value
                print(f"linea:{linea} <{tipo},{valor}>")  
            print("\n")
    else:
        print("ANALISIS LÉXICO INCORRECTO:")
        for error in analizadorLexico.erroresLexicosDetectados:
            linea=error.lineno             
            texto=error.value[0]
            print(f"SE HA DETECTADO UN CARACTER DESCONOCIDO: {texto} EN LA LINEA: {linea}.")
        print("\n")
    
    # UNA VEZ PROCESADO TODO EL FICHERO DEVOLVEMOS EL RESULTADO
    if(analizadorLexico.numErroresLexicos == 0):
        return True
    else:
        # HEMOS ENCONTRADO ERRORES
        return False
    

    
def AnalizadorSintactico(programa):
    #ES NECESARIO VOLVER A INICIALIZAR EL CONTADOR DE LINEAS.
    lex.lexer.lineno=1   

    resultado = parser.parse(programa, tracking=True)

    if(yacc.yacc.numErroresSintacticos == 0):
        print("ANALISIS SINTACTICO CORRECTO.")        
    else:
        # HEMOS ENCONTRADO ERRORES
        print("ANALISIS SINTACTICO INCORRECTO:")
        for error in yacc.yacc.erroresSintacticosDetectados:
            print(error)
        return False, None

    if(yacc.yacc.numErroresSemanticos == 0):
        print("ANALISIS SEMANTICO CORRECTO.")
        return True, resultado
    else:
        # HEMOS ENCONTRADO ERRORES
        print("ANALISIS SEMANTICO INCORRECTO:")
        for error in yacc.yacc.erroresSemanticosDetectados:
            print(error)
        return False, None
    




def leerFichero(fichero):
    try:
        with open(fichero, 'rt') as fd:
            contenido = fd.read()
            fd.close()
            return True, contenido
    except:
        return False, None


def compilar(fichero3D, verLexemas, verSalida):

    #COMPROBAMOS SI EXISTE EL FICHERO .3d Y CALCULAMOS EL NOMBRE DEL FICHERO A GENERAR
    if not os.path.exists(fichero3D):
        print(f"ERROR. NO SE HA ENCONTRADO EL FICHERO {fichero3D}.")
        return

    rutaAbsoluta=os.path.abspath(fichero3D)    
    carpeta, nombre_fichero=os.path.split(rutaAbsoluta)
    nombreSinExtension, extension = os.path.splitext(nombre_fichero)

    # EN VEZ DE UTILIZAR UNA VARIABLE GLOBAL USAMOS UNA PROPIEDAD DE CLASE QUE ALMACENA EL NMOBRE DEL FICHERO A ELIMINAR
    destino = f"{carpeta}/{nombreSinExtension}.py"

    # INTENTAMOE LEER EL CONTENIDO DEL FICHERO .3d
    ok, contenido=leerFichero(fichero3D)
    if not ok:
        print(f"ERROR. NO SE HA PODIDO LEER EL FICHERO {fichero3D}")    
        return
   
    # AHORA PASAMOS LOS ANALIZADORES. LEXICO Y SINTACTICO. ESTE ULTIMO LANZA EL SEMANTICO
    ok = AnalizadorLexico(contenido, verLexemas)
    
    if ok:        
        # SI PASA CORRECTAMENTE EL ANALIZADOR LEXICO, PASAREMOS EL SINTACTICO.
        ok, resultado = AnalizadorSintactico(contenido)

        if ok:            
            # SI PASA CORRECTAMENTE EL ANALIZADOR SINTACTICO Y SEMANTICO, GENERAMOS EL CODIGO
            print(f"FICHERO {fichero3D} COMPILADO CON EXITO.")

            salida=resultado.generar(0)            

            with open (destino,"wt") as fichero: 
                fichero.write(f"{salida}")

            if verSalida:
                print(f"{salida}")

            print(f"GENERADO FICHERO {destino}:")
            

####################################
######## PROGRAMA PRINCIPAL ########
####################################
#si hay parametros intentamos cargarlos.
verLexemas=False
verSalida=False
ficheros=[]

for num, parametro in enumerate(sys.argv):
    if num!=0: #ignoramos el 0, ya que es el nombre del ejecutable        
        if parametro.lower()=="-lex":
            verLexemas=True
        elif parametro.lower()=="-out":
            verSalida=True
        else:
            if parametro[-3:].lower()==".3d":
                ficheros.append(parametro)
    
if len(ficheros)>0:
    # HEMOS PASADO UNO O VARIOS FICHEROS COMO PARAMETRO
    for fichero in ficheros:
        compilar(fichero, verLexemas, verSalida)
else:
    ejecutable=sys.argv[0]
    print("ERROR DEBE INDICAR UN FICHERO A COMPILAR")
    print(f"USO: {ejecutable}  [-lex]  [-out]  <fichero.logo3d> ")
    print("")
    print("El parámetro -lex muestra por pantalla los lexemas detectados en el analizados léxico.")
    print("El parámetro -out muestra por pantalla el fichero de codigo intermedio generado.")
    print("")
    print("Los ficheros a compilar tienen que tener la extensión .3D")
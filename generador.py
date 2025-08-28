#Este fichero
from analizador_lexico import colores

#variables que necesita para la generacion del codigo
colorFondo = [0,0,0]
tipoProyeccion=0
nombreAplicacion=""
destino=""



componentes_colores={
    'NEGRO' : [0,0,0],
    'AZUL' : [0,0,1],
    'VERDE' : [0,1,0],
    'AZULCLARO' : [0,1,1],
    'ROJO' : [1,0,0],
    'ROSA' : [1, 0,1],
    'AMARILLO' : [1,1,0],
    'BLANCO' : [1,1,1],
    'CAFE' : [128/255,0,0],
    'CAFECLARO' : [128/255,64/255,0],
    'VERDEMEDIO' : [0,128/255,0],
    'VERDEAZUL': [0,128/255,128/255],
    'SALMON': [128/255,0,128/255],
    'LILA': [0,0,128/255],
    'NARANJA': [26/255,127/255,239/255],
    'GRIS' : [192/255,192/255,192/255],
}


def generarCodigoPrevio():

    aux= """
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, tan, pi
    
"""

    #OPTIMIZAMOS LA DECLARACIÓN DE VARIABLES ELIMINANDO LAS NO NECESARIAS.
    for color in colores:
        if (colores[color]): # HEMOS UTILIZADO ESTE COLOR EN NUESTRO PROGRAMA
            aux +=f"COLOR_BASICO_{color} =  {componentes_colores[color]} \n"

    aux +=f"""
lapizBajado = True

def subeLapiz():
    global lapizBajado
    lapizBajado = False

def bajaLapiz():
    global lapizBajado
    lapizBajado = True
    
def avanza(pasos):
    global lapizBajado
    if lapizBajado:
        glBegin(GL_LINES)    
        glVertex3f(0, 0, 0)
        glVertex3f(0, pasos, 0)
        glEnd()
    glTranslate(0, pasos, 0)
       
def init_gl():
    glutInit()                                                  
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)    
    glutCreateWindow(b"{nombreAplicacion}")                                
    glClearColor({colorFondo[0]}, {colorFondo[1]}, {colorFondo[2]}, 1.0)
    glEnable(GL_DEPTH_TEST)                                        

"""
    return aux

def generarCodigoPosterior():
    global tipoProyeccion
    codigo= """
def display(): """
    
    codigo+=f"""
    xMin, xMax, yMin, yMax, dNear, dFar = -1000, 1000, -1000, 1000, -1000, 1000    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()    """

    if tipoProyeccion == 6: # VISTA_GABINETE
        codigo +=f"""
    factor = pi/180                         
    alpha = 63.4  * factor                  
    phi = 30 * factor              
    cx = cos(phi)/tan(alpha)
    cy = sin(phi)/tan(alpha)
    cabinet_matrix = [1, 0, 0, 0, 0, 1, 0, 0, cx, cy, 1, 0, 0, 0, 0, 1]
    glMultMatrixf(cabinet_matrix) 
    glOrtho(xMin, xMax, yMin, yMax, dNear, dFar)     """
    elif tipoProyeccion == 7:  # VISTA_PERSPECTIVA
        codigo +=f"""
    fovy, near, far =  45, 1, 4500
    gluPerspective(fovy, glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT), near, far) """
    else: # EL RESTO DE VISTAS PARALELAS ORTOGONALES
        codigo +=f"""
    glOrtho(xMin, xMax, yMin, yMax, dNear, dFar)     """

    codigo +=f"""
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()    """

    if tipoProyeccion==0: # VISTA_ANTERIOR o DELANTERA
        codigo +=f"""
    x0 = 0.0;  y0 = 0.0;  z0 = 0.0;  xref = 0.0;  yref = 0.0;  zref = -1.0;  vx = 0.0;  vy = 1.0; vz = 0.0     """                
    elif tipoProyeccion==1: # VISTA_POSTERIOR 
        codigo +=f"""        
    x0 = 0.0;  y0 = 0.0;  z0 = 0.0;  xref = 0.0;  yref = 0.0;  zref = 1.0;  vx = 0.0;  vy = 1.0; vz = 0.0     """
    elif tipoProyeccion==2: # VISTA_ARRIBA 
        codigo +=f"""        
    x0 = 0.0;  y0 = 0.0;  z0 =0.0;  xref = 0.0;  yref = -1.0;  zref = 0.0;  vx = 0.0;  vy = 0.0; vz = -1.0     """
    elif tipoProyeccion==3: # VISTA_ABAJO 
        codigo +=f"""        
    x0 = 0.0;  y0 = 0.0;  z0 =0.0;  xref = 0.0;  yref = 1.0;  zref = 0.0;  vx = 0.0;  vy = 0.0; vz = -1.0     """
    elif tipoProyeccion==4: # VISTA_DERECHA 
        codigo +=f"""        
    x0 = 0.0;  y0 = 0.0;  z0 =0.0;  xref = -1;  yref = 0.0;  zref = 0.0;  vx = 0.0;  vy = 1.0; vz = 0.0     """
    elif tipoProyeccion==5: # VISTA_IZQUIERDA
        codigo +=f"""
    x0 = 0.0;  y0 = 0.0;  z0 =0.0;  xref = 1;  yref = 0.0;  zref = 0.0;  vx = 0.0;  vy = 1.0; vz = 0.0     """
    elif tipoProyeccion==6: # VISTA_GABINETE
        codigo +=f"""
    x0 = 0.0;  y0 = 0.0;  z0 = 0.0;  xref = 0.0;  yref = 0.0;  zref = -1.0;  vx = 0.0;  vy = 1.0; vz = 0.0     """
    else: # VISTA_PERSPECTIVA (SIMETRICA)
        codigo +=f"""        
    x0 = 1500.0;  y0 = 1200.0;  z0 = 1500.0;  xref = 0.0;  yref = 0.0;  zref = 0.0;  vx = 0.0;  vy = 1.0; vz = 0.0     """

    codigo +=f"""        
    gluLookAt(x0, y0, z0, xref, yref, zref, vx, vy, vz)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    programa()   
    glFlush() 

init_gl()
glutDisplayFunc(display)
glutMainLoop() 
"""
    return codigo

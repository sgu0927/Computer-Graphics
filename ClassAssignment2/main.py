import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *
from OpenGL.arrays import vbo
import os

gCamAng = 0.
gCamHeight = 1.

# Orbit
Orbit = False
gElevation = 0.
gAzimuth = 0.

# Panning
Panning = False
panned_xpos = 0.
panned_ypos = 0.

# Zooming
zoom = 0.

start_xpos = 0. 
start_ypos = 0.

gToggle = False
forced_smooth = False

gVertexArraySeparate = np.array([])
gNormalArray = np.array([])
gNormalArray2 = np.array([])

def draw_Obj_glDrawArray():
    global gVertexArraySeparate, gNormalArray
    varr = gVertexArraySeparate
    vnarr = gNormalArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 0, vnarr)
    glVertexPointer(3, GL_FLOAT, 0, varr)
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/3))


def draw_Obj_glDrawArray2():
    global gVertexArraySeparate, gNormalArray2
    varr = gVertexArraySeparate
    fvnarr = gNormalArray2
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 0, fvnarr)
    glVertexPointer(3, GL_FLOAT, 0, varr)
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/3))


def render(): 
    global gCamAng, gCamHeight, gAzimuth, gElevation, panned_xpos, panned_ypos, zoom
    global gToggle, forced_smooth

    if gToggle:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity()
    gluPerspective(45, 1, 1,30) 

    glMatrixMode(GL_MODELVIEW) 
    glLoadIdentity()
    gluLookAt(5 * np.sin(gCamAng),gCamHeight,10 * np.cos(gCamAng), 0,0,0, 0,1,0)
    # for panning and zoomming
    glTranslatef(panned_xpos, -panned_ypos, zoom)
    # for Orbit
    glRotatef(gAzimuth,1,0,0)
    glRotatef(gElevation,0,1,0)
    
    drawFrame()
    drawGrid()

    glEnable(GL_LIGHTING) 
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)

    glEnable(GL_NORMALIZE) 

    glPushMatrix()

    lightPos = (1.,0.,0.,0.) 
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    lightPos = (0.,1.,0.,0.) 
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    lightPos = (0.,0.,1.,0.) 
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos)
    lightPos = (-1.,-1.,-1.,0.) 
    glLightfv(GL_LIGHT3, GL_POSITION, lightPos)
    glPopMatrix()

    lightColor = (1., 0., 0., 1.)
    ambientLightColor = (.1, .0, .0, 1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    lightColor = (0., 1., 0., 1.)
    ambientLightColor = (.0, .1, .0, 1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

    lightColor = (0., 0., 1., 1.)
    ambientLightColor = (.0, .0, .1, 1.)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor)

    lightColor = (1., 0.2, 1., 1.)
    ambientLightColor = (.1, 0., .1, 1.)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT3, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT3, GL_AMBIENT, ambientLightColor)

    objectColor = (1.,0.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()

    glColor3ub(0, 0, 255) 

    if not forced_smooth:
        draw_Obj_glDrawArray()
    else:
        draw_Obj_glDrawArray2()

    glPopMatrix()

    glDisable(GL_LIGHTING)

def drawGrid():
    glColor3ub(192, 192, 192)

    glBegin(GL_LINES)
    glVertex3f(10., 0., 10.)
    glVertex3f(-10., 0., 10.)
    glVertex3f(-10., 0., -10.)
    glVertex3f(10., 0., -10.)
    glEnd()

    glBegin(GL_LINES)
    for i in range(-10, 10):
        glVertex3f(i, 0., -10.)
        glVertex3f(i, 0., 10.)
        glVertex3f(-10., 0., i)
        glVertex3f(10., 0., i)
    glEnd()

def drawFrame():
    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-10.,0.,0.]))
    glVertex3fv(np.array([10.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,10.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,-10]))
    glVertex3fv(np.array([0.,0.,10.]))
    glEnd()

def cursor_callback(window, xpos, ypos):
    global gElevation, gAzimuth, Orbit, Panning
    global start_xpos, start_ypos, panned_xpos, panned_ypos

    if Orbit:
        gAzimuth += (ypos - start_ypos)*(0.1)
        gElevation += (xpos - start_xpos)*(0.1)

        start_ypos = ypos
        start_xpos = xpos
    elif Panning:
        panned_ypos += (ypos - start_ypos)*(0.01)
        panned_xpos += (xpos - start_xpos)*(0.01)

        start_ypos = ypos
        start_xpos = xpos

def button_callback(window, button, action, mod):
    global Orbit, Panning, start_xpos, start_ypos
    start_xpos, start_ypos = glfw.get_cursor_pos(window)

    if action==glfw.PRESS:
        if button==glfw.MOUSE_BUTTON_LEFT:
            Orbit = True
        elif button==glfw.MOUSE_BUTTON_RIGHT:
            Panning = True
    elif action==glfw.RELEASE:
        Orbit = False
        Panning = False
     
def scroll_callback(window, xoffset, yoffset):
    global zoom

    if yoffset > 0:
        zoom += 0.5
    elif yoffset < 0:
        zoom += -0.5

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, gToggle, forced_smooth
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_Z:
            if gToggle: gToggle = False
            else: gToggle = True
        elif key==glfw.KEY_S:
            if forced_smooth: forced_smooth = False
            else: forced_smooth = True

def drop_callback(window, paths):
    global gVertexArraySeparate, gNormalArray, gNormalArray2
    
    f = open(paths[0],"r")

    vertex = []
    vertex_normal = []
    varr = []
    vnarr = []
    fvnarr = []
    tri = 0
    quad = 0
    n = 0

    while True:
        line = f.readline()
        if not line: break
        else:
            line = line.split()
        
        if len(line) == 0:
            continue

        if line[0] == 'v':
            vertex.append(list(map(float,line[1:])))
        elif line[0] == 'vn':
            vertex_normal.append(list(map(float,line[1:])))
        elif line[0] == 'f':
            if len(line) == 4:
                tri += 1
                for v in line[1:]:
                    indices = v.split('/')
                    varr.append(vertex[int(indices[0])-1])
                    if len(indices) > 2:
                        vnarr.append(vertex_normal[int(indices[2])-1])
                    v2 = vertex[int(indices[0])-1]
                    norm = np.sqrt(np.dot(v2,v2))
                    norm = 1/norm *np.array(v2)
                    fvnarr.append(norm)

            elif len(line) >= 5:
                if len(line) == 5:
                    quad += 1
                else:
                    n += 1

                first = line[1].split('/')
                fv1 = vertex[int(first[0])-1]
                norm1 = np.sqrt(np.dot(fv1,fv1))
                norm1 = 1/norm1 *np.array(fv1)

                for i in range(len(line)-3):
                    fvnarr.append(norm1)
                    varr.append(vertex[int(first[0])-1])
                    if len(first) > 2:
                        vnarr.append(vertex_normal[int(first[2])-1])
                    second = line[i+2].split('/')
                    third = line[i+3].split('/')
                    fv2 = vertex[int(second[0])-1]
                    fv3 = vertex[int(third[0])-1]
                    norm2 = np.sqrt(np.dot(fv2,fv2))
                    norm2 = 1/norm2 *np.array(fv2)
                    norm3 = np.sqrt(np.dot(fv3,fv3))
                    norm3 = 1/norm3 *np.array(fv3)
                    fvnarr.append(norm2)
                    fvnarr.append(norm3)
                    varr.append(vertex[int(second[0])-1])
                    varr.append(vertex[int(third[0])-1])
                    if len(second) > 2:
                        vnarr.append(vertex_normal[int(second[2])-1])
                    if len(third) > 2:
                        vnarr.append(vertex_normal[int(third[2])-1])
            

    print("File name: "+ (os.path.basename(paths[0])))
    print("Total number of faces: "+ str(tri + quad + n))
    print("Number of faces with 3 vertices: "+ str(tri))
    print("Number of faces with 4 vertices: "+ str(quad))
    print("Number of faces with more than 4 vertices: "+ str(n))

    gVertexArraySeparate = np.array(varr)
    gNormalArray = np.array(vnarr)
    gNormalArray2 = np.array(fvnarr)

    f.close()

def main(): 
    if not glfw.init(): 
        return 
    window = glfw.create_window(700,700,'2016025478', None,None) 
    if not window: 
        glfw.terminate() 
        return 
    glfw.make_context_current(window) 
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window): 
        glfw.poll_events() 
        render() 
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()

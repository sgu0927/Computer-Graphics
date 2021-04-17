import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *

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

def render(): 
    global gAzimuth, gElevation, panned_xpos, panned_ypos, zoom

    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE )
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity() 

    glMatrixMode(GL_MODELVIEW) 
    glLoadIdentity()
    
    gluPerspective(45, 1, 1,30)
    gluLookAt(0,1,10, 0,0,0, 0,1,0)
    # for panning and zoomming
    glTranslatef(panned_xpos, -panned_ypos, zoom)
    # for Orbit
    glRotatef(gAzimuth,1,0,0)
    glRotatef(gElevation,0,1,0)

    t = glfw.get_time()
    t = 2*t # for fast movement
    
    drawFrame()
    drawGrid()

    #body
    glPushMatrix()
    glTranslatef(0.3*np.sin(t), 0, 0)
    glColor3ub(123, 104, 238)
    glPushMatrix()
    glScalef(0.7, 1., 0.7) 
    drawSphere()
    glPopMatrix()

    #head (body -> head)
    glPushMatrix()
    glScalef(0.5, 0.5, 0.5) 
    glTranslatef(0.,2.2, 0.)
    drawSphere()
    glPopMatrix()

    #left arm (body -> left arm)
    glPushMatrix()
    glRotatef(-25*np.sin(t),0,0,1)
    glPushMatrix()
    glScalef(0.1, 1., 0.1) 
    glTranslatef(0.,-0.5, 8.0)
    drawSphere()
    glPopMatrix()

    #left hand (body -> left arm -> left hand)
    glPushMatrix()
    glTranslate(0.,-1.55,0.8)
    glScalef(0.1,0.1,0.1)
    drawSphere()
    glPopMatrix()
    glPopMatrix()

    #right arm (body -> right arm)
    glPushMatrix()
    glRotatef(25*np.sin(t),0,0,1)
    glPushMatrix()
    glScalef(0.1, 1., 0.1) 
    glTranslatef(0.,-0.5, -8.0)
    drawSphere()
    glPopMatrix()

    #right hand (body -> right arm -> right hand)
    glPushMatrix()
    glTranslate(0.,-1.55,-0.8)
    glScalef(0.1,0.1,0.1)
    drawSphere()
    glPopMatrix()
    glPopMatrix()
    
    #left leg (body -> left leg)
    glPushMatrix()
    glRotatef(10*np.sin(t),0,0,1)
    glPushMatrix()
    glScalef(0.2, 0.8, 0.2) 
    glTranslatef(0.,-2.0, 1.5)
    drawSphere()
    glPopMatrix()
    
    #left foot (body -> left leg -> left feet)
    glPushMatrix()
    glTranslatef(-0.15,-2.3, 0.3)
    glRotatef(-15*np.sin(t),0,0,1)
    glScalef(0.3, 0.1, 0.1) 
    drawSphere()
    glPopMatrix()
    glPopMatrix()

    #right thigh (body -> right thigh)
    glPushMatrix()
    glTranslatef(0.,-1.0, -0.5)
    glRotatef(-30*np.sin(t),0,0,1)
    glPushMatrix()
    glScalef(0.2, 0.6, 0.2) 
    drawSphere()
    glPopMatrix()

    #right calf (body -> right thigh -> right calf)
    glPushMatrix()
    glRotatef(-50*np.sin(t),0,0,1)
    glTranslatef(0.,-0.8, 0.)
    glPushMatrix()
    glScalef(0.2, 0.8, 0.2) 
    drawSphere()
    glPopMatrix()

    #right feet (body -> right thigh -> right calf -> right foot)
    glPushMatrix()
    glTranslatef(-0.15,-0.88,0.)  
    glRotatef(-25*np.sin(t),0,0,1)
    glScalef(0.3, 0.1, 0.1)
    drawSphere()
    glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()

    #draw ball (have no parent and child)
    glTranslatef(-1.0,-2.4,-0.5)  
    glScalef(0.4, 0.4, 0.4) 
    drawSphere()

#draw rectangular grid with lines on xz plane
def drawGrid():
    glColor3ub(192, 192, 192)

    glBegin(GL_QUADS)
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

# draw a cube of side 2, centered at the origin. 
def drawCube(): 
    glBegin(GL_QUADS) 
    glVertex3f( 1.0, 1.0,-1.0) 
    glVertex3f(-1.0, 1.0,-1.0) 
    glVertex3f(-1.0, 1.0, 1.0) 
    glVertex3f( 1.0, 1.0, 1.0)

    glVertex3f( 1.0,-1.0, 1.0) 
    glVertex3f(-1.0,-1.0, 1.0) 
    glVertex3f(-1.0,-1.0,-1.0) 
    glVertex3f( 1.0,-1.0,-1.0)

    glVertex3f( 1.0, 1.0, 1.0) 
    glVertex3f(-1.0, 1.0, 1.0) 
    glVertex3f(-1.0,-1.0, 1.0) 
    glVertex3f( 1.0,-1.0, 1.0)

    glVertex3f( 1.0,-1.0,-1.0) 
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0) 
    glVertex3f( 1.0, 1.0,-1.0)

    glVertex3f(-1.0, 1.0, 1.0) 
    glVertex3f(-1.0, 1.0,-1.0) 
    glVertex3f(-1.0,-1.0,-1.0) 
    glVertex3f(-1.0,-1.0, 1.0)

    glVertex3f( 1.0, 1.0,-1.0) 
    glVertex3f( 1.0, 1.0, 1.0) 
    glVertex3f( 1.0,-1.0, 1.0) 
    glVertex3f( 1.0,-1.0,-1.0) 
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

# draw a sphere of radius 1, centered at the origin. 
# numLats: number of latitude segments 
# numLongs: number of longitude segments 
def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0) 
        zr0 = np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats))) 
        z1 = np.sin(lat1) 
        zr1 = np.cos(lat1)

        # Use Quad strips to draw the sphere 
        glBegin(GL_QUAD_STRIP)

        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs)) 
            x = np.cos(lng) 
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0) 
            glVertex3f(x * zr1, y * zr1, z1)
        
        glEnd()

def cursor_callback(window, xpos, ypos):
    global gElevation, gAzimuth, Orbit, Panning
    global start_xpos, start_ypos, panned_xpos, panned_ypos

    if Orbit:
        gAzimuth += (ypos - start_ypos)*(0.1)
        gElevation += (xpos - start_xpos)*(0.1)

        #update current position
        start_ypos = ypos
        start_xpos = xpos
    elif Panning:
        panned_ypos += (ypos - start_ypos)*(0.01)
        panned_xpos += (xpos - start_xpos)*(0.01)

        #update current position
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

def main(): 
    if not glfw.init(): 
        return 
    window = glfw.create_window(700,700,'2016025478', None,None) 
    if not window: 
        glfw.terminate() 
        return 
    glfw.make_context_current(window) 

    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    glfw.swap_interval(1)
    while not glfw.window_should_close(window): 
        glfw.poll_events() 
        render() 
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()

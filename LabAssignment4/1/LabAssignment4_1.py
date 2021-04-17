import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

key_inputs=[]

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw coordinates
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0,255,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    glColor3ub(255,255,255)
    global key_inputs

    for i in range(len(key_inputs)-1,-1,-1):
        if(key_inputs[i]==1):
            glTranslatef(-0.1,0.,0.)
        elif(key_inputs[i]==2):
            glTranslatef(0.1,0.,0.)
        elif(key_inputs[i]==3):
            glRotatef(10,0,0,1)
        elif(key_inputs[i]==4):
            glRotatef(-10,0,0,1)
    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0., .5]))
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([.5, 0.]))
    glEnd()
    

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016025478", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.set_key_callback(window, key_callback)
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()

        glfw.swap_buffers(window)

    glfw.terminate()

def key_callback(window, key, scancode, action, mods):
    global key_inputs

    if key==glfw.KEY_Q and action == glfw.PRESS:
        key_inputs.append(1)
    elif key==glfw.KEY_E and action == glfw.PRESS:
        key_inputs.append(2)
    elif key==glfw.KEY_A and action == glfw.PRESS:
        key_inputs.append(3)
    elif key==glfw.KEY_D and action == glfw.PRESS:
        key_inputs.append(4)
    elif key==glfw.KEY_1 and action == glfw.PRESS:
        key_inputs.clear()
    



if __name__ == "__main__":
    main()

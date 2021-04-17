import glfw
from OpenGL.GL import *
import numpy as np

p0 = np.array([100.,200.])
p1 = np.array([200.,300.])
p2 = np.array([300.,300.])
p3 = np.array([400.,200.])
gEditingPoint = ''

def lerp(v1, v2, t):
    return (1-t)*v1 + t*v2

def render():
    global p0, p1, p2, p3
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,480, 0,480, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glColor3ub(0, 255, 0)
    glBegin(GL_LINE_STRIP)
    for t in np.arange(0,1,.01):
        p = (1-t)*p0 + t*p1
        glVertex2fv(p)
    for t in np.arange(0,1,.01):
        p = (1-t)*p1 + t*p2
        glVertex2fv(p)
    for t in np.arange(0,1,.01):
        p = (1-t)*p2 + t*p3
        glVertex2fv(p)
    for t in np.arange(0,1,.01):
        p = (1-t)*p3 + t*p0
        glVertex2fv(p)
    glEnd()

    glBegin(GL_LINE_STRIP)
    glColor3ub(255, 255, 255)
    for t in np.arange(0,1,.01):
        q0 = lerp(p0,p1,t)
        q1 = lerp(p1,p2,t)
        q2 = lerp(p2,p3,t)

        r0 = lerp(q0,q1,t)
        r1 = lerp(q1,q2,t)

        x = lerp(r0,r1,t)
        glVertex2fv(x)
    glEnd()

    glColor3ub(0, 255, 0)
    glPointSize(20.)
    glBegin(GL_POINTS)
    glVertex2fv(p0)
    glVertex2fv(p1)
    glVertex2fv(p2)
    glVertex2fv(p3)
    glEnd()

def button_callback(window, button, action, mod):
    global p0, p1, p2, p3, gEditingPoint
    if button==glfw.MOUSE_BUTTON_LEFT:
        x, y = glfw.get_cursor_pos(window)
        y = 480 - y
        if action==glfw.PRESS:
            if np.abs(x-p0[0])<10 and np.abs(y-p0[1])<10:
                gEditingPoint = 'p0'
            elif np.abs(x-p1[0])<10 and np.abs(y-p1[1])<10:
                gEditingPoint = 'p1'
            elif np.abs(x-p2[0])<10 and np.abs(y-p2[1])<10:
                gEditingPoint = 'p2'
            elif np.abs(x-p3[0])<10 and np.abs(y-p3[1])<10:
                gEditingPoint = 'p3'
        elif action==glfw.RELEASE:
            gEditingPoint = ''

def cursor_callback(window, xpos, ypos):
    global p0, p1, p2, p3, gEditingPoint
    ypos = 480 - ypos
    if gEditingPoint=='p0':
        p0[0]=xpos; p0[1]=ypos
    elif gEditingPoint=='p1':
        p1[0]=xpos; p1[1]=ypos
    elif gEditingPoint=='p2':
        p2[0]=xpos; p2[1]=ypos
    elif gEditingPoint=='p3':
        p3[0]=xpos; p3[1]=ypos

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2016025478-11-1', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()



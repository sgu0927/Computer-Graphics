import glfw
import numpy as np
from OpenGL.GL import *

A = np.deg2rad(np.arange(0,360,30,dtype=int))
xs = np.cos(A)
ys = np.sin(A)
p_type = [GL_POLYGON,GL_POINTS,GL_LINES,GL_LINE_STRIP,GL_LINE_LOOP,GL_TRIANGLES,
GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP]
idx = 4
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(p_type[idx])
    for i in range(12):
        glVertex2f(xs[i],ys[i])
    glEnd()

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2016025478", None,None)
    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()
# key char 형식
def key_callback(window, key, scancode, action, mods):
    global idx
    if key==glfw.KEY_0 and action==glfw.PRESS:
        idx =0
    elif key==glfw.KEY_1 and action==glfw.PRESS:
        idx =1
    elif key==glfw.KEY_2 and action==glfw.PRESS:
        idx =2
    elif key==glfw.KEY_3 and action==glfw.PRESS:
        idx =3
    elif key==glfw.KEY_4 and action==glfw.PRESS:
        idx =4
    elif key==glfw.KEY_5 and action==glfw.PRESS:
        idx =5
    elif key==glfw.KEY_6 and action==glfw.PRESS:
        idx =6
    elif key==glfw.KEY_7 and action==glfw.PRESS:
        idx =7
    elif key==glfw.KEY_8 and action==glfw.PRESS:
        idx =8
    elif key==glfw.KEY_9 and action==glfw.PRESS:
        idx =9
    
if __name__ == "__main__":
    main()

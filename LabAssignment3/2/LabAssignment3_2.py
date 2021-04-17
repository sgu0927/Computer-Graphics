import glfw
from OpenGL.GL import *
import numpy as np

gComposedM =np.identity(3)


def render(M):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    # draw triangle - p'=Mp
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (M @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (M @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (M @ np.array([.5,.0,1.]))[:-1] )
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

        render(gComposedM)

        glfw.swap_buffers(window)

    glfw.terminate()

# key char 형식
def key_callback(window, key, scancode, action, mods):
    global gComposedM

    if key==glfw.KEY_W and action == glfw.PRESS:
        N = np.array([[0.9, 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]])
        gComposedM = N@gComposedM
    elif key==glfw.KEY_E and action == glfw.PRESS:
        N = np.array([[1.1, 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]])
        gComposedM = N@gComposedM
    elif key==glfw.KEY_S and action == glfw.PRESS:
        N = np.array([[np.cos(np.deg2rad(10)), -np.sin(np.deg2rad(10)), 0],
            [np.sin(np.deg2rad(10)),np.cos(np.deg2rad(10)),   0.],
            [0.,          0.,        1.]])
        gComposedM = N@gComposedM
    elif key==glfw.KEY_D and action == glfw.PRESS:
        N = np.array([[np.cos(np.deg2rad(-10)), -np.sin(np.deg2rad(-10)), 0],
            [np.sin(np.deg2rad(-10)),np.cos(np.deg2rad(-10)),   0.],
            [0.,          0.,        1.]])
        gComposedM= N@gComposedM
    elif key==glfw.KEY_X and action == glfw.PRESS:
        N = np.array([[1., -0.1, 0.],
            [0., 1., 0.],
            [0., 0., 1.]]) 
        gComposedM = N@gComposedM       
    elif key==glfw.KEY_C and action == glfw.PRESS:
        N = np.array([[1., 0.1, 0.],
            [0., 1., 0.],
            [0., 0., 1.]])
        gComposedM = N@gComposedM
    elif key==glfw.KEY_R and action == glfw.PRESS:
        N = np.array([[1., 0., 0.],
            [0., -1., 0.],
            [0., 0., 1.]])
        gComposedM = N@gComposedM
    elif key==glfw.KEY_1 and action == glfw.PRESS:
        gComposedM = np.identity(3)

if __name__ == "__main__":
    main()


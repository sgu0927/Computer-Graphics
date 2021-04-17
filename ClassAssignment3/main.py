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
animate = False

gVertexArraySeparate = np.array([])
gNormalArray = np.array([])
gNormalArray2 = np.array([])

idx = 0
root_ = None
grid_size = 30

gVertexArrayIndexed =np.array([])
gIndexArray = np.array([])

class Node:
    def __init__(self, offset = [], channel = [], level = -1):
        self.name = None
        self.offset = offset
        self.channel = channel
        self.parent = None
        self.childs = []
        self.level = level
        self.link = np.identity(4)
        self.joint = np.identity(4)
        self.pos = [0, 0, 0]
        self.motions = []
        self.start_idx = 0
        self.frames = 0

def draw_skeleton(node):
    global gVertexArrayIndexed, gIndexArray
    offset = np.array(node.offset,'float32')
    glPushMatrix()

    if node.level != 0:
        gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed(offset[0], offset[1], offset[2])
        drawCube_glDrawElements()

    glTranslate(offset[0],offset[1],offset[2])

    for child in node.childs:
        draw_skeleton(child)

    glPopMatrix()

def draw_skeleton2(node, idx):
    global root_, gVertexArrayIndexed, gIndexArray

    idx %= root_.frames
    offset = np.array(node.offset,'float32')
    M = np.identity(4)
    Rx = np.identity(4)
    Ry = np.identity(4)
    Rz = np.identity(4)
    trans = [0.,0.,0.]
    
    for i in range(len(node.channel)):

        channel = node.channel[i]
        s = node.start_idx
        j = s + i

        if channel.upper() == "XPOSITION":
            trans[0] = root_.motions[idx][j]
        elif channel.upper() == "YPOSITION":
            trans[1] = root_.motions[idx][j]
        elif channel.upper() == "ZPOSITION":
            trans[2] = root_.motions[idx][j]
        if channel.upper() == "ZROTATION":
            deg = root_.motions[idx][j]
            th = np.deg2rad(deg)
            s = np.sin(th)
            c = np.cos(th)
            Rz[0][0] = c
            Rz[0][1] = -s
            Rz[1][0] = s
            Rz[1][1] = c
            M = M @ Rz
        elif channel.upper() == "XROTATION":
            deg = root_.motions[idx][j]
            th = np.deg2rad(deg)
            s = np.sin(th)
            c = np.cos(th)
            Rx[1][1] = c
            Rx[1][2] = -s
            Rx[2][1] = s
            Rx[2][2] = c
            M = M @ Rx
        elif channel.upper() == "YROTATION":
            deg = root_.motions[idx][j]
            th = np.deg2rad(deg)
            s = np.sin(th)
            c = np.cos(th)
            Ry[0][0] = c
            Ry[2][0] = -s
            Ry[0][2] = s
            Ry[2][2] = c
            M = M @ Ry

    glPushMatrix()
    glTranslatef(trans[0],trans[1],trans[2])
    if node.level != 0:
        gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed(offset[0], offset[1], offset[2])
        drawCube_glDrawElements()

    glTranslatef(offset[0],offset[1],offset[2])
    glMultMatrixf(M.T)
    for child in node.childs:
        draw_skeleton2(child, idx)

    glPopMatrix()

def set_motions(node, motions):
    if node.level != 0:
        node.motions.append(motions[0:len(node.channel)])
        motions = motions[len(node.channel):]
    else:
        node.motions.append(motions)
        motions = motions[len(node.channel):]

    for child in node.childs:
        set_motions(child, motions)

def render(): 
    global gCamAng, gCamHeight, gAzimuth, gElevation, panned_xpos, panned_ypos, zoom
    global gToggle, forced_smooth, root_, idx, animate
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity()
    gluPerspective(45, 1, 1,50000) 

    glMatrixMode(GL_MODELVIEW) 
    glLoadIdentity()
    gluLookAt(300 * np.sin(gCamAng),gCamHeight,300 * np.cos(gCamAng), 0,0,0, 0,1,0)
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

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    if root_ is not None and not animate:
        draw_skeleton(root_)
    elif root_ is not None and animate:
        draw_skeleton2(root_, idx)
        if idx == root_.frames:
            idx = 0
    glPopMatrix()

    glDisable(GL_LIGHTING)

def drawGrid():
    global grid_size

    glColor3ub(192, 192, 192)

    glBegin(GL_LINES)
    glVertex3f(grid_size, 0., grid_size)
    glVertex3f(-grid_size, 0., grid_size)
    glVertex3f(-grid_size, 0., -grid_size)
    glVertex3f(grid_size, 0., -grid_size)
    glEnd()

    glBegin(GL_LINES)
    for i in range(-grid_size, grid_size):
        glVertex3f(i, 0., -grid_size)
        glVertex3f(i, 0., grid_size)
        glVertex3f(-grid_size, 0., i)
        glVertex3f(grid_size, 0., i)
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

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def createVertexAndIndexArrayIndexed(x, y, z):
    flag = False
    x_ = float(x)/2 
    y_ = float(y)/2 
    z_ = float(z)/2 

    tmp = [abs(x_),abs(y_),abs(z_)]
    max_ = max(tmp)
    min_ = min(tmp)
    middle_ = sum(tmp) - max_ - min_

    if middle_ == 0:
        flag = True

    if min_ == abs(x_):
        x_ = max_ * 0.15
    elif min_ == abs(y_):
        y_ = max_ * 0.15
    elif min_ == abs(z_):
        z_ = max_ * 0.15

    if flag:
        if middle_ == abs(x_):
            x_ = max_ * 0.2
        elif middle_ == abs(y_):
            y_ = max_ * 0.2
        elif middle_ == abs(z_):
            z_ = max_ * 0.2

    varr = np.array([
        ( -0.5773502691896258 , 0.5773502691896258 , 0.5773502691896258 ),
        [-x_, y_, z_],
        ( 0.8164965809277261 , 0.4082482904638631 , 0.4082482904638631 ),
        [x_, y_, z_],
        ( 0.4082482904638631 , -0.4082482904638631 , 0.8164965809277261 ),
        [x_, -y_, z_],
        ( -0.4082482904638631 , -0.8164965809277261 , 0.4082482904638631 ),
        [-x_, -y_, z_],
        ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
        [-x_, y_, -z_],
        ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
        [x_, y_, -z_],
        ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
        [x_, -y_, -z_],
        ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
        [-x_, -y_,-z_],
        ], 'float32')

    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

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
        zoom += 1.1
    elif yoffset < 0:
        zoom += -1.1

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, gToggle, forced_smooth, animate, idx
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_SPACE:
            if animate:
                idx = 0
            animate = not animate

def drop_callback(window, paths):
    global gVertexArraySeparate, gNormalArray, gNormalArray2, root_, animate
    
    f = open(paths[0],"r")
    animate = False

    frames = 0
    frame_time = 0
    FPS = 0
    joints = []
    joint_cnt = 0
    brace_cnt = 0
    all_nodes =[]
    i=0
    flag = True
    channel_idx = 0

    #parsing HIERARCHY
    while True:
        line = f.readline()
        if not line: break
        else:
            line = line.split()
        
        if len(line) == 0:
            continue

        if line[0] == 'Frames:':
            frames = int(line[1])
        elif line[0] == 'Frame' and line[1] == 'Time:':
            frame_time = float(line[2])
            FPS = 1 / frame_time
        elif  line[0] == 'ROOT' or line[0] == 'JOINT':
            joint_cnt += 1

        if line[0] == 'ROOT':
            name_ = line[1]
            while line[0] != 'OFFSET':
                line = f.readline()
                line = line.split()

            offsets_tmp = [line[1],line[2],line[3]]
            while line[0] != 'CHANNELS':
                line = f.readline()
                line = line.split()
            channels_tmp = [line[2], line[3], line[4], line[5], line[6], line[7]]
            channel_idx += len(channels_tmp)
            root = Node(offsets_tmp, channels_tmp,0)
            root.name = name_
            brace_cnt = 0
            parent = root
            all_nodes.append(root)
        elif line[0] == 'JOINT':
            joints.append(line[1])
            name_ = line[1]
            while line[0] != '{':
                line = f.readline()
                line = line.split()
            brace_cnt += 1
            while line[0] != 'OFFSET':
                line = f.readline()
                line = line.split()
            offsets_tmp = [line[1],line[2],line[3]]
            while line[0] != 'CHANNELS':
                line = f.readline()
                line = line.split()
            channels_tmp = [line[2], line[3], line[4]]
            joint_tmp = Node(offsets_tmp, channels_tmp, brace_cnt)
            joint_tmp.name = name_
            if parent is not None:
                parent.childs.append(joint_tmp)
            joint_tmp.parent = parent
            parent = joint_tmp
            joint_tmp.start_idx = channel_idx
            channel_idx += len(channels_tmp)
            all_nodes.append(joint_tmp)
        elif line[0] == 'End':
            while line[0] != '{':
                line = f.readline()
                line = line.split()
            brace_cnt += 1
            while line[0] != 'OFFSET':
                line = f.readline()
                line = line.split()
            offsets_tmp = [line[1],line[2],line[3]]
            joint_tmp = Node(offsets_tmp)
            joint_tmp.level = brace_cnt
            joint_tmp.name = 'End'
            parent.childs.append(joint_tmp)
            joint_tmp.parent = parent
            all_nodes.append(joint_tmp)
            flag = False
        elif line[0] == '}':
            brace_cnt -= 1
            if parent is not None and flag:
                parent = parent.parent
            else:
                flag = True
        elif line[0] == 'MOTION':
            break

    #parsing MOTION 
    while line[0] != 'Frames:':
        line = f.readline()
        line = line.split()
    frames = int(line[1])
    while line[0] != 'Frame' and line[1] != 'Time:':
        line = f.readline()
        line = line.split()
    frame_time = float(line[2])
    FPS = 1 / frame_time

    while True:
        motions = []
        line = f.readline()
        if not line: break
        else:
            line = line.split()
            motions = [float(a) for a in line]
        if len(line) == 0:
            continue

        if len(motions) > 0:
            set_motions(root,motions)

    print("File name: "+ (os.path.basename(paths[0])))
    print("Number of frames: "+ str(frames))
    print("FPS (which is 1/FrameTime): " + str(FPS))
    print("Number of joints (including root): "+ str(joint_cnt))
    print("List of all joint names: "+ str(joints))
    root.frames = frames
    root_ = root

    f.close()

def main():
    global idx, animate
    if not glfw.init(): 
        return 
    window = glfw.create_window(1000,1000,'2016025478', None,None) 
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

    idx = 0
    while not glfw.window_should_close(window): 
        glfw.poll_events() 
        render() 
        glfw.swap_buffers(window)
        if animate:
            idx +=1
    glfw.terminate()

if __name__ == "__main__":
    main()

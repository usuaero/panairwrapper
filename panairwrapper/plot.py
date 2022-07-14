'''
Module for plotting surfaces in a pyqtgraph 3D ViewWidget
'''

import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import panairwrapper as panw

def plot(case, cols=[], hold=True):
    '''
    Function to plot a set of networks (from a PanairWrapper class instance) with pyqtgraph.
    parameters:
    * case: the panair case at hand
    * cols: array of colors to be attributed to the wireframe plot of each network
    * hold: whether to await for user pressing ENTER after plot is generated
    '''

    #create Qt App
    qapp=pg.mkQApp()

    #get networks as 3D arrays
    arrs=[ntw[1] for ntw in case._networks]

    #create OpenGL widget
    view=gl.GLViewWidget()

    items=[]
    meshes=[]

    #add default colors if any is missing
    defcols=['r', 'g', 'b', 'c', 'm', 'y', 'k']
    n=0
    while len(cols)<len(arrs):
        cols.append(defcols[n])
        n=(n+1)%len(defcols)
    
    for arr, col in zip(arrs, cols):
        _addplot(view, arr, items, meshes, col=pg.glColor(col))
    
    view.show()

    if hold:
        _hold()

def _hold():
    input('Press ENTER to continue ...')

def _addplot(view, ntw, items, meshes, col=pg.glColor('w')):
    #create mesh item

    nm=np.size(ntw, 0) #indexing assumes np.swapaxes in PanairCase.add_network method
    nn=np.size(ntw, 1)
    verts=np.zeros((6*(nm-1)*(nn-1), 3))
    faces=np.zeros((2*(nm-1)*(nn-1), 3), dtype='int')
    n=0
    nf=0
    for i in range(nm-1):
        for j in range(nn-1):
            #first triangle
            verts[n, :]=ntw[i, j, :]
            verts[n+1, :]=ntw[i+1, j, :]
            verts[n+2, :]=ntw[i+1, j+1, :]
            faces[nf, :]=np.array([n, n+1, n+2], dtype='int')

            #second triangle
            verts[n+3, :]=ntw[i+1, j+1, :]
            verts[n+4, :]=ntw[i, j+1, :]
            verts[n+5, :]=ntw[i, j, :]
            faces[nf+1, :]=np.array([n, n+1, n+2], dtype='int')+3
            
            n+=6
            nf+=2
    
    mdata=gl.MeshData(vertexes=verts, faces=faces)
    mitem=gl.GLMeshItem(meshdata=mdata, drawEdges=True, edgeColor=col, color=pg.glColor('w'))

    view.addItem(mitem)

    items.append(mitem)
    meshes.append(mdata)
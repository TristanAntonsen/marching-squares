import numpy as np

CELL_TYPES = {
    "BC" : {
        "nodes" : np.array([[0,0],[1,0],[1,1],[0,1]]), # vertices
        "beams" : np.array([[0,2],[1,3]]) # node connectivity
    }, 

    "SC" : {
        "nodes" : np.array([[0,0],[1,0],[1,1],[0,1]]), # vertices
        "beams" : np.array([[0,1],[1,2],[2,3],[3,1]]) # node connectivity
    }
}
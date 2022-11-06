import numpy as np
from cells import CELL_TYPES

class UnitCell:

    def __init__(self, type):
        
        self.nodes = CELL_TYPES[type]['beams']
        self.beams = CELL_TYPES[type]['nodes']
        self.x_scale = 10
        self.y_scale = 10

class Lattice:

    def __init__(self, unit_cell, x_count, y_count):
        self.unit_cell = unit_cell
        self.cell_x_scale = unit_cell.x_scale
        self.cell_y_scale = unit_cell.y_scale
        self.x_count = x_count
        self.y_count = y_count

        # self.return_cell(1,1)

    def return_cell_coords(self, x, y):

        if x > self.x_count or y > self.y_count:
            print("Index too large")
            return

        node_coords = self.unit_cell.nodes.copy()

        for node in node_coords:
            node[0] = node[0] * self.cell_x_scale + self.cell_x_scale * x
            node[1] = node[1] * self.cell_y_scale + self.cell_y_scale * y

        return node_coords

    def return_all_cell_coords(self):
        all_cell_coords = []
        for x in range(self.x_count):
            for y in range(self.y_count):
                coords = self.return_cell_coords(x,y)
                all_cell_coords.append(coords)

        return all_cell_coords



if __name__ == "__main__":

    cell = UnitCell("BC")

    lattice = Lattice(cell, 2, 2)
    lattice.return_cell_coords(0,1)
    
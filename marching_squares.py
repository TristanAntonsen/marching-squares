import numpy as np
from PIL import Image, ImageDraw
import numpy as np
from tables import STATES

# ignore divide by zero errors
np.seterr(divide='ignore', invalid='ignore')


class Grid:

    def __init__(self, scale, x_count, y_count):
        self.x_count = x_count
        self.y_count = y_count
        self.scale = scale
        self.values = np.zeros((x_count + 1) * (y_count + 1)).reshape(y_count + 1, x_count + 1)
        self.point_array = np.zeros(x_count * y_count).reshape(y_count, x_count)
        self.create_points()

    def create_points(self):
        points = []
        point_indices = []
        for x in range(self.x_count):
            for y in range(self.y_count):
                points.append([x * self.scale,y * self.scale])
                point_indices.append([y, x])

        self.points = np.array(points)
        self.point_indices = np.array(point_indices)

def get_state(a,b,c,d,threshold):
    
    # Either 0 or 1
    # < threshold = 0
    # > threshold = 1

    a = threshold + a > threshold
    b = threshold + b > threshold
    c = threshold + c > threshold
    d = threshold + d > threshold

    # Index for lookup table
    s = round(a * 8 + b * 4 + c * 2 + d * 1)

    return s

def circle(x, y, cx, cy, radius):
    # distance from center point
    d = np.sqrt((cx-x) ** 2 + (cy-y) ** 2) - radius
    return d

def lerp(a, b, t):
    c = a + t * (b - a)
    return c

def lerp_points(p0, p1, t):

    return [
        lerp(p0[0], p1[0], t),
        lerp(p0[1], p1[1], t)
    ]

def find_lerp_factor(v0, v1, iso_val):
    return (iso_val - v0) / (v1 - v0)

def map(x, y):
    d = circle(x, y, 540, 540, 400)
    return d

def map_grid(grid: Grid):
    
    for i in range(grid.x_count + 1):
        for j in range(grid.y_count + 1):
            x = i * grid.scale
            y = j * grid.scale
            grid.values[j, i] = circle(x, y, 540, 540, 400)

def march(grid: Grid, iso, interpolated=True):

    graph = []

    map_grid(grid)

    for point in grid.points:

        scale = grid.scale

        x = point[0]
        y = point[1]

        ## Corner points
        p0 = (x        , y        )
        p1 = (x + scale, y        )
        p2 = (x + scale, y + scale)
        p3 = (x        , y + scale)

        ## values at (corner) points
        v0 = map(*p0)
        v1 = map(*p1)
        v2 = map(*p2)
        v3 = map(*p3)

        ## Interopolation factors
        ta = find_lerp_factor(v0, v1, iso)
        tb = find_lerp_factor(v1, v2, iso)
        tc = find_lerp_factor(v3, v2, iso) # flip due to sign change
        td = find_lerp_factor(v0, v3, iso)

        ## edge point locations (interpolated)
        a = [x + ta * scale , y              ] # 01
        b = [x + scale      , y + tb * scale ] # 12
        c = [x + tc * scale , y + scale      ] # 23
        d = [x              , y + td * scale ] # 30

        ## edge point locations (not interpolated)
        _a = [x + 0.5 * scale , y               ] # 01
        _b = [x + scale       , y + 0.5 * scale ] # 12
        _c = [x + 0.5 * scale , y + scale       ] # 23
        _d = [x               , y + 0.5 * scale ] # 30

        edge_points = [a,b,c,d]

        if interpolated == False:
            edge_points = [_a,_b,_c,_d]

        state = get_state(v0, v1, v2, v3, 0)
        edges = STATES[state]
        

        for line in edges:
            p1 = edge_points[line[0]]
            p2 = edge_points[line[1]]
            graph.append((p1, p2))

    return graph

def march2(grid: Grid, iso, interpolated=True):

    graph = []

    map_grid(grid)

    for i in range(grid.x_count):
        for j in range(grid.y_count):
            scale = grid.scale

            x = i * scale
            y = j * scale

            ## values at (corner) points
            v0 = grid.values[i    , j    ]
            v1 = grid.values[i + 1, j    ]
            v2 = grid.values[i + 1, j + 1]
            v3 = grid.values[i    , j + 1]

            ## Interopolation factors
            ta = find_lerp_factor(v0, v1, iso)
            tb = find_lerp_factor(v1, v2, iso)
            tc = find_lerp_factor(v3, v2, iso) # flip due to sign change
            td = find_lerp_factor(v0, v3, iso)

            ## edge point locations (interpolated)
            a = [x + ta * scale , y              ] # 01
            b = [x + scale      , y + tb * scale ] # 12
            c = [x + tc * scale , y + scale      ] # 23
            d = [x              , y + td * scale ] # 30

            ## edge point locations (not interpolated)
            _a = [x + 0.5 * scale , y               ] # 01
            _b = [x + scale       , y + 0.5 * scale ] # 12
            _c = [x + 0.5 * scale , y + scale       ] # 23
            _d = [x               , y + 0.5 * scale ] # 30

            edge_points = [a,b,c,d]

            if interpolated == False:
                edge_points = [_a,_b,_c,_d]

            state = get_state(v0, v1, v2, v3, 0)
            edges = STATES[state]
            
            for line in edges:
                p1 = edge_points[line[0]]
                p2 = edge_points[line[1]]
                graph.append((p1, p2))

    return graph

def main():

    image_resolution = 1080
    img = Image.new('RGB', (image_resolution, image_resolution))
    draw = ImageDraw.Draw(img)

    def center_ellipse(x,y,r,c):

        draw.ellipse([x - r, y - r, x + r, y + r], fill=c)

    def center_rectangle(x,y,l,w,c):
        l = l/2
        w = w/2
        draw.rectangle([x - w, y - l, x + w, y + l], fill=c)

    radius = 400
    interpolated = True
    iso = 0
    grid_divisions = 50

    grid_scale = image_resolution / (grid_divisions - 1)

    grid = Grid(grid_scale, grid_divisions, grid_divisions)

    ## Drawing shapes 
    # Background
    center_rectangle(image_resolution / 2, image_resolution / 2, image_resolution, image_resolution, f'rgb({73},{73},{71})')
    ## Circle (for map(p))
    center_ellipse(image_resolution / 2, image_resolution / 2, radius, f'rgb({68},{204},{255})')

    def draw_edges(grid, img_path):

        edges = march2(grid, iso, interpolated)
        for line in edges:
            p1 = line[0]
            p2 = line[1]
            draw.line([p1[0], p1[1], p2[0], p2[1]], fill=f'rgb({255},{255},{255})',width=4)
        
        img.save(img_path)

    draw_edges(grid, "marched.png")

if __name__ == "__main__":
    main()
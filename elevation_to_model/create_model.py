from stl import Stl
import tifffile as tiff
import numpy as np


input = tiff.imread('N:\\usgs-data\\elevation\\CA_YosemiteNP_2019_D19\\USGS_1M_11_x27y418_CA_YosemiteNP_2019_D19.tif')

'''
    nw -- ne
    |  m  |
    sw -- se
'''


def total_triangles(x_width, y_width):
    return 6 * x_width * y_width + 4 * x_width + 4 * y_width


width = 10


stl = Stl('outfile.stl', width)

h = [[1,2,3], [4,9,2], [3,5,10]]
nx, ny = 3, 3

h = np.array(input)
h = h[0:1000, 0:1000]
h -= np.min(h) - 1
h *= 100
nx, ny = h.shape
stl.write_header(total_triangles(nx, ny))
print(f"Writing {total_triangles(nx, ny)} triangles for {nx}x{ny} grid")


# stl.emit((1, 1, 1), (2, 3, 4), (5, 6, 7))



for x in range(nx - 1):
    for y in range(ny - 1):
        if h[x][y] < 0:
            continue

        nw = (x * width, y * width, h[x][y])
        ne = ((x+1) * width, y * width, h[x+1][y])
        sw = (x * width, (y+1) * width, h[x][y+1])
        se = ((x+1) * width, (y+1) * width, h[x+1][y+1])
        nwh0 = (x * width, y * width, 0)
        neh0 = ((x+1) * width, y * width, 0)
        swh0 = (x * width, (y+1) * width, 0)
        seh0 = ((x+1) * width, (y+1) * width, 0)
        m = ((x+0.5) * width, (y+0.5) * width, (nw[2] + ne[2] + sw[2] + se[2]) / 4)

        # four triangles for the top
        stl.emit(nw, m, ne)
        stl.emit(ne, m, se)
        stl.emit(se, m, sw)
        stl.emit(sw, m, nw)

        # two triangles for the bottom
        stl.emit(nwh0, swh0, seh0)
        stl.emit(seh0, neh0, nwh0)

        # North edge
        if y == 0 or h[x][y-1] < 0:
            stl.emit(nw, ne, nwh0)
            stl.emit(ne, neh0, nwh0)

        # East edge
        if x == nx - 2 or h[x+1][y] < 0:
            stl.emit(se, ne, seh0)
            stl.emit(ne, neh0, seh0)

        # South edge
        if y == ny - 2 or h[x][y+1] < 0:
            stl.emit(sw, se, swh0)
            stl.emit(se, seh0, swh0)

        # West edge
        if x == 0 or h[x-1][y] < 0:
            stl.emit(nw, sw, swh0)
            stl.emit(swh0, nwh0, nw)



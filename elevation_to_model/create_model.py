from stl import Stl
import tifffile as tiff
import numpy as np
from pathlib import Path



'''
    nw -- ne
    |  m  |
    sw -- se
'''


def total_triangles(x_width, y_width):
    return 6 * x_width * y_width + 4 * x_width + 4 * y_width



width = 1

input_filepath = "H:\\usgs-data\\elevation\\AZ_USFS_3DEP_Processing_2019_D20\\USGS_1M_12_x62y378_AZ_USFS_3DEP_Processing_2019_D20.tif"
input_file_contents = tiff.imread(input_filepath)
filename = input_filepath.split('\\')[-1]
filename = filename.split('.')[0]
stl = Stl(f"N:\\3d\\models\\generated\\yosemite\\{width}M-{filename}.stl")


input_filepath = "C:\\Users\\Eracoy\\Downloads\\swissalti3d_2019_2617-1091_2_2056_5728.tif"
input_file_contents = tiff.imread(input_filepath)
Path(f"N:\\3d\\models\\generated\\matterhorn").mkdir(parents=True, exist_ok=True)
stl = Stl(f"N:\\3d\\models\\generated\\matterhorn\\{width}M-matterhorn.stl")


h = np.array(input_file_contents)
resolution = 1
# h = h[:2000:resolution, 8000::resolution]
h -= 0
h *= width / resolution
nx, ny = h.shape
stl.write_header(total_triangles(nx, ny))
print(f"Writing {total_triangles(nx, ny)} triangles for {nx}x{ny} grid")


for x in range(nx - 1):
    print(f"Processing row {x+1}/{nx}")
    for y in range(ny - 1):
        if h[x][y] < 0 or h[x+1][y] < 0 or h[x][y+1] < 0 or h[x+1][y+1] < 0:
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



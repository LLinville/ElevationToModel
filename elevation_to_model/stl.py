import struct

ORIGIN = b'\x00' * 12


class Stl:
    def __init__(self, outfile_name):
        self.outfile = open(outfile_name, 'wb+')

    def write_header(self, total_triangles=4):
        self.outfile.write(b'\x00' * 80)
        self.outfile.write(total_triangles.to_bytes(4, byteorder='little', signed=False))

    def emit(self, p1, p2, p3):
        # print(f"Emitting triangle {p1}, {p2}, {p3}")
        self.outfile.write(ORIGIN)
        values = [v for p in [p1, p2, p3] for v in p]
        self.outfile.write(struct.pack('f'*len(values), *values))
        self.outfile.write(b'\x00\x00')

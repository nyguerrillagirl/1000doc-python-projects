from wad_data import WADData


def read_vertex(self, offset):
    # 4 bytes = 2h + 2h
    x = self.read_2_bytes(offset, byte_format='h')
    y = self.read_2_bytes(offset, byte_format='h')
    return vec2(x, y)
if __name__ == '__main__':
    doom = DoomEngine()
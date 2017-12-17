import os
from RLedInterface import RL
from RLedException import RLedError


class RL2(RL):
    def __init__(self):
        """Voreinstelllungen"""
        super().__init__()
        self.MAXBYTES = 131

    def compress(self, sourcefile, destinationfile):
        """runlength compressing for ASCII files only\
           raises ValueError if it encounters chars bigger than 127
        @param sourcefile: The file including path that should be compressed
        @type sourcefile: string
        @return: Nothing"""
        with open(sourcefile, 'rb') as src_file, open(destinationfile,
                                                      'wb') as dest_file:
            dest_file.write(bytes("rl2", 'utf-8'))
            extension_orig = bytes(os.path.splitext(sourcefile)[1][1:], 'utf-8')
            dest_file.write(len(extension_orig).to_bytes(1, 'big'))
            dest_file.write(extension_orig)
            counter = 1
            last_byte = None
            chunk = src_file.read(self.chunk_size)
            while chunk:
                for byte in chunk:
                    if last_byte is not None and last_byte == byte and counter < self.MAXBYTES:
                        counter += 1
                    else:
                        if last_byte is not None:
                            if last_byte < 128:
                                if counter != 1:
                                    dest_file.write((counter + (255 - self.MAXBYTES)).to_bytes(1, 'big'))
                                dest_file.write(last_byte.to_bytes(1, 'big'))
                            else:
                                raise RLedError
                            counter = 1
                    last_byte = byte
                if last_byte < self.MAXBYTES:
                    if counter != 1:
                        dest_file.write((counter + (255 - self.MAXBYTES)).to_bytes(1, 'big'))
                    dest_file.write(last_byte.to_bytes(1, 'big'))
                else:
                    raise RLedError
                counter = 1
                chunk = src_file.read(self.chunk_size)
        return 0

    def expand(self, sourcefile, destionationfile):
        """runlength expanding for files which were\
           compressed with compress_simple method
        @param sourcefile: The file including path that should be compressed
        @type sourcefile: string
        @return: Nothing"""
        with open(sourcefile, 'rb') as src_file:
            if src_file.read(3) == b'rl2':
                extension_counter = src_file.read(1)
                extension_orig = src_file.read(int.from_bytes(extension_counter, 'big'))
                with open(destionationfile,
                          'wb') as dest_file:
                    chunk = src_file.read(self.chunk_size)
                    count = 0
                    while chunk:
                        for byte in chunk:
                            if count == 0:
                                if byte > 127:
                                    count = byte - (255 - self.MAXBYTES)
                                else:
                                    dest_file.write(byte.to_bytes(1, 'big'))
                            else:
                                for i in range(count):
                                    dest_file.write(byte.to_bytes(1, 'big'))
                                count = 0
                        chunk = src_file.read(self.chunk_size)
            else:
                raise RLedError
        return 0

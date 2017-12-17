import os
from RLedInterface import RL
from RLedException import RLedError


class RL3(RL):
    def __init__(self):
        """Voreinstelllungen"""
        super().__init__()
        self.MARKER = chr(0x90)
        self.MAXBYTES = 258

    def compress(self, sourcefile, destinationfile):
        """runlength compressing for any type of file
        @param sourcefile: The file including path that should be compressed
        @type sourcefile: string
        @return: Nothing

        It contains two paragraphs."""
        with open(sourcefile, 'rb') as src_file, open(destinationfile,
                                                      'wb') as dest_file:
            dest_file.write(bytes("rl3", 'utf-8'))
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
                            if counter > (self.MAXBYTES - 255):
                                dest_file.write(ord(self.MARKER).to_bytes(1, 'big'))
                                dest_file.write((counter - (self.MAXBYTES - 255)).to_bytes(1, 'big'))
                                dest_file.write(last_byte.to_bytes(1, 'big'))
                            else:
                                for i in range(counter):
                                    dest_file.write(last_byte.to_bytes(1, 'big'))
                                    if last_byte == ord(self.MARKER):
                                        dest_file.write(b'\x00')
                            counter = 1
                    last_byte = byte
                chunk = src_file.read(self.chunk_size)
            if last_byte is not None:
                if counter > (self.MAXBYTES - 255):
                    dest_file.write(ord(self.MARKER).to_bytes(1, 'big'))
                    dest_file.write((counter - (self.MAXBYTES - 255)).to_bytes(1, 'big'))
                    dest_file.write(last_byte.to_bytes(1, 'big'))
                else:
                    for i in range(counter):
                        dest_file.write(last_byte.to_bytes(1, 'big'))
                        if last_byte == ord(self.MARKER):
                            dest_file.write(b'\x00')
        return 0

    def expand(self, sourcefile, destionationfile):
        """runlength expanding for files which were\
           compressed with compress method
        @param sourcefile: The file including path that should be compressed
        @type sourcefile: string
        @return: Nothing"""
        with open(sourcefile, 'rb') as src_file:
            if src_file.read(3) == b'rl3':
                extension_counter = src_file.read(1)
                extension_orig = src_file.read(int.from_bytes(extension_counter, 'big'))
                with open(destionationfile,
                          'wb') as dest_file:
                    chunk = src_file.read(self.chunk_size)
                    counter = False
                    value = False
                    count = 0
                    while chunk:
                        for byte in chunk:
                            if byte == ord(self.MARKER) and not counter and not value:
                                counter = True
                            elif counter:
                                if byte == 0:
                                    dest_file.write(ord(self.MARKER).to_bytes(1, 'big'))
                                    counter = False
                                else:
                                    count = byte
                                    counter = False
                                    value = True
                            elif value:
                                for i in range(count + (self.MAXBYTES - 255)):
                                    dest_file.write(byte.to_bytes(1, 'big'))
                                value = False
                            else:
                                dest_file.write(byte.to_bytes(1, 'big'))
                        chunk = src_file.read(self.chunk_size)
                    if counter:
                        dest_file.write(ord(self.MARKER).to_bytes(1, 'big'))
            else:
                raise RLedError
        return 0

#### Python, Simon Bullik, 2017-11-20
# Runlength Encoder als Klasse
# Eine binaere Datei auslesen,komprimieren und danach wieder herstellen
# komprimierte Datei hat die Endung *.rld
# wiederhergestellte Datei erhaelt eine name.bmp -> name1.bmp
# Themen: Ein-, Ausgabe, Schleife, UP, Dateihandling
# Dateiformat
# Endeerkennung
#

import glob
import os
import argparse


class RLed(object):
    """ Runlength Encoder als Klasse """
    #: escape sequence - seperates token and counters
    #: 0x90 is going to be 0x90 0x00
    MARKER = chr(0x90)
    #: max number of repetions for compress_simple
    #: 1 represents 4 repetitions
    MAXBYTES_SIMPLE = 131
    #: max number of repetions for compress
    #: 1 represents 4 repetitions
    MAXBYTES = 258

    def __init__(self):
        """Voreinstelllungen"""
        """self.compress = True"""
        self.quiet = False
        self.extension = "rld"
        self.chunk_size = 4096

    def compress(self, sourcefile):
        """runlength compressing for any type of file
        @param sourcefile: The file including path that should be compressed
        @type sourcefile: string
        @return: Nothing

        It contains two paragraphs."""
        with open(sourcefile, 'rb') as src_file, open(os.path.splitext(sourcefile)[0] + "." + self.extension,
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

    def expand(self, sourcefile):
        """runlength expanding for files which were\
           compressed with compress method
        @param sourcefile: The file including path that should be compressed
        @type sourcefile: string
        @return: Nothing"""
        with open(sourcefile, 'rb') as src_file:
            if src_file.read(3) == b'rl3':
                extension_counter = src_file.read(1)
                extension_orig = src_file.read(int.from_bytes(extension_counter, 'big'))
                with open(os.path.splitext(sourcefile)[0] + "." + extension_orig.decode("utf-8"),
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
                print("Falsche Komprimierung")

    def compress_simple(self, sourcefile):
        """runlength compressing for ASCII files only\
           raises ValueError if it encounters chars bigger than 127
        @param sourcefile: The file including path that should be compressed
        @type sourcefile: string
        @return: Nothing"""
        with open(sourcefile, 'rb') as src_file, open(os.path.splitext(sourcefile)[0] + "." + self.extension,
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
                    if last_byte is not None and last_byte == byte and counter < self.MAXBYTES_SIMPLE:
                        counter += 1
                    else:
                        if last_byte is not None:
                            if last_byte < 128:
                                if counter != 1:
                                    dest_file.write((counter + (255 - self.MAXBYTES_SIMPLE)).to_bytes(1, 'big'))
                                dest_file.write(last_byte.to_bytes(1, 'big'))
                            else:
                                print("Wrong Character: " + str(last_byte))
                            counter = 1
                    last_byte = byte
                if last_byte < self.MAXBYTES_SIMPLE:
                    if counter != 1:
                        dest_file.write((counter + (255 - self.MAXBYTES_SIMPLE)).to_bytes(1, 'big'))
                    dest_file.write(last_byte.to_bytes(1, 'big'))
                else:
                    print("Wrong Character: " + str(last_byte))
                counter = 1
                chunk = src_file.read(self.chunk_size)

    def expand_simple(self, sourcefile):
        """runlength expanding for files which were\
           compressed with compress_simple method
        @param sourcefile: The file including path that should be compressed
        @type sourcefile: string
        @return: Nothing"""
        with open(sourcefile, 'rb') as src_file:
            if src_file.read(3) == b'rl2':
                extension_counter = src_file.read(1)
                extension_orig = src_file.read(int.from_bytes(extension_counter, 'big'))
                with open(os.path.splitext(sourcefile)[0] + "." + extension_orig.decode("utf-8"),
                          'wb') as dest_file:
                    chunk = src_file.read(self.chunk_size)
                    count = 0
                    while chunk:
                        for byte in chunk:
                            if count == 0:
                                if byte > 127:
                                    count = byte - (255 - self.MAXBYTES_SIMPLE)
                                else:
                                    dest_file.write(byte.to_bytes(1, 'big'))
                            else:
                                for i in range(count):
                                    dest_file.write(byte.to_bytes(1, 'big'))
                                count = 0
                        chunk = src_file.read(self.chunk_size)
            else:
                print("Falsche Komprimierung")

    def setStatusQuiet(self):
        """verboose level, we do not see messages on the screen"""
        self.quiet = True

    def setStatusVerboose(self):
        """verboose level, we see messages on the screen"""
        self.quiet = False

    def setExtension(self, ext="rld"):
        """sets extension of destination file"""
        self.extension = ext


if __name__ == "__main__":
    """for file in glob.glob("test_files/*"):
        if "_expanded" not in file and ".rld" not in file:
            rled = RLed()
            rled.compress(file)
            rled.expand(os.path.splitext(file)[0] + ".rld")
    """
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("-c", "--compress", action="store_true", help="→ komprimieren")
    action.add_argument("-u", "--uncompress", action="store_true", help="→ expandieren")
    parser.add_argument("-f", "--file", help="", required=True)
    parser.add_argument("-e", "--extension", help="", required=False)
    parser.add_argument("-q", "--quiet", action="store_true", help="", required=False)
    args = parser.parse_args()

    if args.extension is None:
        extension = "rld"
    else:
        extension = args.extension

    outputfile = os.path.splitext(args.file)[0]
    if os.path.isfile(outputfile + "." + extension):
        if " (" in outputfile:
            outputfile = outputfile.split(" (")[0]
        number = 1
        while os.path.isfile(outputfile + " (" + str(number) + ")." + extension):
            number += 1
        outputfile += " (" + str(number) + ")"

    rld = RLed()
    if args.compress:
        rld.compress(args.file)
    elif args.uncompress:
        with open(args.file, 'rb') as src_file:
            identifier = src_file.read(3)
        if identifier == b'rl2':
            rld.expand_simple(args.file)
        elif identifier == b'rl3':
            rld.expand(args.file)
        else:
            print("Die Datei ist nicht mit RL2 oder RL3 komprimiert")
exit()

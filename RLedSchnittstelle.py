#### Python, wol, 2009-08-20
# Runlength Encoder als Klasse
# Eine binaere Datei auslesen,komprimieren und danach wieder herstellen
# komprimierte Datei hat die Endung *.rld
# wiederhergestellte Datei erhaelt eine name.bmp -> name1.bmp
# Themen: Ein-, Ausgabe, Schleife, UP, Dateihandling
# Dateiformat
# Endeerkennung
#

import sys, os, RL2, RL3


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
        self.rld = None

    def compress(self, source_file):
        """runlength compressing for any type of file
        @param source_file: The file including path that should be compressed
        @type source_file: string
        @return: Nothing

        It contains two paragraphs."""
        self.rld = RL3.RL3()
        self.rld.MARKER = self.MARKER
        self.rld.MAXBYTES = self.MAXBYTES
        destination_file = os.path.splitext(source_file)[0] + "." + self.extension
        try:
            self.rld.compress(source_file, destination_file)
        except Exception as inst:
            if not self.quiet:
                raise inst
            else:
                sys.exit(4)

    def expand(self, source_file):
        """runlength expanding for files which were\
           compressed with compress method
        @param source_file: The file including path that should be compressed
        @type source_file: string
        @return: Nothing"""
        self.rld = RL3.RL3()
        self.rld.MARKER = self.MARKER
        self.rld.MAXBYTES = self.MAXBYTES
        with open(source_file, 'rb') as src_file:
            if src_file.read(3) == b'rl3':
                extension_counter = src_file.read(1)
                extension_orig = src_file.read(int.from_bytes(extension_counter, 'big'))
                outputfile = os.path.splitext(source_file)[0]
                if os.path.isfile(outputfile + "." + extension_orig.decode("utf-8")):
                    number = 1
                    while os.path.isfile(outputfile + str(number) + "." + extension_orig.decode("utf-8")):
                        number += 1
                    outputfile += str(number)
                outputfile += "." + extension_orig.decode("utf-8")
                try:
                    self.rld.expand(source_file, outputfile)
                except Exception as inst:
                    if not self.quiet:
                        raise inst
                    else:
                        sys.exit(4)

    def compress_simple(self, source_file):
        """runlength compressing for ASCII files only\
           raises ValueError if it encounters chars bigger than 127
        @param source_file: The file including path that should be compressed
        @type source_file: string
        @return: Nothing"""
        self.rld = RL2.RL2()
        self.rld.MAXBYTES = self.MAXBYTES_SIMPLE
        destination_file = os.path.splitext(source_file)[0] + "." + self.extension
        try:
            self.rld.compress(source_file, destination_file)
        except Exception as inst:
            if not self.quiet:
                raise inst
            else:
                sys.exit(4)

    def expand_simple(self, source_file):
        """runlength expanding for files which were\
           compressed with compress_simple method
        @param source_file: The file including path that should be compressed
        @type source_file: string
        @return: Nothing"""
        self.rld = RL2.RL2()
        self.rld.MAXBYTES = self.MAXBYTES_SIMPLE
        with open(source_file, 'rb') as src_file:
            if src_file.read(3) == b'rl2':
                extension_counter = src_file.read(1)
                extension_orig = src_file.read(int.from_bytes(extension_counter, 'big'))
                outputfile = os.path.splitext(source_file)[0]
                if os.path.isfile(outputfile + "." + extension_orig.decode("utf-8")):
                    number = 1
                    while os.path.isfile(outputfile + str(number) + "." + extension_orig.decode("utf-8")):
                        number += 1
                    outputfile += str(number)
                outputfile += "." + extension_orig.decode("utf-8")
                try:
                    self.rld.expand(source_file, outputfile)
                except Exception as inst:
                    if not self.quiet:
                        raise inst
                    else:
                        sys.exit(4)

    def setStatusQuiet(self):
        """verboose level, we do not see messages on the screen"""
        self.quiet = True

    def setStatusVerboose(self):
        """verboose level, we see messages on the screen"""
        self.quiet = False

    def setExtension(self, ext="rld"):
        """sets extension of destination file"""
        self.extension = ext

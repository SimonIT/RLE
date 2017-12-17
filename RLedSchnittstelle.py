#### Python, wol, 2009-08-20
# Runlength Encoder als Klasse
# Eine binaere Datei auslesen,komprimieren und danach wieder herstellen
# komprimierte Datei hat die Endung *.rld
# wiederhergestellte Datei erhaelt eine name.bmp -> name1.bmp
# Themen: Ein-, Ausgabe, Schleife, UP, Dateihandling
# Dateiformat
# Endeerkennung
#

import RL2
import RL3
import RLedException
import os
import sys


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
        self.quiet = False  # Ausgaben standardmäßig anschalten
        self.extension = "rld"  # Setze die Standarddateiendung auf rld
        self.rld = None  # rld auf none

    def compress(self, source_file):
        """runlength compressing for any type of file
        @param source_file: The file including path that should be compressed
        @type source_file: string
        @return: Nothing

        It contains two paragraphs."""
        self.rld = RL3.RL3()  # Erstelle ein neues RL3 Objekt
        self.rld.MARKER = self.MARKER  # Setze den Marker im Objekt
        self.rld.MAXBYTES = self.MAXBYTES  # Setze die Maximale Byteanzahl
        destination_file = os.path.splitext(source_file)[
                               0] + "." + self.extension  # Erstelle den Namen der Ausgabedatei, mit dem Namen der Eingabedatei und der eingegeben Dateiendung
        try:
            self.rld.compress(source_file, destination_file)  # Komprimiere die eingebene Datei
        except RLedException.RLedError as inst:  # Wenn ein RLedError auftritt
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(4)  # Beende das Programm mit dem Code 4
        except OSError as inst:  # Wenn ein Fehler bei den Dateien auftritt
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(2)  # Beende das Programm mit dem Code 2
        except Exception as inst:  # Bei allen anderen Fehlern
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(5)  # Beende das Programm mit dem Code 5

    def expand(self, source_file):
        """runlength expanding for files which were\
           compressed with compress method
        @param source_file: The file including path that should be compressed
        @type source_file: string
        @return: Nothing"""
        self.rld = RL3.RL3()  # Erstelle ein neues RL3 Objekt
        self.rld.MARKER = self.MARKER  # Setze den Marker im Objekt
        self.rld.MAXBYTES = self.MAXBYTES  # Setze die Maximale Byteanzahl
        try:
            self.rld.expand(source_file)  # Expandiere die Datei
        except RLedException.RLedError as inst:  # Wenn ein RLedError auftritt
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(4)  # Beende das Programm mit dem Code 4
        except OSError as inst:  # Wenn ein Fehler bei den Dateien auftritt
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(2)  # Beende das Programm mit dem Code 2
        except Exception as inst:  # Bei allen anderen Fehlern
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(5)  # Beende das Programm mit dem Code 5

    def compress_simple(self, source_file):
        """runlength compressing for ASCII files only\
           raises ValueError if it encounters chars bigger than 127
        @param source_file: The file including path that should be compressed
        @type source_file: string
        @return: Nothing"""
        self.rld = RL2.RL2()  # Erstelle ein neues RL2 Objekt
        self.rld.MAXBYTES = self.MAXBYTES_SIMPLE  # Setze die Maximale Byteanzahl
        destination_file = os.path.splitext(source_file)[
                               0] + "." + self.extension  # Erstelle den Namen der Ausgabedatei, mit dem Namen der Eingabedatei und der eingegeben Dateiendung
        try:
            self.rld.compress(source_file, destination_file)
        except RLedException.RLedError as inst:  # Wenn ein RLedError auftritt
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(4)  # Beende das Programm mit dem Code 4
        except OSError as inst:  # Wenn ein Fehler bei den Dateien auftritt
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(2)  # Beende das Programm mit dem Code 2
        except Exception as inst:  # Bei allen anderen Fehlern
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(5)  # Beende das Programm mit dem Code 5

    def expand_simple(self, source_file):
        """runlength expanding for files which were\
           compressed with compress_simple method
        @param source_file: The file including path that should be compressed
        @type source_file: string
        @return: Nothing"""
        self.rld = RL2.RL2()  # Erstelle ein neues RL2 Objekt
        self.rld.MAXBYTES = self.MAXBYTES_SIMPLE  # Setze die Maximale Byteanzahl
        try:
            self.rld.expand(source_file)
        except RLedException.RLedError as inst:  # Wenn ein RLedError auftritt
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(4)  # Beende das Programm mit dem Code 4
        except OSError as inst:  # Wenn ein Fehler bei den Dateien auftritt
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(2)  # Beende das Programm mit dem Code 2
        except Exception as inst:  # Bei allen anderen Fehlern
            if not self.quiet:  # Wenn Ausgaben erlaubt sind
                raise inst  # Werfe den Fehler
            else:  # Wenn Ausgaben nicht erlaubt sind
                sys.exit(5)  # Beende das Programm mit dem Code 5

    def setStatusQuiet(self):
        """verboose level, we do not see messages on the screen"""
        self.quiet = True

    def setStatusVerboose(self):
        """verboose level, we see messages on the screen"""
        self.quiet = False

    def setExtension(self, ext="rld"):
        """sets extension of destination file"""
        self.extension = ext

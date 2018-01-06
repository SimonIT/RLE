##########################################################################################
#  Namen:      Simon Bullik                                                              #
#  Prog-Name:  RL2.py                            Klasse DQI16                            #
#  Version:    1.0                                                                       #
#  Python:     3.6                               Datum:      2017.12.17                  #
#  OS:         Windows 10                                                                #
##########################################################################################
import os
from RLedInterface import RL
from RLedException import RLedError


class RL2(RL):
    def __init__(self):
        """Voreinstelllungen"""
        super().__init__()
        self.MAXBYTES = 131  # Setze die maximale zusammengefasste Bytezahl

    def compress(self, sourcefile, destinationfile):
        """runlength compressing for ASCII files only\
           raises ValueError if it encounters chars bigger than 127
        @param sourcefile: The file including path that should be compressed
        @param destinationfile: The new file including path that should be created
        @type sourcefile: string
        @type destinationfile: string
        @return: Nothing"""
        with open(sourcefile, 'rb') as src_file, open(destinationfile,
                                                      'wb') as dest_file:  # Öffne die zu Komprimierende Datei und die neue Datei
            dest_file.write(bytes("rl2", 'utf-8'))  # Schreibe rl2 in die neue Datei zur Algorythmuserkennung
            extension_orig = bytes(os.path.splitext(sourcefile)[1][1:], 'utf-8')  # Splitte die Dateiendung
            dest_file.write(len(extension_orig).to_bytes(1, 'big'))  # Schreibe die Länge der Dateiendung
            dest_file.write(extension_orig)  # Schreibe die Dateiendung
            counter = 1  # Setze den Wiederhohlungszähler auf 1
            last_byte = None  # Erstelle die leere Variable mit dem letzten Byte
            chunk = src_file.read(self.chunk_size)  # Liest Bytes aus
            while chunk:  # Solange Bytes existieren
                for byte in chunk:  # Für jedes Bytes
                    if last_byte is not None and last_byte == byte and counter < self.MAXBYTES:  # Wenn das letzte Byte gleich dem neuen Byts ist und die Anzahl nicht überschritten worden ist
                        counter += 1  # Erhöhe den Zähler
                    else:  # Sonst
                        if last_byte is not None:  # Wenn das letzte Byte existiert
                            if last_byte < 128:  # Wenn das letzte Byte ein gültiges ASCII Zeichen ist
                                if counter > (self.MAXBYTES - 128):  # Wenn der Counter nicht nicht eins ist
                                    dest_file.write(
                                        (counter + (255 - self.MAXBYTES)).to_bytes(1, 'big'))  # Schreibe den Counter
                                    dest_file.write(last_byte.to_bytes(1, 'big'))  # Schreibe den Wert
                                else:
                                    for i in range(counter):
                                        dest_file.write(last_byte.to_bytes(1, 'big'))  # Schreibe den Wert
                            else:  # Sonst
                                raise RLedError  # Werfe den RLedError
                            counter = 1  # Setze den Zähler auf 1 zurück
                    last_byte = byte  # Merke das aktuelle Byte für den Vergleich
                chunk = src_file.read(self.chunk_size)  # Lese die neuen Bytes aus
            if last_byte < 128:  # Wenn das letzte Byte ein gültiges ASCII Zeichen ist
                if counter > (self.MAXBYTES - 128):  # Wenn der Counter nicht nicht eins ist
                    dest_file.write(
                        (counter + (255 - self.MAXBYTES)).to_bytes(1, 'big'))  # Schreibe den Counter
                    dest_file.write(last_byte.to_bytes(1, 'big'))  # Schreibe den Wert
                else:
                    for i in range(counter):
                        dest_file.write(last_byte.to_bytes(1, 'big'))  # Schreibe den Wert
            else:  # Sonst
                raise RLedError  # Werfe den RLedError

    def expand(self, sourcefile):
        """runlength expanding for files which were\
           compressed with compress_simple method
        @param sourcefile: The file including path that should be compressed
        @type sourcefile: string
        @return: Nothing"""
        with open(sourcefile, 'rb') as src_file:  # Öffne die zu expandierende Datei
            if src_file.read(3) == b'rl2':  # Wenn sie eine RL2 Datei ist
                extension_counter = src_file.read(1)  # Lese die Anzahl der Bytes der Endung aus
                extension_orig = src_file.read(
                    int.from_bytes(extension_counter, 'big'))  # Lese die Endung auf Basis der Anzahl aus
                outputfile = os.path.splitext(sourcefile)[0]  # Splitte den Dateinamen vom Pfad
                if os.path.isfile(
                        outputfile + "." + extension_orig.decode("utf-8")):  # Überprüfe ob die Datei existiert
                    number = 1  # Setz Dateinummer auf eins
                    while os.path.isfile(outputfile + str(number) + "." + extension_orig.decode(
                            "utf-8")):  # Wiederhohle solange bis die Datei nicht existiert
                        number += 1  # Erhöhe die Dateinummer
                    outputfile += str(number)  # Füge dem Dateiname die Nummer hinzu
                outputfile += "." + extension_orig.decode("utf-8")  # Füge dem Dateinamen die Endung hinzu
                with open(outputfile, 'wb') as dest_file:  # Öffne die Zieldatei
                    chunk = src_file.read(self.chunk_size)  # Lese die Bytes aus
                    count = 0  # Setz die Nzahl auf 0
                    while chunk:  # Solange Bytes da sind
                        for byte in chunk:  # Gehe durch jedes Byte
                            if count == 0:  # Wenn die Anzahl null ist
                                if byte > 127:  # Wenn das Byte kein ASCII Zeichen ist
                                    count = byte - (255 - self.MAXBYTES)  # Setze den Zähler auf die Anzahl
                                else:  # Sonst
                                    dest_file.write(byte.to_bytes(1, 'big'))  # Schreibe das Byte
                            else:  # Sonst
                                for i in range(count):  # Für die Anzahl im Zähler
                                    dest_file.write(byte.to_bytes(1, 'big'))  # Schreibe die Bytes
                                count = 0  # Zurücksetzen des Zählers
                        chunk = src_file.read(self.chunk_size)  # Lese neue Bytes ein
            else:  # Sonst
                raise RLedError  # Werfe den RLedError

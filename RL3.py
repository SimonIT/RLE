##########################################################################################
#  Namen:      Simon Bullik                                                              #
#  Prog-Name:  RL3.py                            Klasse DQI16                            #
#  Version:    1.0                                                                       #
#  Python:     3.6                               Datum:      2017.12.17                  #
#  OS:         Windows 10                                                                #
##########################################################################################
import os
from RLedInterface import RL
from RLedException import RLedError


class RL3(RL):
    def __init__(self):
        """Voreinstelllungen"""
        super().__init__()
        self.MARKER = chr(0x90)  # Setze das Markierungszeichen für den Zähler
        self.MAXBYTES = 258  # Setze die maximale zusammengefasste Bytezahl

    def compress(self, sourcefile, destinationfile):
        """runlength compressing for any type of file
        @param sourcefile: The file including path that should be compressed
        @param destinationfile: The new file including path that should be created
        @type sourcefile: string
        @type destinationfile: string
        @return: Nothing

        It contains two paragraphs."""
        with open(sourcefile, 'rb') as src_file, open(destinationfile,
                                                      'wb') as dest_file:  # Öffne die Quell- und Zieldatei
            dest_file.write(bytes("rl3", 'utf-8'))  # Schreibe rl3 in die neue Datei zur Algorythmuserkennung
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
                            if counter > (self.MAXBYTES - 255):  # Wenn es sich lohnt zu komprimieren
                                dest_file.write(ord(self.MARKER).to_bytes(1, 'big'))  # Schreibe das Markierungszeichen
                                dest_file.write((counter - (self.MAXBYTES - 255)).to_bytes(1,
                                                                                           'big'))  # Schreibe die Anzahl der Wiederhohlungen des Zeichen
                                dest_file.write(last_byte.to_bytes(1, 'big'))  # Schreibe das Zeichen
                            else:  # Sonst
                                for i in range(counter):  # Für die Anzahl der zeichen
                                    dest_file.write(last_byte.to_bytes(1, 'big'))  # Schreibe das Zeichen
                                    if last_byte == ord(
                                            self.MARKER):  # Wenn das Zeichen gleich dem Markierungzeichen ist
                                        dest_file.write(b'\x00')  # Schreibe 0 dahinter
                            counter = 1  # Setze den Zähler auf 1 zurück
                    last_byte = byte  # Merke das aktuelle Byte für den Vergleich
                chunk = src_file.read(self.chunk_size)  # Lese die neuen Bytes aus
            if counter > (self.MAXBYTES - 255):  # Wenn es sich lohnt zu komprimieren
                dest_file.write(ord(self.MARKER).to_bytes(1, 'big'))  # Schreibe das Markierungszeichen
                dest_file.write((counter - (self.MAXBYTES - 255)).to_bytes(1,
                                                                           'big'))  # Schreibe die Anzahl der Wiederhohlungen des Zeichen
                dest_file.write(last_byte.to_bytes(1, 'big'))  # Schreibe das Zeichen
            else:  # Sonst
                for i in range(counter):  # Für die Anzahl der zeichen
                    dest_file.write(last_byte.to_bytes(1, 'big'))  # Schreibe das Zeichen
                    if last_byte == ord(self.MARKER):  # Wenn das Zeichen gleich dem Markierungzeichen ist
                        dest_file.write(b'\x00')  # Schreibe 0 dahinter

    def expand(self, sourcefile):
        """runlength expanding for files which were\
           compressed with compress method
        @param sourcefile: The file including path that should be compressed
        @type sourcefile: string
        @return: Nothing"""
        with open(sourcefile, 'rb') as src_file:  # Öffne die zu expandierende Datei
            if src_file.read(3) == b'rl3':  # Wenn sie eine RL3 Datei ist
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
                    counter = False  # Aktuelles Byte ist keine Zähler
                    value = False  # Aktuelles Byte ist nicht der Wert
                    count = 0  # Null Wiederhohlungen vom Wert
                    while chunk:  # Solange Bytes da sind
                        for byte in chunk:  # Gehe durch jedes Byte
                            if byte == ord(
                                    self.MARKER) and not counter and not value:  # Wenn das Byte ein Markierungszeichen ist und Zähler und Wert nicht aktiv sind
                                counter = True  # Aktiviere den Zähler
                            elif counter:  # Wenn der Zähler aktiv ist
                                if byte == 0:  # Wenn das aktuelle Byte null ist
                                    dest_file.write(ord(self.MARKER).to_bytes(1, 'big'))  # Schreibe den Marker
                                    counter = False  # Desktiviere den Zähler
                                else:  # Sonst
                                    count = byte  # Setze die Anzahl auf den Wert des Bytes
                                    counter = False  # Deaktiviere den Zähler
                                    value = True  # Aktiviere den Wert
                            elif value:  # Wenn der Wert aktiv ist
                                for i in range(count + (self.MAXBYTES - 255)):  # Für die Aazahl im Zähler
                                    dest_file.write(byte.to_bytes(1, 'big'))  # Schreibe die Bytes
                                value = False  # Deaktiviere den Wert
                            else:  # Sonst
                                dest_file.write(byte.to_bytes(1, 'big'))  # Schreibe das Byte
                        chunk = src_file.read(self.chunk_size)  # Lese neue Bytes ein
                    if counter:  # Wenn der Zähler aktiv ist
                        dest_file.write(ord(self.MARKER).to_bytes(1, 'big'))  # Schreibe den Marker
            else:  # Sonst
                raise RLedError  # Werfe den RLedError

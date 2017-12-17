import glob
import sys
import os
import argparse
import RLedSchnittstelle
import RLedException

if __name__ == "__main__":
    # Schneller Test für alle testfiles
    # for file in glob.glob("test_files/*txt"):
    #   if "_expanded" not in file and ".rld" not in file:
    #       rled = RLedSchnittstelle.RLed()
    #       rled.compress_simple(file)
    #       rled.expand_simple(os.path.splitext(file)[0] + ".rld")
    # for file in glob.glob("test_files/*"):
    #    if "_expanded" not in file and ".rld" not in file:
    #        rled = RLedSchnittstelle.RLed()
    #        rled.compress(file)
    #        rled.expand(os.path.splitext(file)[0] + ".rld")
    parser = argparse.ArgumentParser()  # Erstelle einen neuen Argumentparser
    action = parser.add_mutually_exclusive_group(required=True)  # Füge eine neue entweder oder Gruppe hinzu
    action.add_argument("-c", "--compress", action="store_true", help="→ komprimieren")  # Entweder komprimieren
    action.add_argument("-u", "--uncompress", action="store_true", help="→ expandieren")  # oder dekomprimieren
    parser.add_argument("-f", "--file", help="file to (un)compress", required=True)  # Eingabepfad der Datei
    parser.add_argument("-e", "--extension", help="Default: .rld", required=False)  # Eigene Dateiendung
    parser.add_argument("-q", "--quiet", action="store_true", help="", required=False)  # Sollen Ausgaben gemacht werden
    try:
        args = parser.parse_args()  # Verarbeite die Argumente
    except:  # Bei Fehlern
        sys.exit(1)  # Beende mit Code 1

    rld = RLedSchnittstelle.RLed()  # Erstelle ein neues Objekt der zur Verfügung gestellten Schnittstelle

    if args.quiet:  # Wenn keine Ausgaben gemacht werden sollen
        rld.setStatusQuiet()  # Setze Objekt auf "Leise"

    if args.extension is not None:  # Wenn eine Dateiendung übergeben wurde
        rld.setExtension(args.extension)  # Setze die Dateiendung

    if args.compress:  # Wenn die Datei komprimiert werden soll
        rld.compress(args.file)  # Komprimiere die Datei mit RL3
    elif args.uncompress:  # Wenn die Datei deomprimiert werden soll
        with open(args.file, 'rb') as src_file:  # Öffne die Datei
            identifier = src_file.read(3)  # Lese aus, welche Komprimierung genutzt wurde
        if identifier == b'rl2':  # Wenn RL2 genutzt wurde
            rld.expand_simple(args.file)  # dann dekomprimiere mit RL2
        elif identifier == b'rl3':  # wenn RL3 genutzt wurde
            rld.expand(args.file)  # dann dekomprimiere mit RL3
        else:  # sonst
            if args.quiet:  # wenn keine Ausgaben gemacht werden sollen
                sys.exit(4)  # beende das Prgramm mit Code 4
            else:  # sonst
                raise RLedException.RLedError()  # werfe den RLedError
sys.exit(0)  # Bei Erfolg beende mit Code 0

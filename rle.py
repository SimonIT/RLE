import argparse


def compress_rl2(source_file, destination_file):  # -> Exception bei Zeichen > 0x7F in source_file
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            counter = 1
            last_byte = src_file.read(1)
            byte = src_file.read(1)
            while last_byte:
                if last_byte == byte and counter < 127:
                    counter += 1
                else:
                    if int.from_bytes(last_byte, 'big') < 128:
                        if counter != 1:
                            dest_file.write((counter + 128).to_bytes(1, 'big'))
                        dest_file.write(last_byte)
                    else:
                        print("Wrong Character: " + str(last_byte.hex()))
                    counter = 1
                last_byte = byte
                byte = src_file.read(1)


def expand_rl2(source_file, destination_file):
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            last_byte = src_file.read(1)
            byte = src_file.read(1)
            while last_byte:
                if int.from_bytes(last_byte, 'big') > 128:
                    counter = int.from_bytes(last_byte, 'big') - 128
                    for i in range(counter):
                        dest_file.write(byte)
                    last_byte = src_file.read(1)
                else:
                    dest_file.write(last_byte)
                    last_byte = byte
                byte = src_file.read(1)


def compress_rl3(source_file, destination_file):
    counter_char = b'\x90'
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            counter = 1
            last_byte = src_file.read(1)
            byte = src_file.read(1)
            while last_byte:
                if last_byte == byte and counter < 255:
                    counter += 1
                else:
                    if counter > 2:
                        dest_file.write(counter_char)
                        dest_file.write(counter.to_bytes(1, 'big'))
                        dest_file.write(last_byte)
                    else:
                        for i in range(counter):
                            dest_file.write(last_byte)
                            if last_byte == counter_char:
                                dest_file.write(b'\x00')
                    counter = 1
                last_byte = byte
                byte = src_file.read(1)


def expand_rl3(source_file, destination_file):
    counter_char = b'\x90'
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            last_byte = src_file.read(1)
            byte = src_file.read(1)
            while last_byte:
                if last_byte == counter_char:
                    if byte == b'\x00':
                        dest_file.write(last_byte)
                    else:
                        counter = int.from_bytes(byte, 'big')
                        value = src_file.read(1)
                        for i in range(counter):
                            dest_file.write(value)
                    last_byte = src_file.read(1)
                else:
                    dest_file.write(last_byte)
                    last_byte = byte
                byte = src_file.read(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--compress", action="store_true", help="→ komprimieren")
    parser.add_argument("-d", "--uncompress", action="store_true", help="→ expandieren")
    parser.add_argument("-i", "--inputfile", help="")
    parser.add_argument("-o", "--outputfile", help="")
    parser.add_argument("-t2", "--type2", action="store_true", help="Typ2 des Algorithmus")
    parser.add_argument("-t3", "--type3", action="store_true", help="Typ3 des Algorithmus")
    parser.add_argument("-e", "--extension", help="")
    parser.add_argument("-q", "--quiet", action="store_true", help="")
    args = parser.parse_args()

    if args.extension is None:
        extension = ""
    else:
        extension = args.extension

    if args.compress:
        if args.type2:
            compress_rl2(args.inputfile, args.outputfile + extension)
        else:
            compress_rl3(args.inputfile, args.outputfile + extension)
    elif args.uncompress:
        if args.type2:
            expand_rl2(args.inputfile, args.outputfile + extension)
        else:
            expand_rl3(args.inputfile, args.outputfile + extension)
    else:
        print("Komprimieren oder Dekomprimieren auswählen!")
    exit()

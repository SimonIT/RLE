import argparse
import os.path


def compress_rl2(source_file, destination_file):  # -> Exception bei Zeichen > 0x7F in source_file
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            counter = 1
            last_byte = None
            chunk = src_file.read(4096)
            while chunk:
                for byte in chunk:
                    if last_byte is not None and last_byte == byte and counter < 131:
                        counter += 1
                    else:
                        if last_byte is not None:
                            if last_byte < 128:
                                if counter != 1:
                                    dest_file.write((counter + 124).to_bytes(1, 'big'))
                                dest_file.write(last_byte.to_bytes(1, 'big'))
                            else:
                                print("Wrong Character: " + str(last_byte))
                            counter = 1
                    last_byte = byte
                if last_byte < 128:
                    if counter != 1:
                        dest_file.write((counter + 124).to_bytes(1, 'big'))
                    dest_file.write(last_byte.to_bytes(1, 'big'))
                else:
                    print("Wrong Character: " + str(last_byte))
                counter = 1
                chunk = src_file.read(4096)


def expand_rl2(source_file, destination_file):
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            chunk = src_file.read(4096)
            count = 0
            while chunk:
                for byte in chunk:
                    if count == 0:
                        if byte > 127:
                            count = byte - 124
                        else:
                            dest_file.write(byte.to_bytes(1, 'big'))
                    else:
                        for i in range(count):
                            dest_file.write(byte.to_bytes(1, 'big'))
                        count = 0
                chunk = src_file.read(4096)


def compress_rl3(source_file, destination_file):
    counter_char = b'\x90'
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            counter = 1
            last_byte = None
            chunk = src_file.read(4096)
            while chunk:
                for byte in chunk:
                    if last_byte is not None and last_byte == byte and counter < 255:
                        counter += 1
                    else:
                        if last_byte is not None:
                            if counter > 2:
                                dest_file.write(counter_char)
                                dest_file.write(counter.to_bytes(1, 'big'))
                                dest_file.write(last_byte.to_bytes(1, 'big'))
                            else:
                                for i in range(counter):
                                    dest_file.write(last_byte.to_bytes(1, 'big'))
                                    if last_byte == counter_char:
                                        dest_file.write(b'\x00')
                            counter = 1
                    last_byte = byte
                if counter > 2:
                    dest_file.write(counter_char)
                    dest_file.write(counter.to_bytes(1, 'big'))
                    dest_file.write(last_byte.to_bytes(1, 'big'))
                else:
                    for i in range(counter):
                        dest_file.write(last_byte.to_bytes(1, 'big'))
                        if last_byte == counter_char:
                            dest_file.write(b'\x00')
                counter = 1
                chunk = src_file.read(4096)


def expand_rl3(source_file, destination_file):
    counter_char = 144
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            chunk = src_file.read(4096)
            counter = False
            value = False
            count = 0
            while chunk:
                for byte in chunk:
                    if byte == counter_char and not counter and not value:
                        counter = True
                    elif counter:
                        if byte == 0:
                            dest_file.write(counter_char.to_bytes(1, 'big'))
                            counter = False
                        else:
                            count = byte
                            counter = False
                            value = True
                    elif value:
                        for i in range(count):
                            dest_file.write(byte.to_bytes(1, 'big'))
                        value = False
                    else:
                        dest_file.write(byte.to_bytes(1, 'big'))
                chunk = src_file.read(4096)
            if counter:
                dest_file.write(counter_char.to_bytes(1, 'big'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("-c", "--compress", action="store_true", help="→ komprimieren")
    action.add_argument("-u", "--uncompress", action="store_true", help="→ expandieren")
    parser.add_argument("-f", "--file", help="", required=True)
    parser.add_argument("-e", "--extension", help="", required=False)
    parser.add_argument("-q", "--quiet", action="store_true", help="", required=False)
    args = parser.parse_args()

    if args.extension is None:
        extension = ""
    else:
        extension = args.extension

    outputfile = os.path.splitext(args.file)[0]

    if args.compress:
        if args.type2:
            compress_rl2(args.file, outputfile + extension)
        else:
            compress_rl3(args.file, outputfile + extension)
    elif args.uncompress:
        if args.type2:
            expand_rl2(args.file, outputfile + extension)
        else:
            expand_rl3(args.file, outputfile + extension)
    exit()

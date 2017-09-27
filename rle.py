import argparse


def compress_rl2(source_file, destination_file):  # -> Exception bei Zeichen > 0x7F in source_file
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            counter = 1
            lastbyte = src_file.read(1)
            byte = src_file.read(1)
            while lastbyte:
                if lastbyte == byte:
                    counter += 1
                else:
                    if int.from_bytes(lastbyte, 'big') < 128:
                        if counter != 1:
                            dest_file.write((counter + 128).to_bytes(1, 'big'))
                        dest_file.write(lastbyte)
                    counter = 1
                lastbyte = byte
                byte = src_file.read(1)


def expand_rl2(source_file, destination_file):
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            lastbyte = src_file.read(1)
            byte = src_file.read(1)
            while lastbyte:
                if int.from_bytes(lastbyte, 'big') > 128:
                    counter = int.from_bytes(lastbyte, 'big') - 128
                    for i in range(counter):
                        dest_file.write(byte)
                    lastbyte = src_file.read(1)
                    byte = src_file.read(1)
                else:
                    dest_file.write(lastbyte)
                    lastbyte = byte
                    byte = src_file.read(1)


def compress_rl3(source_file, destination_file):
    counter_char = b'\x90'
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            counter = 1
            lastbyte = src_file.read(1)
            byte = src_file.read(1)
            while lastbyte:
                if lastbyte == byte and counter < 255:
                    counter += 1
                else:
                    if counter > 2:
                        dest_file.write(counter_char)
                        print(counter)
                        dest_file.write(counter.to_bytes(1, 'big'))
                        dest_file.write(lastbyte)
                    else:
                        for i in range(counter):
                            dest_file.write(lastbyte)
                            if lastbyte == counter_char:
                                dest_file.write(b'\x00')
                    counter = 1
                lastbyte = byte
                byte = src_file.read(1)


def expand_rl3(source_file, destination_file):
    counter_char = b'\x90'
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            lastbyte = src_file.read(1)
            byte = src_file.read(1)
            while lastbyte:
                if lastbyte == counter_char:
                    if byte == b'\x00':
                        dest_file.write(lastbyte)
                        lastbyte = byte
                        byte = src_file.read(1)
                    else:
                        counter = int.from_bytes(byte, 'big')
                        value = src_file.read(1)
                        for i in range(counter):
                            dest_file.write(value)
                        lastbyte = src_file.read(1)
                        byte = src_file.read(1)
                else:
                    dest_file.write(lastbyte)
                    lastbyte = byte
                    byte = src_file.read(1)


if __name__ == "__main__":
    compress_rl2("test_files/test.txt", "compress.rl2")
    expand_rl2("compress.rl2", "test.orig.txt")
    compress_rl3("test_files/bild.bmp", "compress.rl3")
    expand_rl3("compress.rl3", "test2.bmp")
    compress_rl3("test_files/kirby.bmp", "compress2.rl3")
    expand_rl3("compress2.rl3", "test.bmp")
    exit()

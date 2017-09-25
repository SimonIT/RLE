def compress_rl2(source_file, destination_file):  # -> Exception bei Zeichen > 0x7F in source_file
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            counter = 1
            byte = src_file.read(1)
            lastbyte = b""
            while byte:
                """if byte < b'\x80':
                    print("kleiner")
                else:
                    print("größer")"""
                if lastbyte == byte:
                    counter += 1
                else:
                    if lastbyte != b"":
                        if counter != 1:
                            dest_file.write((counter + 128).to_bytes(1, 'big'))
                        dest_file.write(lastbyte)
                        counter = 1
                lastbyte = byte
                byte = src_file.read(1)
            if counter != 1:
                dest_file.write((counter + 128).to_bytes(1, 'big'))
            dest_file.write(lastbyte)


def expand_rl2(source_file, destination_file):
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            byte = src_file.read(1)
            while byte:
                lastbyte = byte
                byte = src_file.read(1)
                if int.from_bytes(lastbyte, 'big') > 128:
                    counter = int.from_bytes(lastbyte, 'big') - 128
                    for i in range(counter):
                        dest_file.write(byte)
                else:
                    dest_file.write(byte)
                byte = src_file.read(1)


def compress_rl3(source_file, destination_file):
    counter_char = b'\x90'
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            counter = 1
            byte = src_file.read(1)
            lastbyte = b""
            while byte:
                if lastbyte == byte:
                    counter += 1
                else:
                    if lastbyte != b"":
                        if counter > 2:
                            dest_file.write(counter_char)
                            dest_file.write(counter.to_bytes(1, 'big'))
                        else:
                            dest_file.write(lastbyte)
                            if lastbyte == counter_char:
                                dest_file.write(b'\x00')
                        dest_file.write(lastbyte)
                        if lastbyte == counter_char:
                            dest_file.write(b'\x00')
                        counter = 1
                lastbyte = byte
                byte = src_file.read(1)
            if counter > 2:
                dest_file.write(counter_char)
                dest_file.write(counter.to_bytes(1, 'big'))
            else:
                dest_file.write(lastbyte)
                if lastbyte == counter_char:
                    dest_file.write(b'\x00')
            dest_file.write(lastbyte)
            if lastbyte == counter_char:
                dest_file.write(b'\x00')


def expand_rl3(source_file, destination_file):
    counter_char = b'\x90'
    with open(source_file, 'rb') as src_file:
        with open(destination_file, 'wb') as dest_file:
            byte = src_file.read(1)
            while byte:
                lastbyte = byte
                byte = src_file.read(1)
                if lastbyte == counter_char:
                    if byte == b'\x00':
                        dest_file.write(lastbyte)
                    else:
                        counter = int.from_bytes(byte, 'big')
                        value = src_file.read(1)
                        for i in range(counter):
                            dest_file.write(value)
                else:
                    dest_file.write(lastbyte)
                    dest_file.write(byte)
                byte = src_file.read(1)


if __name__ == "__main__":
    compress_rl2("test.txt", "test.rl2")
    compress_rl3("test2.hex", "test2.rl3")
    expand_rl2("test.rl2", "orig.txt")
    expand_rl3("test2.rl3", "orig2.hex")

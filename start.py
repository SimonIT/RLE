import glob
import sys
import os
import argparse
import RLedSchnittstelle
import RLedException

if __name__ == "__main__":
    """for file in glob.glob("test_files/*txt"):
        if "_expanded" not in file and ".rld" not in file:
            rled = RLedSchnittstelle.RLed()
            rled.setStatusQuiet()
            rled.compress_simple(file)
            rled.expand_simple(os.path.splitext(file)[0] + ".rld")
    """
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("-c", "--compress", action="store_true", help="→ komprimieren")
    action.add_argument("-u", "--uncompress", action="store_true", help="→ expandieren")
    parser.add_argument("-f", "--file", help="", required=True)
    parser.add_argument("-e", "--extension", help="", required=False)
    parser.add_argument("-q", "--quiet", action="store_true", help="", required=False)
    try:
        args = parser.parse_args()
    except:
        sys.exit(1)

    rld = RLedSchnittstelle.RLed()
    if args.extension is not None:
        rld.setExtension(args.extension)

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
            raise RLedException.RLedError()
exit()

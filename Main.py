"""
Main for Nand to Tetris project7, HUJI

Runs multiple conversions from .vm (virtual machine language) files to .asm
language files.
Authors: Shimon Heimowitz, Karin Sorokin

"""

import sys
import os
import traceback
from Analyzer import Analyzer

FILE_PATH = 1

FILE_EXTENSION_JACK = '.jack'
FILE_EXTENSION_VM = '.vm'
FILE_EXTENSION_XML = '.xml'


def main(path, no_tokenize=True, no_compile=False):
    """
    Main Compiler. Checks legality of arguments and operates on directory
    or file accordingly.
    :param path: argument
    """
    jack_files = []
    if not os.path.exists(path):
        print("Error: File or directory does not exist: %s"
              % path)
        return

    elif os.path.isdir(path):  # Directory of files
        jack_files = filter_paths(path)
        dir_path = path
        file_name = os.path.basename(path) + FILE_EXTENSION_XML
        if not jack_files:  # no vm files found
            print("Error: No files matching %s found in supplied "
                  "directory: %s" % (FILE_EXTENSION_JACK, path))
            return

    elif os.path.isfile(path):  # Single file
        if not path.endswith(FILE_EXTENSION_JACK):
            print("Error: Mismatched file type.\n\"%s\"suffix is not a valid "
                  "file type. Please supply .jack filename or dir." % path)
            return
        jack_files.append(path)
        dir_path = os.path.dirname(path)
        file_name = os.path.splitext(os.path.basename(path))[0] + \
                    FILE_EXTENSION_XML

    else:
        print("Error: Unrecognized path: \"%s\"\n"
              "Please supply dir or path/filename.vm")
        return

    try:
        # Initilizes write based, using a condition for multiple file reading.
        # Multiple files have a special initialization
        analyzer = Analyzer()


        for jack_file in jack_files:
            if not no_tokenize:
                analyzer.tokenize(os.path.join(dir_path, jack_file))
            if not no_compile:
                analyzer.tokenize(os.path.join(dir_path, jack_file))


    except OSError:
        print("Could not open some file.\n "
              "If file exists, check spelling of file path.")
        return

    except Exception as e:
        print("Some exception occurred while parsing.", e)
        traceback.print_exc()
        return


def filter_paths(path):
    """
    Filter vm file paths in case a directory path is supplied
    """
    return ["{}/{}".format(path, f) for f in os.listdir(path) if
            f.endswith(FILE_EXTENSION_JACK)]



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Wrong number of arguments.\n"
              "Usage: VMTranslator file_name.vm or /existing_dir_path/")
    else:
        main(sys.argv[FILE_PATH], no_compile=True, no_tokenize=False)

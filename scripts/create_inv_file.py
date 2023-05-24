import re
import sys
import zlib
import codecs
import PySide6
import requests
from sphinx.ext.intersphinx import inspect_main
from sphinx.util.inventory import InventoryFileReader

pyside_uri = "https://doc.qt.io/qtforpython/"
package_name = "PySide6"

alias_modules = PySide6._find_all_qt_modules()

# the filename to use to save the original objects.inv file
original_inv = "qt6-original.inv"
original_txt = "qt6-original.txt"

# the filename to use to save the Sphinx-compatible object.inv file
modified_inv = "qt6-with-aliases.inv"
modified_txt = "qt6-with-aliases.txt"


def create_modified_inv():
    def write(*args):
        fout.write(compressor.compress((" ".join(args) + "\n").encode("utf-8")))

    # download the original objects.inv file
    with open(original_inv, mode="wb") as f:
        f.write(requests.get(pyside_uri + "objects.inv").content)

    fin = open(original_inv, mode="rb")
    fout = open(modified_inv, mode="wb")

    # use the same compression for the output file as
    # sphinx.util.inventory.InventoryFile.dump
    compressor = zlib.compressobj(9)

    reader = InventoryFileReader(fin)

    # copy the header
    for i in range(4):
        fout.write((reader.readline() + "\n").encode("utf-8"))

    for line in reader.read_compressed_lines():
        # the re.match code is copied from
        # sphinx.util.inventory.InventoryFile.load_v2
        m = re.match(r"(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)", line.rstrip())
        if not m:
            continue

        name, typ, prio, location, dispname = m.groups()
        location = pyside_uri + location.rstrip("$") + name

        write(name, typ, prio, location, dispname)
        if name.endswith("QtCore.Signal"):
            # QtCore.SignalInstance maps to QtCore.Signal
            write(package_name + ".QtCore.SignalInstance", typ, prio, location, dispname)

        # apply the aliases
        for module in alias_modules:
            m = re.match(
                r"{0}\.{1}\.{0}\.{1}\.(\w+)(\.\w+)?".format(package_name, module), name
            )
            if m:
                classname, method = m.groups()
                if method is None:
                    method = ""

                aliases = [
                    "PyQt6" + "." + module + "." + classname + method,
                    "prettyqt.qt" + "." + module + "." + classname + method,
                    "qtpy" + "." + module + "." + classname + method,
                    "PySide6" + "." + module + "." + classname + method,
                    module + "." + classname + method,
                    classname + method,
                ]

                for alias in aliases:
                    write(alias, typ, prio, location, dispname)
                    # print(location)

    fout.write(compressor.flush())
    fin.close()
    fout.close()


def main():
    create_modified_inv()

    print("Created:")
    print("  " + original_inv)
    print("  " + original_txt)
    print("  " + modified_inv)
    print("  " + modified_txt)

    # redirect the print() statements in the inspect_main() function to a file
    sys.stdout = codecs.open(original_txt, "wb", encoding="utf-8")
    inspect_main([original_inv])
    sys.stdout.close()

    # if the following succeeds without raising an exception then Sphinx is
    # able to read the pyqt#-modified-objects.inv file that was just created
    sys.stdout = codecs.open(modified_txt, "wb", encoding="utf-8")
    inspect_main([modified_inv])
    sys.stdout.close()

    sys.exit(0)


if __name__ == "__main__":
    main()

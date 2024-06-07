import sys
import interpreter

if len(sys.argv) > 2:
    sys.exit("Insufficient arguments")

if len(sys.argv) == 2:
    filename = sys.argv[1]
    with open(filename, "r", encoding="UTF-8") as file:
        code = file.readlines()
    interpreter.compile(code)
else:
    interpreter.run()
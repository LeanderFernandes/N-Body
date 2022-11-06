import sys
from nbody_cython import main

if len(sys.argv) == 3:
    main(int(sys.argv[1]), int(sys.argv[2]))
else:
    print("Usage: Python {} <ITERATIONS> <DAYS PER ITERATION>".format(sys.argv[0]))

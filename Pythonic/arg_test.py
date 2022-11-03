import sys

def main(x):
    y = x*x
    print(y)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
    else:
        print("Usage: Python {} <X>".format(sys.argv[0]))


"""if int(len(sys.argv)) == 3:
    main(int(sys.argv[1]),int(sys.argv[2]))
else:
    print("Usage: python {} <ITERATIONS> <THREADS>".format(sys.argv[0]))"""
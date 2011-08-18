import getopt, sys

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:b:c:d:')
        print(opts)
        print(args)
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)
    

if __name__ == "__main__":
    main()
from yacc_parser import parser


def main():
    # Parse some text
    # main.py
    while True:
        try:
            s = input('Enter a statement or expression: ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)


if __name__ == '__main__':
    main()

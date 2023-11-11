from yacc_parser import parser


def main():
    # Parse some text
    while True:
        try:
            s = input('Enter an arithmetic expression: ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)


if __name__ == '__main__':
    main()

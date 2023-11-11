import unittest

from yacc_grammar import parser


class TestArithmeticParser(unittest.TestCase):

    def test_basic_arithmetic(self):
        self.assertEqual(parser.parse("2 + 3"), 5)
        self.assertEqual(parser.parse("4 - 2"), 2)
        self.assertEqual(parser.parse("6 * 3"), 18)
        self.assertEqual(parser.parse("8 / 2"), 4)
        self.assertEqual(parser.parse("5 / 2"), 2.5)

    def test_exponentiation(self):
        self.assertEqual(parser.parse("2 ^ 3"), 8)

    def test_variable_assignment_and_use(self):
        parser.parse("x = 5")
        self.assertEqual(parser.parse("x + 2"), 7)

    def test_complex_expression(self):
        parser.parse("y = 10")
        self.assertEqual(parser.parse("2 * y + 3"), 23)


if __name__ == '__main__':
    unittest.main()

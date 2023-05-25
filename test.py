import unittest
from unittest.mock import patch

def additionner(a, b):
    return a+b

def conversion_number():
    nb_str = input("Rentrer un nombre")
    return int(nb_str)

class TestsUnitaireDemo(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_additionner_nombres_positifs(self):
        print("Les nombres positifs")
        self.assertEqual(additionner(5, 10), 15)
        self.assertEqual(additionner(6, 10), 16)
        self.assertEqual(additionner(6000, 5), 6005)

    def test_additionner_nombres_negatifs(self):
        print("Les nombres négatifs")
        self.assertEqual(additionner(-6, -10), -16)

    def test_conversion_number_valide(self):
        print("Les conversions valides")
        with patch('builtins.input', return_value="10"):
            self.assertEqual(conversion_number(), 10)
        with patch('builtins.input', return_value="55"):
            self.assertEqual(conversion_number(), 55)

    def test_conversion_entrer_valide(self):
        print("Les conversions enter valides")
        with patch('builtins.input', return_value='vrs<ssff'):
            self.assertRaises(ValueError, conversion_number)    

unittest.main()
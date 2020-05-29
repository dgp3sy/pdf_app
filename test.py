import unittest
import process_pdf
import ido_reader

class Test_New_Annual_Report(unittest.TestCase):
    def test_name_generator_single(self):
        # SETUP
        names = process_pdf.file_name_generator_new("test_new_single.pdf")

        # Test
        self.assertEqual(type(names), type([]), msg="Annual Report (New) Error: Wrong Return Type on Name Generator")
        self.assertLess(len(names), 2, msg="Annual Report (New) Error: Name Generator List Too Long")
        self.assertGreater(len(names), 0, msg="Annual Report (New) Error: Name Generator List Too Short")
        self.assertEqual(len(names), 1, msg="Annual Report (New) Error: Name Generator List Not Correct Length")
        self.assertEqual(names[0], 'Davison, James 0720004830 June 2019 Annual Statement.pdf',
                         msg="Annual Report (New) Error: Incorrect File Name Generated")
    def test_prepare_name(self):
        self.assertEqual("Jones, Bob", process_pdf.prepare_name("Bob Jones"), msg="Name Preparation Error: First Name and Surname")
        self.assertEqual("Jones, Bob", process_pdf.prepare_name("Bob Robert Jones"), msg="Name Preparation Error: Middle Name")
        self.assertEqual("Jones, Bob", process_pdf.prepare_name("Bob R. Jones"), msg="Name Preparation Error: Middle Initial")
        self.assertEqual("Jones, Bob", process_pdf.prepare_name("Bob R Jones"), msg="Name Preparation Error: Middle Initial")
    def test_prepare_month(self):
        self.assertEqual("January", process_pdf.prepare_month(1), msg="Process PDF - Prepare Month Incorrect Return Value on Month 1")
        self.assertEqual("MONTH ", process_pdf.prepare_month(0), msg="Process PDF - Incorrect Error Handling when Input is 0")
        self.assertEqual("MONTH ", process_pdf.prepare_month(-1), msg="Process PDF - Incorrect Error Handling when Input is -1")
        self.assertEqual("MONTH ", process_pdf.prepare_month("test"), msg="Process PDF - Incorrect Error Handling when Input is string")
        self.assertEqual("MONTH ", process_pdf.prepare_month(13), msg="Process PDF - Incorrect Error Handling when Input is greater than 12")
        self.assertEqual("MONTH ", process_pdf.prepare_month([]), msg="Process PDF - Incorrect Error Handling when Input is unexpected type")

class Test_Old_Annual_Report(unittest.TestCase):
    def test_name_generator_single(self):
        # SETUP
        names = process_pdf.file_name_generator_old("test_old_single.pdf")

        # Test
        self.assertEqual(type(names), type([]), msg="Annual Report (Old) Error: Wrong Return Type on Name Generator")
        self.assertLess(len(names), 2, msg="Annual Report (Old) Error: Name Generator List Too Long")
        self.assertGreater(len(names), 0, msg="Annual Report (Old) Error: Name Generator List Too Short")
        self.assertEqual(len(names), 1, msg="Annual Report (Old) Error: Name Generator List Not Correct Length")
        self.assertEqual(names[0], 'RUHLAND, JAMES 1618657810 May 2019 Annual Statement.pdf',
                         msg="Annual Report (Old) Error: Incorrect File Name Generated")

class Test_IDO_Letter(unittest.TestCase):
    def test_name_generator(self):
        names = ido_reader.ido_name_generator("IDO Letter.pdf")

        self.assertEqual(type(names), type([]), msg="Annual Report (Old) Error: Wrong Return Type on Name Generator")
        self.assertLess(len(names), 2, msg="Annual Report (Old) Error: Name Generator List Too Long")
        self.assertGreater(len(names), 0, msg="Annual Report (Old) Error: Name Generator List Too Short")
        self.assertEqual(len(names), 1, msg="Annual Report (Old) Error: Name Generator List Not Correct Length")
        self.assertEqual(names[0], 'STEELE, BRENT 0720726910 June 2020 IDO Letter.pdf',
                         msg="Annual Report (Old) Error: Incorrect File Name Generated")


if __name__ == '__main__':
    unittest.main()
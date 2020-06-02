import shutil
import unittest
import process_pdf
import ido_reader
import os

class Test_New_Annual_Report(unittest.TestCase):
    def setUp(self):
        self.names = process_pdf.file_name_generator_new("test_new_single.pdf")

    def test_name_generator_single(self):
        # Test
        self.assertEqual(type(self.names), type([]), msg="Annual Report (New) Error: Wrong Return Type on Name Generator")
        self.assertLess(len(self.names), 2, msg="Annual Report (New) Error: Name Generator List Too Long")
        self.assertGreater(len(self.names), 0, msg="Annual Report (New) Error: Name Generator List Too Short")
        self.assertEqual(len(self.names), 1, msg="Annual Report (New) Error: Name Generator List Not Correct Length")
        self.assertEqual(self.names[0], 'Davison, James 0720004830 June 2019 Annual Statement.pdf',
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
        self.assertEqual("MONTH ", process_pdf.prepare_month(None), msg="Process PDF - Incorrect Error Handling of Null Type")


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
    def test_writing_to_folder(self):
        # SETUP - Clear Extracted Pages Folder
        folder_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\\Extracted Pages Testing Environment\\"



        process_pdf.init_old("Annual161.pdf", is_test=True)# Call Subroutine

        # TEST
        self.assertTrue(os.path.exists(folder_path), msg="OLD Annual - Path of Save Location Never Created by generate_save_location() Subroutine")
        self.assertEqual(4, len(next(os.walk(folder_path))[2]), msg="OLD Annual - Incorrect Number of Files Generated")
        self.assertEqual("DABERKOW, JEREMY 1618870350 May 2019 Annual Statement.pdf", next(os.walk(folder_path))[2][0], msg="OLD Annual - Incorrect File Name Generated")
        self.assertEqual("KARDOES, NICOLE 1617116460 May 2019 Annual Statement.pdf", next(os.walk(folder_path))[2][1], msg="OLD Annual - Incorrect File Name Generated")

class Test_IDO_Letter(unittest.TestCase):
    def setUp(self):
        self.names = ido_reader.ido_name_generator("IDO Letter.pdf")
        self.folder_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\\Extracted Pages Testing Environment\\"
        ido_reader.generate_save_location(is_test=True)

        # Clear Testing Folder
        shutil.rmtree(self.folder_path)
        ido_reader.init_ido_reader("IDO Letter.pdf", is_test=True)# Call Subroutine
    def tearDown(self):
        # Clear Testing Folder
        shutil.rmtree(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\\Extracted Pages Testing Environment\\")


    def test_name_generator_type(self):
        self.assertEqual(type(self.names), type([]), msg="Annual Report (Old) Error: Wrong Return Type on Name Generator")
    def test_name_generator_lower(self):
        self.assertLess(len(self.names), 2, msg="Annual Report (Old) Error: Name Generator List Too Long")
    def test_name_generator_upper(self):
        self.assertGreater(len(self.names), 0, msg="Annual Report (Old) Error: Name Generator List Too Short")
    def test_name_generator_amt(self):
        self.assertEqual(len(self.names), 1, msg="Annual Report (Old) Error: Name Generator List Not Correct Length")
    def test_name_generator_value(self):
        self.assertEqual(self.names[0], 'STEELE, BRENT 0720726910 June 2020 IDO Letter.pdf',
                         msg="Annual Report (Old) Error: Incorrect File Name Generated")
    def test_prepare_month(self):
        self.assertEqual("January", ido_reader.prepare_month(1), msg="Process PDF - Prepare Month Incorrect Return Value on Month 1")
    def test_prepare_month_0(self):
        self.assertEqual("MONTH ", ido_reader.prepare_month(0), msg="Process PDF - Incorrect Error Handling when Input is 0")
    def test_prepare_month_negative(self):
        self.assertEqual("MONTH ", ido_reader.prepare_month(-1), msg="Process PDF - Incorrect Error Handling when Input is -1")
        self.assertEqual("MONTH ", ido_reader.prepare_month(-1000), msg="Process PDF - Incorrect Error Handling when Input is -1")

    def test_prepare_month_str(self):
        self.assertEqual("MONTH ", ido_reader.prepare_month("test"), msg="Process PDF - Incorrect Error Handling when Input is string")
    def test_prepare_month_large(self):
        self.assertEqual("MONTH ", ido_reader.prepare_month(13), msg="Process PDF - Incorrect Error Handling when Input is greater than 12")
        self.assertEqual("MONTH ", ido_reader.prepare_month(1000), msg="Process PDF - Incorrect Error Handling when Input is greater than 12")
    def test_prepare_month_list(self):
        self.assertEqual("MONTH ", ido_reader.prepare_month([]), msg="Process PDF - Incorrect Error Handling when Input is unexpected type")
    def test_prepare_month_null(self):
        self.assertEqual("MONTH ", ido_reader.prepare_month(None), msg="Process PDF - Incorrect Error Handling of Null Type")
    def test_file_path_generated(self):
        self.assertTrue(os.path.exists(self.folder_path), msg="IDO Letter - Path of Save Location Never Created by generate_save_location() Subroutine")
    def test_num_files_generated(self):
        self.assertEqual(1, len(next(os.walk(self.folder_path))[2]), msg="IDO Letter - Incorrect Number of Files Generated")
    def test_file_name_valid(self):
        self.assertEqual("STEELE, BRENT 0720726910 June 2020 IDO Letter.pdf", next(os.walk(self.folder_path))[2][0], msg="IDO Letter - Incorrect File Name Generated")



if __name__ == '__main__':
    unittest.main()
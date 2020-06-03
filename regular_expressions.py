import re
class Report():
    def __init__(self, report_type):
        self.type = report_type
        self.__month_dict = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
    def prepare_name(self, name):
        '''
        Helper function for the process_pdf function that takes in a name with possible middle initial or middle name
        and returns the name in the format: last name, first name. This will be later used to create the file path for the
        new pdf document
        :param name: string, name in the format: first name (possible middle name) last name
        :return: name: string, in the format: last name, first name
        '''
        middle_name = False
        if name.count(' ') == 2:
            middle_name = True
        if middle_name:
            l = name.rfind(' ')
            f = name.find(' ')
            first_name = name[:f]
            last_name = name[l + 1:]
        else:
            n = name.find(' ')
            first_name = name[:n]
            last_name = name[n + 1:]
        return last_name + ", " + first_name

    def prepare_month(self, num):
        '''
        Converts integers to string value of month using dictionary
        :param num: (int) Integer value of month, expected values: 1-12
        :return: (str) String value that corresponds to that integer's month
        '''

        # Pragmatic Programmer recommends exceptions being reserved for unexpected events
        # This would not be a good place to include exception handling because the subroutines that are
        # calling this function are all being controlled internally, therefore, the inputs should be under the
        # contract of integer values between 1 and 12. However, I included conditions in the unlikely event that
        # another type is passed through by using a default value, and accounting for invalid keys
        if num == None or type(num) != int:
            return "MONTH"
        else:
            return self.__month_dict.get(num, "MONTH")
class new_annual_regex(Report):

    def __init__(self):
        Report.__init__(self, "New Annual Report")
        self.__date_findr_new = re.compile(r"through ([0-9]{2})/([0-9]{2})/([0-9]{4})")
        self.__insured_findr_new = re.compile(r"Dean E Harder ([A-Za-z ]*)")
        self.__insured_findr2_new = re.compile(r"Dear ([A-Za-z ]*),")
        self.__policyNo_findr_new = re.compile(r"(07[1|2][0-9]{7})")

    def get_date_findr(self):
        return self.__date_findr_new
    def get_insured_findr(self):
        return self.__insured_findr_new
    def get_insured_findr2(self):
        return self.__insured_findr2_new
    def get_policyNo_findr(self):
        return self.__policyNo_findr_new
    def find_month(self, text):
        for match in self.__date_findr_new.finditer(text):
            return self.prepare_month(int(match.group(1)))
        return "MONTH"
    def find_year(self, text):
        for match in self.__date_findr_new.finditer(text):
            return match.group(3)
        return "YEAR"
    def find_policyNo(self, text):
        for match in self.__policyNo_findr_new.finditer(text):
            return match.group(1)
        return "POLICY_NO"
    def find_name(self, text):
        for match in self.__insured_findr_new.finditer(text):
            return self.prepare_name(match.group(1))
        for match in self.__insured_findr2_new.finditer(text):
            return self.prepare_name(match.group(1))
        return "NAME"





class old_annual_regex(Report):
    def __init__(self):
        Report.__init__(self, "Old Annual Report")
        self.__month_findr = re.compile(r"(January|February|March|April|May|June|July|August|September|October|November|December)")
        self.__year_findr = re.compile(r"through [A-Za-z ]*[0-9]*, ([0-9]{4})")
        self.__policyNo_findr_old = re.compile(r"Policy No\. ([0-9/-]*)")
        self.__insured_findr = re.compile(r"which insures ([A-Za-z ]*)")
    def get_month_findr(self):
        return self.__month_findr
    def get_year_findr(self):
        return self.__year_findr
    def get_policy_findr(self):
        return self.__policyNo_findr_old
    def get_name_findr(self):
        return self.__insured_findr

    def find_month(self, text):
        for match in self.__month_findr.finditer(text):
            return match.group(1)
        return "MONTH "
    def find_year(self, text):

        for match in self.__year_findr.finditer(text):
            return match.group(1)
        return "YEAR"
    def find_policyNo(self, text):
        for match in self.__policyNo_findr_old.finditer(text):
            policy_no = match.group(1)
            policy_no = policy_no.replace("-","") + "0"
            return policy_no
        return "POLICY_NO"
    def find_name(self, text):
        for match in self.__insured_findr.finditer(text):
            return self.prepare_name(match.group(1))
        return "NAME "


class ido_regex(Report):
    def __init__(self):
        Report.__init__(self, "IDO Letter")
        self.__date_findr = re.compile(r"Anniversary Date: ([0-9]{2})/([0-9]{2})/([0-9]{4})")
        self.__policy_no_findr = re.compile(r"Policy Number: ([0-9]*)")
        self.__name_findr = re.compile(r"Dear ([A-Za-z ]*),")
    def get_date_findr(self):
        return self.__date_findr
    def get_policy_findr(self):
        return self.__policy_no_findr
    def get_name_findr(self):
        return self.__name_findr

    def find_month(self, text):
        for match in self.__date_findr.finditer(text):
            return self.prepare_month(int(match.group(1)))
    def find_year(self, text):
        for match in self.__date_findr.finditer(text):
            return match.group(3)
    def find_policyNo(self, text):
        for match in self.__policy_no_findr.finditer(text):
            return match.group(1).replace("-", "")
    def find_name(self, text):
        for match in self.__name_findr.finditer(text):
            return self.prepare_name(match.group(1).strip())


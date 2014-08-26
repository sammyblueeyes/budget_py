import unittest 


class Cashflow:

    def __init__(self, start_position=0.0, number_of_days=0):
        pass

    def calculate(self, start_position, number_of_days):
        return [start_position]


    def load_csv(self, filename):
        """Load data csv file from filename. Return pointer to data object."""
        infile = open(filename, "r")
        data = []
        for line in infile:
            data.append(line.rstrip().split(","))
        infile.close()
        return data

    def load_expenses(self, filename):
        return self.load_csv(filename)
       
    def load_income(self, filename):
        return self.load_csv(filename)



class BudgetTest(unittest.TestCase):

    def setUp(self):
        """Setup unit tests by creating CSV files for income and expenses"""
        ofile = open("expenses.csv", "w")
        ofile.write('''"Mortgage",WEEKLY,500.00,30/12/2009
"Rates",QUARTERLY,301.10,04/02/2010
"Water",QUARTERLY,194.67,11/02/2010
"Car club membership",YEARLY,165.00,09/08/2010
"Food",WEEKLY,130.00,02/01/2010
"Car petrol",WEEKLY,60.00,07/12/2009
"Electricity",MONTHLY,300.00,10/12/2009
"Health Insurance",MONTLY,205.00,16/11/2009
"Phone bill",MONTLY,40.00,27/11/2009
"Entertainment",WEEKLY,300.00,04/12/2009
''')
        ofile.close()

        ofile = open("income.csv", "w")
        ofile.write('"Rosie\'s salary",MONTHLY,3944.20,02/05/2013\n')
        ofile.write('"Jeanette\' salary",FORTNIGHTLY,2899.20,23/08/2013\n')
        ofile.close()


    def test_load_expenses_csv_file(self):
        expenses = Cashflow().load_expenses("expenses.csv")
        self.assertIsNotNone(expenses)
        self.assertEqual(10, len(expenses))

    def test_load_income_csv_file(self):
        income = Cashflow().load_income("income.csv")
        self.assertIsNotNone(income)
        self.assertEqual(2, len(income))

    def test_range_contains_no_income_or_expenses(self):
        start_position = 1000.0
        num_days = 1
        cashflow = Cashflow().calculate(start_position, num_days)
        self.assertEqual(len(cashflow), num_days)
        for day in cashflow:
            self.assertEqual(day, start_position)



if __name__ == '__main__':
    unittest.main()

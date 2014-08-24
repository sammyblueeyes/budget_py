import unittest 


#TODO read each line of file, validate and add to a structure
def load_expenses(filename):
    """Load expenses csv file from filename. Return pointer to expenses object."""
    infile = open(filename, "r")
    infile.close()
    return []





class BudgetTest(unittest.TestCase):

    #TODO write out some sample date for income and expenses
    def setUp(self):
        """Setup unit tests by creating CSV files for income and expenses"""
        ofile = open("expenses.csv", "w")
        ofile.close()
        ofile = open("income.csv", "w")
        ofile.close()

    def test_load_expenses(self):
        """docstring for test_load_expenses"""
        expenses = load_expenses("expenses.csv")
        self.assertIsNotNone(expenses)




if __name__ == '__main__':
    unittest.main()

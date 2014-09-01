import unittest 

from datetime import datetime, date, timedelta
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY


(FORTNIGHTLY,
 QUARTERLY,
 HALFYEARLY) = range(10,13)


# TODO Add a method to tally up income and expenses for each day of the specified period
# TODO Add an input for user arguments (income file, expenses file, number of days to graph)

class Cashflow:

    def __init__(self, start_position=0.0, number_of_days=1, start_date=None):
        # TODO: number_of_days must be > 0
        # TODO: Ensure start_date is at the beginning of the day
        self.start_position = start_position
        self.number_of_days = number_of_days
        d = date.today()
        if start_date is None:
            self.start_date = datetime(d.year, d.month, d.day)
        else:
            self.start_date = start_date
        self.end_date = self.start_date + timedelta(number_of_days-1)

    def calculate(self, start_position, number_of_days, start_date=None, income=None, expenses=None):
        return [start_position for x in range(number_of_days)]
    
    def get_due_dates(self, due_date, period):
        if period == YEARLY:
            r = rrule(period, dtstart=due_date, bymonth=due_date.month, bymonthday=(due_date.day, -1), bysetpos=1)
        elif period == HALFYEARLY:
            r = rrule(MONTHLY, dtstart=due_date, bymonthday=(due_date.day, -1), bysetpos=1, interval=6)
        elif period == QUARTERLY:
            r = rrule(MONTHLY, dtstart=due_date, bymonthday=(due_date.day, -1), bysetpos=1, interval=3)
        elif period == MONTHLY:
            r = rrule(period, dtstart=due_date, bymonthday=(due_date.day, -1), bysetpos=1)
        elif period == FORTNIGHTLY:
            r = rrule(WEEKLY, dtstart=due_date, interval=2)
        else:
            r = rrule(period, dtstart=due_date)
        return r.between(self.start_date, self.end_date, inc=True)

    def load_csv(self, filename):
        """Load data csv file from filename. Return pointer to data object."""
        infile = open(filename, "r")
        data = []
        line_number = 1;
        for line in infile:
            fields = line.rstrip().split(",")
            # Name:string,type:int,amount:double,first_date:date
            if len(fields) != 4:
                raise ValueError("Invalid input from file %s @ "
                        "line %d" % (filename, line_number))
            # TODO: Validate field types
            line_number = line_number+1
            data.append(fields)
        
        infile.close()
        return data

    def load_expenses(self, filename):
        return self.load_csv(filename)
       
    def load_income(self, filename):
        return self.load_csv(filename)



class BudgetTest(unittest.TestCase):

    def setUp(self):
        self.last_days = (31,28,31,30,31,30,31,31,30,31,30,31)

    def write_test_expenses_file(self):
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

    def write_test_income_file(self):
        ofile = open("income.csv", "w")
        ofile.write('"Rosie\'s salary",MONTHLY,3944.20,02/05/2013\n')
        ofile.write('"Jeanette\' salary",FORTNIGHTLY,2899.20,23/08/2013\n')
        ofile.close()


    def test_load_expenses_csv_file(self):
        self.write_test_expenses_file()
        expenses = Cashflow().load_expenses("expenses.csv")
        self.assertIsNotNone(expenses)
        self.assertEqual(10, len(expenses))

    def test_load_income_csv_file(self):
        self.write_test_income_file()
        income = Cashflow().load_income("income.csv")
        self.assertIsNotNone(income)
        self.assertEqual(2, len(income))

    def test_load_csv_file_with_incorrect_number_of_items_per_line(self):
        ofile = open("broken.csv", "w")
        ofile.write('abc,1\n')
        ofile.close()
        self.assertRaises(ValueError, Cashflow().load_csv, 
                "broken.csv")

    # TODO: Test checking of types of CSV fields
    # TODO: Parse CSV with commma in the description

    def test_range_with_no_income_or_expenses(self):
        start_position = 1000.0
        for num_days in range(0, 21):
            cashflow = Cashflow().calculate(start_position, num_days)
            self.assertEqual(len(cashflow), num_days)
            for day in cashflow:
                self.assertEqual(day, start_position)


    def assert_single_due_date(self, due_dates, start_date):
        self.assertEqual(len(due_dates), 1)
        self.assertEqual(due_dates[0], start_date)

    def test_gen_weekly_due_date_with_1_day_range(self):
        for i in range(-500, 20):
            c = Cashflow()
            due_date = c.start_date + timedelta(i)
            due_dates = c.get_due_dates(due_date, WEEKLY)
            # If the due date is in the future, It can't be in the
            # generated range.
            if i > 0:
                self.assertEqual(len(due_dates), 0)
            elif (i % 7) == 0:
                self.assert_single_due_date(due_dates, c.start_date)
            else:
                self.assertEqual(len(due_dates), 0)
            #print "     %d) " % i + str(due_dates)

    def test_gen_fortnightly_due_date_with_1_day_range(self):
        for i in range(-500, 20):
            c = Cashflow()
            due_date = c.start_date + timedelta(i)
            due_dates = c.get_due_dates(due_date, FORTNIGHTLY)
            # If the due date is in the future, It can't be in the
            # generated range.
            if i > 0:
                self.assertEqual(len(due_dates), 0)
            elif (i % 14) == 0:
                self.assert_single_due_date(due_dates, c.start_date)
            else:
                self.assertEqual(len(due_dates), 0)

    def test_gen_monthly_due_date_with_1_day_range_at_end_of_feb(self):
        def check_date(due_date):
            due_dates = c.get_due_dates(due_date, MONTHLY)
            self.assert_single_due_date(due_dates, c.start_date)

        # Due date on last day of February
        end_of_feb = datetime(2014, 2, 28)
        start_date = datetime(2014, 3, 28)
        c = Cashflow(start_date=start_date)

        check_date(end_of_feb)

        # Cashflow date on last day of February (non-leap year)
        start_date = end_of_feb
        c = Cashflow(start_date=start_date)

        check_date(datetime(2014, 1, 28))
        check_date(datetime(2014, 1, 29))
        check_date(datetime(2014, 1, 30))
        check_date(datetime(2014, 1, 31))

        # Cashflow date on last day of February (leap year)
        end_of_feb = datetime(2012, 2, 29)
        start_date = end_of_feb
        c = Cashflow(start_date=start_date)

        check_date(datetime(2012, 1, 29))
        check_date(datetime(2012, 1, 30))
        check_date(datetime(2012, 1, 31))

    def test_gen_monthly_due_date_with_1_day_range_at_end_of_month(self):
        # Check behaviour when due date is 30/31 of the month
        for i in range(len(self.last_days)):
            c = Cashflow(start_date=datetime(2014, i+1, self.last_days[i]))
            due_dates = c.get_due_dates(datetime(2012,12,30), MONTHLY)
            if self.last_days[i] <= 30:
                self.assert_single_due_date(due_dates, c.start_date)
            else:
                self.assertEqual(len(due_dates), 0)
            due_dates = c.get_due_dates(datetime(2012,12,31), MONTHLY)
            self.assert_single_due_date(due_dates, c.start_date)

    def test_gen_monthly_due_date_with_1_day_range_at_start_of_month(self):
        # check first of month 
        c = Cashflow(start_date=datetime(2014, 1, 1))
        due_dates = c.get_due_dates(datetime(2012,12,1), MONTHLY)
        self.assert_single_due_date(due_dates, c.start_date)


    def test_gen_monthly_due_date_with_1_day_range_within_the_month(self):
        # Check other day within the month 
        c = Cashflow(start_date=datetime(2014, 1, 17))
        due_dates = c.get_due_dates(datetime(2012,06,17), MONTHLY)
        self.assert_single_due_date(due_dates, c.start_date)

    def test_gen_yearly_due_date_with_1_day_range_for_leap_year(self):
        # Test YEARLY with 29 Feb in leap year as the due date
        c = Cashflow(start_date=datetime(2014, 2, 28))
        due_dates = c.get_due_dates(datetime(2012,02,29), YEARLY)
        self.assert_single_due_date(due_dates, c.start_date)

        c = Cashflow(start_date=datetime(2016, 2, 28))
        due_dates = c.get_due_dates(datetime(2012,02,29), YEARLY)
        self.assertEqual(len(due_dates), 0)

        c = Cashflow(start_date=datetime(2016, 2, 29))
        due_dates = c.get_due_dates(datetime(2012,02,29), YEARLY)
        self.assert_single_due_date(due_dates, c.start_date)

    def test_gen_yearly_due_date_with_1_day_range_for_non_leap_years(self):
        for i in range(365):
            c = Cashflow(start_date=datetime(2014, 1, 1)+timedelta(i))
            due_dates = c.get_due_dates(datetime(2013,c.start_date.month,c.start_date.day), YEARLY)
            self.assert_single_due_date(due_dates, c.start_date)

    def test_gen_quarterly_due_date_with_1_day_range(self):
        for i in range(12):
            c = Cashflow(start_date=datetime(2014, ((i+3) % 12)+1, 15))
            due_dates = c.get_due_dates(datetime(2013,i+1,15), QUARTERLY)
            self.assert_single_due_date(due_dates, c.start_date)
    
    def test_gen_quarterly_due_date_with_1_day_range_for_feb(self):
        c = Cashflow(start_date=datetime(2014, 2, 28))
        due_dates = c.get_due_dates(datetime(2012, 2, 29), QUARTERLY)
        self.assert_single_due_date(due_dates, c.start_date)

        c = Cashflow(start_date=datetime(2014, 2, 28))
        due_dates = c.get_due_dates(datetime(2013, 11, 30), QUARTERLY)
        self.assert_single_due_date(due_dates, c.start_date)

    def test_gen_halfyearly_due_date_with_1_day_range(self):
        def test(start_date, due_date):
            c = Cashflow(start_date=start_date)
            due_dates = c.get_due_dates(due_date, HALFYEARLY)
            self.assert_single_due_date(due_dates, c.start_date)
        test(datetime(2014,1,1), datetime(2013,7,1))
        test(datetime(2014,5,20), datetime(2013,11,20))
        test(datetime(2014,4,30), datetime(2013,10,31))
        test(datetime(2014,4,30), datetime(2013,10,31))
        test(datetime(2014,2,28), datetime(2013,8,31))
        test(datetime(2012,2,29), datetime(2011,8,31))


if __name__ == '__main__':
    unittest.main()


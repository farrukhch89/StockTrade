import sys
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox
from PyQt5 import QtCore
from decimal import Decimal

class StockTradeProfitCalculator(QDialog):
    '''
    Provides the following functionality:

    - Allows the selection of the stock to be purchased
    - Allows the selection of the quantity to be purchased
    - Allows the selection of the purchase date
    - Displays the purchase total
    - Allows the selection of the sell date
    - Displays the sell total
    - Displays the profit total
    - Additional functionality

    '''

    def __init__(self):
        '''
        This method requires substantial updates
        Each of the widgets should be suitably initalized and laid out
        '''
        super().__init__()

        # setting up dictionary of stocks
        self.data = self.make_data()
        # sorting the dictionary of stocks by the keys. The keys at the high level are dates, so we are sorting by date
        self.stocks = sorted(self.data.keys())

        # the following 2 lines of code are for debugging purposee and show you how to access the self.data to get dates and prices
        # print all the dates and close prices for AAL
        print("all the dates and close prices for AAL", self.data['AAL'])
        # print the close price for AAL on 12/2/2013
        print("the close price for AAL on 12/2/2013",self.data['AAL'][QDate(2013,2,12)])

        # The data in the file is in the following range
        #  first date in dataset - 7th Feb 2013
        #  last date in dataset - 8th Feb 2018
        # When the calendars load we want to ensure that the default dates selected are within the date range above
        #  we can do this by setting variables to store suitable default values for sellCalendar and buyCalendar.
        self.sellCalendarDefaultDate = sorted(self.data['AAL'].keys())[-1] # Accessing the last element of a python list is explained with method 2 on https://www.geeksforgeeks.org/python-how-to-get-the-last-element-of-list/
        print("self.sellCalendarStartDate", self.sellCalendarDefaultDate)
        # self.buyCalendarDefaultDate
        # print("self.buyCalendarStartDate", self.buyCalendarDefaultDate)


        # create QLabel for stock purchased
        stockLabel = QLabel('Stock Purchased: ')

        # create QComboBox and populate it with a list of stocks
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(self.stocks)

        # create CalendarWidgets for selection of purchase and sell dates
        # purchase calender
        purchaseDate = QLabel('Purchased Date: ')
        self.calender = QCalendarWidget(self)
        self.calender.move(15, 15)
        self.calender.setGridVisible(True)

        # get the first start date of purchase
        self.purchaseCalendarDefaultDate = sorted(self.data['AAL'].keys())[0]
        # start date of purchase
        self.calender.setMinimumDate(self.purchaseCalendarDefaultDate)
        self.calender.setMaximumDate(QDate(self.sellCalendarDefaultDate))

        # sell calender
        sellDate = QLabel('Sell Date: ')
        self.calenderSell = QCalendarWidget(self)
        self.calenderSell.move(15, 15)
        self.calenderSell.setGridVisible(True)

        # start and end date of sell
        self.calenderSell.setMinimumDate(QDate(self.purchaseCalendarDefaultDate))
        self.calenderSell.setMaximumDate(QDate(self.sellCalendarDefaultDate))

        # create QSpinBox to select stock quantity purchased
        quantity = QLabel('Quantity: ')
        self.fromSpinBox = QSpinBox()

        # create QLabels to show the stock purchase total
        stockPurchaseTotal = QLabel('Purchase Total: ')
        self.purchasingTotal = QLabel("0.00")

        # create QLabels to show the stock sell total
        stockSellTotal = QLabel('Sell Total: ')
        self.sellingTotal = QLabel("0.00")

        # create QLabels to show the stock profit total
        profitTotal = QLabel('Profit Total: ')
        self.profitMade = QLabel("0.00")

        # initialize the layout - 6 rows to start
        grid = QGridLayout()

        # row 0 - stock selection
        grid.addWidget(stockLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 0, 1)

        # row 1 - quantity selection
        grid.addWidget(quantity, 1, 0)
        self.fromSpinBox.setValue(1)
        grid.addWidget(self.fromSpinBox, 1, 1)


        # row 2 - purchase date selection
        grid.addWidget(purchaseDate, 2, 0)
        grid.addWidget(self.calender, 2, 1)
        # self.calender.setStyleSheet("border: 2px Solid black")

        # row 3 - display purchase total
        grid.addWidget(stockPurchaseTotal, 3, 0)
        grid.addWidget(self.purchasingTotal, 3, 1)

        # row 4 - sell date selection
        grid.addWidget(sellDate, 4, 0)
        grid.addWidget(self.calenderSell, 4, 1)

        # row 5 - display sell total
        grid.addWidget(stockSellTotal, 5, 0)
        grid.addWidget(self.sellingTotal, 5, 1)

        # row 6 - display profit total
        grid.addWidget(profitTotal, 6, 0)
        grid.addWidget(self.profitMade, 6, 1)

        self.setLayout(grid)

        # set the calendar values
        # purchase: two weeks before most recent
        self.calender.setSelectedDate(QDate(2018, 1, 24))
        # self.calender.setSelectedDate.setStyleSheet()
        # sell: most recent
        self.calenderSell.setSelectedDate(QDate(2018, 2, 7))

        # connecting signals to slots to that a change in one control updates the UI
        self.fromComboBox.currentIndexChanged.connect(self.updateUi)
        self.fromSpinBox.valueChanged.connect(self.updateUi)
        self.calender.clicked.connect(self.updateUi)
        self.calenderSell.clicked.connect(self.updateUi)

        # set the window title
        self.setWindowTitle('Ass1-StockTradeProfit-Farrukh-Jahangeer-2960928')

        # update the UI
    def updateUi(self):
        '''
        This requires substantial development
        Updates the Ui when control values are changed, should also be called when the app initializes
        :return:
        '''
        try:
            print("")
            # name of stock selected
            name = self.fromComboBox.currentText()
            # quantity changed
            quantity = self.fromSpinBox.value()

            # get selected dates from calendars
            dateOfPurchase = self.calender.selectedDate()
            dateOfSelling = self.calenderSell.selectedDate()

            # price of purchase and selling
            price = self.data[name][QDate(dateOfPurchase)]
            priceSell = self.data[name][QDate(dateOfSelling)]

            # perform necessary calculations to calculate totals
            # purchase total = price multiply by the quantity
            purchase_total = price * quantity
            # sell total = price multiply by the quantity
            sell_total = priceSell * quantity
            # profit = sell total - purchase total
            profit = sell_total - purchase_total

            #print("Stock name " + name)
            #print(quantity)
            #print(dateOfPurchase)
            #print(dateOfSelling)
            #print(price)
            #print(purchase_total)
            #print(sell_total)
            #print(profit)

            # update the label displaying totals
            # set the total purchase price back to its location with label purchase total
            self.purchasingTotal.setNum(purchase_total)
            # set the sell total back to its location with label sell total
            self.sellingTotal.setNum(sell_total)
            # set the profit back to its location with label profit
            self.profitMade.setNum(profit)

        except Exception as e:
            print(e)


################ YOU DO NOT HAVE TO EDIT CODE BELOW THIS POINT  ########################################################

    def make_data(self):
        '''
        This code is complete
        Data source is derived from https://www.kaggle.com/camnugent/sandp500/download but use the provided file to avoid confusion

        Converts a CSV file to a dictonary fo dictionaries like

            Stock   -> Date      -> Close
            AAL     -> 08/02/2013 -> 14.75
                    -> 11/02/2013 -> 14.46
                    ...
            AAPL    -> 08/02/2013 -> 67.85
                    -> 11/02/2013 -> 65.56

        Helpful tutorials to understand this
        - https://stackoverflow.com/questions/482410/how-do-i-convert-a-string-to-a-double-in-python
        - nested dictionaries https://stackoverflow.com/questions/16333296/how-do-you-create-nested-dict-in-python
        - https://www.tutorialspoint.com/python3/python_strings.htm
        :return: a dictionary of dictionaries
        '''
        file = open("./all_stocks_5yr.csv","r")  # open a CSV file for reading https://docs.python.org/3/library/functions.html#open
        data = {}         # empty data dictionary
        file_rows = []    # empty list of file rows
        # add rows to the file_rows list
        for row in file:
            file_rows.append(row.strip()) # https://www.geeksforgeeks.org/python-string-strip-2/
        print("len(file_rows):" + str(len(file_rows)))

        # get the column headings of the CSV file
        row0 = file_rows[0]
        line = row0.split(",")
        column_headings = line
        print(column_headings)

        # get the unique list of stocks from the CSV file
        non_unique_stocks = []
        file_rows_from_row1_to_end = file_rows[1:len(file_rows) - 1]
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            non_unique_stocks.append(line[6])
        stocks = self.unique(non_unique_stocks)
        print("len(stocks):" + str(len(stocks)))
        print("stocks:" + str(stocks))

        # build the base dictionary of stocks
        for stock in stocks:
            data[stock] = {}

        # build the dictionary of dictionaries
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            date = self.string_date_into_QDate(line[0])
            stock = line[6]
            close_price = line[4]
            #include error handeling code if close price is incorrect
            data[stock][date]= float(close_price)
        print("len(data):", len(data))
        return data


    def string_date_into_QDate(self, date_String):
        '''
        This method is complete
        Converts a data in a string format like that in a CSV file to QDate Objects for use with QCalendarWidget
        :param date_String: data in a string format
        :return:
        '''
        date_list = date_String.split("-")
        date_QDate = QDate(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        return date_QDate


    def unique(self, non_unique_list):
        '''
        This method is complete
        Converts a list of non-unique values into a list of unique values
        Developed from https://www.geeksforgeeks.org/python-get-unique-values-list/
        :param non_unique_list: a list of non-unique values
        :return: a list of unique values
        '''
        # intilize a null list
        unique_list = []

        # traverse for all elements
        for x in non_unique_list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
                # print list
        return unique_list

# This is complete
if __name__ == '__main__':

    app = QApplication(sys.argv)
    stockTradeProfitCalculator = StockTradeProfitCalculator()
    stockTradeProfitCalculator.show()
    sys.exit(app.exec_())
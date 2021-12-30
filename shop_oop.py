# Python Shop Program - OOP
# MULTI-PARADIGM PROGRAMMING 2021

import csv

class Product:
    """
    Product Class to store product info
    """

    def __init__(self, name, price=0):
        """
        Parameters:
            -name : string
            -price : floating point number
        """
        self.name = name
        self.price = price
    
    def __repr__(self):
        """
        Returns a string as a representation of the Product Class
        """
        return f'{self.name} {self.price}'


class ProductStock:
    """
    ProductStock Class to store the product stock info
    """
    
    def __init__(self, product, quantity):
        """
        Parameters:
            -product : instance of the Product Class
            -quantity : interger
        """
        self.product = product
        self.quantity = quantity
    
    def name(self):
        """
        Method to return product name`
        """
        return self.product.name;
    
    def unit_price(self):
        """
        Method to return product price
        """
        return self.product.price;
        
    def cost(self):
        """
        Method to return total price per product
        """
        return self.unit_price() * self.quantity;
        
    def __repr__(self):
        """
        Returns a string as a representation of the ProductStock Class
        """
        return f"{self.product} {self.quantity}";


class Customer:
    """
    Customer Class to store customer's details, budget & shopping list info
    """

    def __init__(self, path):
        """
        Method to initialize the object with info imported from a csv file
        Parameters:
            -path : file path to customer csv file
        """
        self.shopping_list = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])
            for row in csv_reader:
                name = row[0]
                quantity = int(row[1])
                p = Product(name)
                ps = ProductStock(p, quantity)
                self.shopping_list.append(ps) 
                
    def calculate_costs(self, price_list):
        """
        Method to return the product price for the
        items within the customer's shopping list
        """
        for shop_item in price_list:
            for list_item in self.shopping_list:
                if (list_item.name() == shop_item.name()):
                    list_item.product.price = shop_item.unit_price()
    
    def order_cost(self):
        """
        Method to calculate the total bill
        for the items in the shopping list
        """
        cost = 0
        for list_item in self.shopping_list:
            cost += list_item.cost()
        return cost
    
    def __repr__(self):
        """
        Returns a easy to read tabulated string as a representation of the Customer Class
        """
        str = f"\n"
        str += f"CUSTOMER NAME: {self.name}\n"
        str += f"BUDGET {self.budget}\n"
        str += f"SHOPPING LIST:\n"
        str += ("{:<15} {:<15} {:<15}".format('Product Name', 'Quantity', 'Price(€)'))

        for item in self.shopping_list:
            str += f"\n{item.product.name:<17}"
            str += f"{item.quantity:<15}"
            str += f"{item.cost()}"
        return str


class newCustomer(Customer):
    """
    New Customer Subclass of Customer Class to store 
    manually inputted customer details, budget & shopping list
    """

    def __init__(self):
        """
        Method to initialize the object with info manually inputted from 
        the command line
        """
        self.shopping_list=[]
        self.name = input("New Customer, please enter your name: ")         # prompt user to input new customer name
        self.budget = float(input("Please enter your budget: "))            # prompt user to input new customer budget

    def new_shopping_list(self, stock_list):
        """
        Method to prompt user to input product items &
        product quanties to create the new shopping list
        Parameters:
            -stock_list : shop ProductStock list
        """
        available_items = []                                                # create a list of the available stock items
        for item in stock_list:                                             # loop through items in shop stock list &
            available_items.append(item.name())                             # append to available stock list

        cust_prod = input("Enter a product name: ")                         # prompt user to input product name

        if cust_prod in available_items:                                    # if input customer product is available
            for item in stock_list:                                         # loop through items in stock list &
                if cust_prod == item.name():                                # identify product & quantity available
                    qty = item.quantity                                     
            p = Product(cust_prod)
        else:                                                               # notify user if input product is not available
            print("Product Not Available")
            return None

        cust_qty = int(input("Enter quantity: "))                           # prompt user for to input quantity of products

        if cust_qty <= qty:                                                 # check if quantity of products is available
            q = cust_qty
            ps = ProductStock(p, q)
        else:
            print("Product Quantity Not Available")                         # notify user if quantity is not available
            return None

        self.shopping_list.append(ps)                                       # append available products & quantities to new customer shopping list
        

class Shop:
    """
    Shop Class to store shop's cash & stock list info
    """

    def __init__(self, path):
        """
        Method to initialize the object with info imported from a csv file
        Parameters:
            -path : file path to shop csv file
        """
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, int(row[2]))
                self.stock.append(ps)

    def update_cash(self, sold):
        """
        Method to update shop cash
        """
        self.cash += sold

    def update_stock(self, sold_items):
        for sold in sold_items:
            for stock_item in self.stock:
                if (stock_item.name() == sold.name()):
                    stock_item.quantity -= sold.quantity

    def __repr__(self):
        """
        Returns a easy to read tabulated string as a representation of the Shop Class
        """
        str = f"\n"
        str += f'SHOP CASH: {self.cash}\n'
        str += f'SHOP PRODUCT STOCK LIST:\n'
        str += ("{:<15} {:<15} {:<15}".format('Product Name', 'Quantity', 'Price(€)'))
        for item in self.stock:
            str += f"\n{item.product.name:<17}"
            str += f"{item.quantity:<15}"
            str += f"{item.product.price}"
        return str


def main():
    """
    Main Python Program
    """
    print("WELCOME TO THE SHOP")
    app_display()	
    s = Shop("../stock.csv")
    c = Customer("../customer.csv")
    								

    while True:
        choice = input("Choice: ")

		# Choice 1 - Import Customer's Details & Shopping List	
        if (choice == "1"):											
            print("Import Customer's Details & Shopping List")									
            print("=" * 41)

            c.calculate_costs(s.stock)	
            print(c)

            bill = c.order_cost()
        
            print(f'\n\t\tTotal Cost: \t{bill}\n')

            if c.budget < bill:
                print("Customer has insufficenet Funds - ORDER NOT PROCESSED")
            else:
                s.update_cash(bill)
                s.update_stock(c.shopping_list)
                # print(s)
            
            app_display()


        # Choice 2 - Live Mode
        elif (choice == "2"):								
            print("\t\tLive Mode")							
            print("=" * 41)

            nc = newCustomer()

            while choice != "p":
                nc.new_shopping_list(s.stock)
                nc.calculate_costs(s.stock)
                choice = input("Would you like to pay <p> or continue shopping <c>?")
                
            print(nc)

            bill = nc.order_cost()

            print(f'\n\t\tTotal Cost: \t{bill}\n')

            if nc.budget < bill:
                print("Customer has insufficenet Funds - ORDER NOT PROCESSED")
            else:
                s.update_cash(bill)
                s.update_stock(nc.shopping_list)
                # print(s)

            app_display()

        # Choice 3 - Check Shop Stock
        elif (choice == "3"):								
            print("Check Shop Stock")							
            print("=" * 41)

            print(s)
            print("\n")

            app_display()


        # Choice x - Close Program
        elif (choice == "x"):								
            # Exit Application
            print("Close Program")
            break;
    

def app_display():
    """
    Python Program Display Options
    """
    # Print choice options to screen
    print("\t\t| MENU |")
    print("1 - Import Customer's Details & Shopping List")
    print("2 - Live Mode")
    print("3 - Check Shop Stock")
    print("x - Exit application")

if __name__ == "__main__": 
	main()
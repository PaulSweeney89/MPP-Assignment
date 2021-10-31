# Python Shop Program
# MULTI-PARADIGM PROGRAMMING 2021


from dataclasses import dataclass
from typing import List
import csv

# Define the program dataclasses

@dataclass
class Product:
    name: str
    price: float

@dataclass
class ProductStock:
    product: Product
    quantity: int

@dataclass
class Shop:
    cash: float
    stock: List[ProductStock]

@dataclass
class Customer:
    name: str
    budget: float
    shopping_list: List[ProductStock]

# Define the program methods

def create_and_stock_shop():
    """
    Function to retrieve & return shop product stock
    from the 'stock.csv' file
    """
    s = Shop('', [])
    with open('stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header_row = next(csv_reader)                           # skip header row at start of 'for loop'
        s.cash = float(header_row[0])                           # shop cash reserve
        for row in csv_reader:
            p = Product(row[0], float(row[1]))                  # Product inputs: (name, price)
            ps = ProductStock(p, float(row[2]))                 # ProductStock inputs: (Product, quantity)
            s.stock.append(ps)
    return s


def get_customer():
    """
    Function to retrieve the Customer's name, budget & 
    shopping list from the 'customer.csv' file
    """
    with open('customer.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header_row = next(csv_reader)                           # skip header row at start of 'for loop'
        c = Customer(header_row[0], float(header_row[1]), [])          # Customer inputs: (name, budget, shopping_list)
        for row in csv_reader:
            price = get_product_price(row[0])                   # get product price
            p = Product(row[0], price)                          # Product inputs: (name, price)
            ps = ProductStock(p, float(row[1]))                 # ProductStock inputs: (Product, quantity)
            c.shopping_list.append(ps)
    return c


def get_product_price(prod_name):
    """
    Function to retrieve the product price for inputted 
    product name from the stock csv file
    """
    with open('stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if prod_name == row[0]:
                price = float(row[1])
                return price


def get_product_qty(prod_name):
    """
    Function to retrieve the product quantity for inputted 
    product name from the stock csv file
    """
    with open('stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if prod_name == row[0]:
                qty = float(row[2])
                return qty


def check_product_stock(prod_name):
    """
    Function to check the product stock
    returns True if product available 
    returns False if product not available
    """
    with open('stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if prod_name == row[0]:
                return True

        return False


def input_product():
    """
    Function to prompt user to input Product Name in Live Mode
    """
    while True:
        try:
            prod_name = input("Enter a product name: ")
            if check_product_stock(prod_name) == False:
                raise Exception
        except Exception:
            print("Please enter an available product name!\n")
        else:
            return prod_name


def input_quantity(prod_name):
    """
    Function to prompt user to input Quantity in Live
    checks input quantity against available stock quantity for 
    the input product name 
    """
    while True:
        try:
            qty = int(input("Enter quantity: "))
            if qty > get_product_qty(prod_name):
                raise Exception
        except Exception:
            print("Please enter a valid quantity")
        else:
            return qty


def calc_bill(c):
    """
    Function to calculate Customer's total bill
    """
    costs = []
    for item in c.shopping_list:
        qty = int(item.quantity)
        price = item.product.price
        cost = round((qty * price), 2)
        costs.append(cost)
    bill = sum(costs)
    return bill


def print_product(p):
    """
    Function to output the product's name & price
    """
    print(f'Product Name: {p.name} Product Price: {p.price}')


def print_customer(c):
    """
    Function to output the customer's name, shopping list
    & total cost spent
    """
    print(f'CUSTOMER NAME: {c.name}')
    print(f'BUDGET: €{c.budget}')
    print("SHOPPING LIST:")
    print ("{:<15} {:<15} {:<15}".format('Product Name', 'Quantity', 'Price(€)'))
    for item in c.shopping_list:
        prod_name = item.product.name
        qty = int(item.quantity)
        price = item.product.price
        cost = round((qty * price), 2)
        print ("{:<15} {:<15} {:<15}".format(prod_name, qty, cost))


def print_shop(s):
    """
    Function to output the shop's cash reserve & product stock list
    """
    print(f'SHOP CASH: {s.cash} \n')
    print("SHOP PRODUCT STOCK LIST:")
    print ("{:<15} {:<15} {:<15}".format('Product Name', 'Quantity', 'Price(€)'))
    for item in s.stock:
        prod_name = item.product.name
        price = item.product.price
        qty = int(item.quantity)
        print ("{:<15} {:<15} {:<15}".format(prod_name, qty, price))


def main():
    """
    Main Python Program
    """
    s = create_and_stock_shop()

    print("WELCOME TO THE SHOP")
    app_display()											

    while True:
        choice = input("Choice: ")

		# Choice 1 - Import Customer's Details & Shopping List	
        if (choice == "1"):											
            print("Import Customer's Details & Shopping List")									
            print("=" * 41)

            c = get_customer()
            print_customer(c)

            bill_csv = calc_bill(c)
            print(f'\n\t\tTotal Cost: \t{bill_csv}\n')

            if bill_csv > c.budget:
                print("Customer has insufficenet Funds - ORDER NOT PROCESSED")
            else:
                s.cash += bill_csv

            app_display()


        # Choice 2 - Live Mode
        elif (choice == "2"):								
            print("\t\tLive Mode")							
            print("=" * 41)

            cust_name = input("New Customer, please enter your name: ")
            cust_budget = float(input("Please enter your budget: "))

            new_customer = Customer(cust_name, cust_budget, [])

            while choice != "p":

                cust_prod = input_product()
                cust_qty = input_quantity(cust_prod)

                price = get_product_price(cust_prod)
                product = Product(cust_prod, price)
                ps = ProductStock(product, cust_qty)
                new_customer.shopping_list.append(ps)

                choice = input("Would you like to pay <p> or continue shopping <c>?")
            
            print("\n\t\tNew Customer")							
            print("=" * 41)
            print_customer(new_customer)

            bill_live = calc_bill(new_customer)
            print(f'\n\t\tTotal Cost: \t{bill_live}\n')

            if bill_live > new_customer.budget:
                print("Customer has insufficenet Funds - ORDER NOT PROCESSED")
            else:
                s.cash += bill_live
            
            app_display()

        # Choice 3 - Check Shop Stock
        elif (choice == "3"):								
            print("Check Shop Stock")							
            print("=" * 41)

            print_shop(s)

            app_display()

        # Choice x - Close Program
        elif (choice == "x"):								
            # Exit Application
            print("Close Program")
            break;
    
    # Store Cash
    # s.cash = s.cash + b
    # print(s.cash)

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

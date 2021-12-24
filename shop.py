# Python Shop Program
# MULTI-PARADIGM PROGRAMMING 2021


from dataclasses import dataclass, field
from typing import List
import csv

# Define the program dataclasses

@dataclass
class Product:
    name: str
    price: float = 0.0

@dataclass
class ProductStock:
    product: Product
    quantity: int

@dataclass
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)

# Define the program methods

def create_and_stock_shop():
    """
    Function to retrieve & return shop product stock
    from the 'stock.csv' file
    """
    s = Shop()
    with open('stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header_row = next(csv_reader)                           # skip header row at start of 'for loop'
        s.cash = float(header_row[0])                           # shop cash reserve
        for row in csv_reader:
            p = Product(row[0], float(row[1]))                  # Product inputs: (name, price)
            ps = ProductStock(p, float(row[2]))                 # ProductStock inputs: (Product, quantity)
            s.stock.append(ps)
    return s


def read_customer(file_path):
    """
    Function to retrieve the Customer's name, budget & 
    shopping list from the 'customer.csv' file
    """
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header_row = next(csv_reader)                           # skip header row at start of 'for loop'
        c = Customer(header_row[0], float(header_row[1]), [])   # Customer inputs: (name, budget, shopping_list)
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
    - returns True if product available 
    - returns False if product not available
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
            prod_name = input("Enter a product name: ")             # prompt user to input product name
            if check_product_stock(prod_name) == False:             # check if user input product is within shop stock        
                raise Exception                                     
        except Exception:                                           # notify user if product not in stock
            print("Please enter an available product name!\n")      
        else:
            return prod_name                                        # return product name if in stock


def input_quantity(prod_name):
    """
    Function to prompt user to input Quantity in Live
    checks input quantity against available stock quantity for 
    the input product name 
    """
    while True:
        try:
            qty = int(input("Enter quantity: "))                    # prompt user to input product quantity   
            if qty > get_product_qty(prod_name):                    # check if product qunatity is available in shop stock
                raise Exception
        except Exception:                                           # notify user if product quantity is not available
            print("Please enter a valid quantity")
        else:
            return qty


def calc_bill(c):
    """
    Function to calculate Customer's total bill
    """
    costs = []                                                      # list of product costs
    for item in c.shopping_list:                                    # loop through items in shopping list
        qty = int(item.quantity)                                    # quantity variable
        price = item.product.price                                  # price variable
        cost = round((qty * price), 2)                              # calculate cost of product
        costs.append(cost)                                          # append product cost to list 'costs'
    bill = sum(costs)                                               # sum of 'costs'
    return bill                                                     

# UPDATE STOCK NOT WORKING CORRECTLY - RECHECK
def update_stock(customer, shop):
    """
    Function to reduce shop stock quantities 
    by number of products sold
    """
    for item in customer.shopping_list:                             # loop through items in customer's shopping list
        stk_qty = get_product_qty(item.product.name)                # get shop product current stock quantity
        updated_qty = stk_qty - item.quantity                       # updated shop stock quntity (current qty - sold qty)
        for i in shop.stock:                                        # loop through items in shop stock
            if item.product.name == i.product.name:                 # identify products sold in shop stock
                i.quantity = updated_qty                            # update shop stock qty
    
    return shop

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
    print("WELCOME TO THE SHOP")
    app_display()	
    open_shop = create_and_stock_shop()										

    while True:
        choice = input("Choice: ")

		# Choice 1 - Import Customer's Details & Shopping List	
        if (choice == "1"):											
            print("Import Customer's Details & Shopping List")									
            print("=" * 41)

            # read customer from csv file
            customer = read_customer("customer.csv")
            # output customer details
            print_customer(customer)

            # calculate & output customer's total bill
            bill_csv = calc_bill(customer)
            print(f'\n\t\tTotal Cost: \t{bill_csv}\n')

            # check if customer has sufficent funds
            if bill_csv > customer.budget:
                print("Customer has insufficenet funds - ORDER NOT PROCESSED")
            else:
                # update shop cash
                open_shop.cash += bill_csv

                # UPDATE STOCK NOT WORKING CORRECTLY - RECHECK
                open_shop = update_stock(customer, open_shop)
                # print_shop(open_shop)

            app_display()


        # Choice 2 - Live Mode
        elif (choice == "2"):								
            print("\t\tLive Mode")							
            print("=" * 41)

            # input prompts for new customer details
            cust_name = input("New Customer, please enter your name: ")
            cust_budget = float(input("Please enter your budget: "))

            new_customer = Customer(cust_name, cust_budget, [])

            # while loop - choice does not = "p" (to pay)
            while choice != "p":

                # input prompt for product name
                cust_prod = input_product()
                # input prompt for product quantity
                cust_qty = input_quantity(cust_prod)

                # retrieve product cost
                price = get_product_price(cust_prod)

                product = Product(cust_prod, price)
                ps = ProductStock(product, cust_qty)
                # append to new customer shoopping list
                new_customer.shopping_list.append(ps)

                choice = input("Would you like to pay <p> or continue shopping <c>?")
            
            print("\n\t\tNew Customer")							
            print("=" * 41)
            # Output new customer detail & shopping list
            print_customer(new_customer)

            # calculate new customer's bill
            bill_live = calc_bill(new_customer)
            print(f'\n\t\tTotal Cost: \t{bill_live}\n')

            # check if new customer has sufficent funds
            if bill_live > new_customer.budget:
                print("Customer has insufficenet Funds - ORDER NOT PROCESSED")
            else:
                open_shop.cash += bill_live

                # UPDATE STOCK NOT WORKING CORRECTLY - RECHECK
                open_shop = update_stock(new_customer, open_shop)
                #print_shop(s)
            
            app_display()

        # Choice 3 - Check Shop Stock
        elif (choice == "3"):								
            print("Check Shop Stock")							
            print("=" * 41)

            # Output shop stock list & cash reserve
            print_shop(open_shop)

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
    
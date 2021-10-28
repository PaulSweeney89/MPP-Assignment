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
    from the stock csv file
    """
    s = Shop(200.0, [])
    with open('stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            p = Product(row[0], float(row[1]))                  # Product inputs: (name, price)
            ps = ProductStock(p, float(row[2]))                 # ProductStock inputs: (Product, quantity)
            s.stock.append(ps)
    return s


def get_customer():
    """
    Function to retrieve the Customer's name, budget & 
    shopping list from the customer csv file
    """
    with open('customer.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        header_row = next(csv_reader)                           # skip header row at start of 'for loop'
        c = Customer(header_row[0], header_row[1], [])          # Customer inputs: (name, budget, shopping_list)
        for row in csv_reader:
            price = get_product_price(row[0])                   # get product price
            p = Product(row[0], price)                          # Product inputs: (name, price)
            ps = ProductStock(p, float(row[1]))                 # ProductStock inputs: (Product, quantity)
            c.shopping_list.append(ps)
    return c


def get_product_price(p_name):
    """
    Function to retrieve the product price for inputted 
    product name from the stock csv file
    """
    with open('stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if p_name == row[0]:
                price = float(row[1])
                return price


def print_product(p):
    """
    Function to output the product's name & price
    """
    print(f'\n PRODUCT NAME: {p.name} \nPRODUCT PRICE: {p.price}')


def print_customer(c):
    """
    Function to output the customer's name, budget & shopping list
    """
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')

    for item in c.shopping_list:
        print_product(item.product)

        print(f'{c.name} ORDERS {item.quantity} OF ABOVE PRODUCT')
        cost = item.quantity * item.product.price
        print(f'THe COST TO {c.name} WILL BE €{cost}')


def print_shop(s):
    """
    Function to output the shop's cash reserve & product stock list
    """
    print(f'SHOP HAS {s.cash}')
    for item in s.stock:
        print_product(item.product)
        print(f' THE SHOP HAS {item.quantity} OF THE ABOVE')

# s = create_and_stock_shop()
#print_shop(s)
c = get_customer()
print_customer(c)
# x = "can of coke"
# p = get_product_price(x)
# print(p)




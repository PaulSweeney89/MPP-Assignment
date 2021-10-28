// # c Shop Program
// MULTI-PARADIGM PROGRAMMING 2021

# include <stdio.h>
# include <string.h>
# include <stdlib.h>

// Define the program structure types 

struct Product {
    char* name;
    double price;
};

struct ProductStock {
    struct Product product;
    int quantity;
};

struct Customer {
    char* name;
    double budget;
    struct ProductStock shoppingList[10];
    int index;
};

struct Shop {
    double cash;
    struct ProductStock stock[20];
    int index;
};


// Define the program methods

/*
 * Function to output the product's name & price
 */
void printProduct(struct Product p)
{
    printf("PRODUCT NAME: %s \nPRODUCT PRICE: %.2f\n", p.name, p.price);
    printf("--------------------\n");
}


/*
 * Function to output the Customer's name, budget, shopping list & cost
 */
void printCustomer(struct Customer c)
{
    printf("CUSTOMER NAME: %s \nCUSTOMER Budget: %.2f\n", c.name, c.budget);
    printf("--------------------\n");
    for(int i = 0; i < c.index; i ++){
        printProduct(c.shoppingList[i].product);
        printf("%s ORDERS %d of ABOVE PRODUCT\n", c.name, c.shoppingList[i].quantity);
        double cost = c.shoppingList[i].quantity * c.shoppingList[i].product.price;
        printf("The cost to %s will be €%.2f\n", c.name, cost);
    }
}


/*
 * Function to retrieve & return shop product stock from csv file
 */
struct Shop createAndStockShop()
{
    struct Shop shop = { 200 };
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("stock.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    while ((read = getline(&line, &len, fp)) != -1) {
        char *n = strtok(line, ",");
        char *p = strtok(NULL, ",");
        char *q = strtok(NULL, ",");
        int quantity = atoi(q);
        double price = atof(p);
        char *name = malloc(sizeof(char) * 50);
        strcpy(name, n);
        struct Product product = { name, price };
        struct ProductStock stockItem = { product, quantity };
        shop.stock[shop.index++] = stockItem;
        // printf("NAME OF PRODUCT: %s PRICE: %.2f QUANTITY: %d \n" , name, price, quantity);
    }

    return shop;
}


/*
 * Function to output the shops cash reserve & product stocklist
 */
void printShop(struct Shop s){

    printf("Shop has %.2f in cash\n", s.cash);
    for (int i =0; i <s.index; i++)
    {
        printProduct(s.stock[i].product);
        printf("THE SHOP HAS %d of the above\n", s.stock[i].quantity);
    }
}

// Program main method
int main(void)
{

    struct Shop shop = createAndStockShop();
    printShop(shop);

    return 0;
}
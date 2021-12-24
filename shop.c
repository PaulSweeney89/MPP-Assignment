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
 * Function to retrieve & return shop product stock from csv file
 */
struct Shop createAndStockShop()
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("stock.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

	read = getline(&line, &len, fp);
	float cash = atof(line);
	// printf("cash in shop is %.2f\n", cash);
	
	struct Shop shop = { cash };

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
    }
	
	return shop;
}

/*
 * Function to retrieve product name from shop stock
 */
struct Product getProduct(struct Shop s, char* pname)
{
    struct Product p;

    for (int i = 0; i < s.index; i++){
        if(strcmp(s.stock[i].product.name, pname)==0){
            p = s.stock[i].product;
        }
    }
    return p;
}


/*
 * Function to retrieve & return Customer's details & shopping list from csv file
 */
struct Customer readCustomer(struct Shop s)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("customer.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

	read = getline(&line, &len, fp);
	char *c = strtok(line, ",");
    char *cname = malloc(sizeof(char) * 50);
	strcpy(cname, c);
    char *b = strtok(NULL, ",");
    double budget = atof(b);

    struct Customer customer = {cname, budget};

    while ((read = getline(&line, &len, fp)) != -1) {
		char *n = strtok(line, ",");
        char *q = strtok(NULL, ",");
        int quantity = atoi(q);
		char *pname = malloc(sizeof(char) * 50);
		strcpy(pname, n);
		struct Product product = { pname, getProduct(s, pname).price};
		struct ProductStock shopItem = { product, quantity };
		customer.shoppingList[customer.index++] = shopItem;
    }
	
	return customer;
}

double calcBill(struct Customer c)
{
    float bill = 0;

    for (int i = 0; i < c.index; i++){
        float b = (c.shoppingList[i].product.price) * (c.shoppingList[i].quantity);
        bill += b;
    }
    return bill;
}


/*
 * Function to output the product's name & price
 */
void printProductName(struct Product p)
{
    printf("%s", p.name);
}

void printProduct(struct Product p)
{
    printf("%s %.2f", p.name, p.price);
}


/*
 * Function to output the Customer's name, budget, shopping list & cost
 */
void printCustomer(struct Customer c)
{
    printf("CUSTOMER NAME: %s \nBudget: €%.2f\n", c.name, c.budget);
    printf("SHOPPING LIST:\n");
    printf("Product Name");
    printf("%20s", "Quantity");
    printf("%20s", "Price(€)\n");
    for(int i = 0; i < c.index; i ++){
        printProductName(c.shoppingList[i].product);
        int qty = c.shoppingList[i].quantity;
        double cost = c.shoppingList[i].quantity * c.shoppingList[i].product.price;
        printf("%20s", "");
        printf("%d", qty);
        printf("%20s", "");
        printf("%.2f", cost);
        printf("\n");
    }
}


/*
 * Function to output the shops cash reserve & product stocklist
 */
void printShop(struct Shop s){

    printf("SHOP CASH: %.2f", s.cash);
    printf("\n\nProduct Name");
    printf("%20s", "Quantity");
    printf("%20s", "Price(€)\n");
    for(int i = 0; i < s.index; i ++){
        printProductName(s.stock[i].product);
        int qty = s.stock[i].quantity;
        double cost = s.stock[i].quantity * s.stock[i].product.price;
        printf("%20s", "");
        printf("%d", qty);
        printf("%15s", "");
        printf("%.2f", cost);
        printf("\n");
    }
}

void app_display(struct Shop s)
{    
    struct Customer c = readCustomer(s);
    // printCustomer(c);

    printf("%20s", "");
    printf("| MENU |");
    printf("\n1 - Import Customer's Details & Shopping List");
    printf("\n2 - Live Mode");
    printf("\n3 - Check Shop Stock");
    printf("\nx - Exit application");

    int choice = -1;

	while (choice != 0){
		
		fflush(stdin);
		printf("\nPlease choose an option ");
		scanf("%d", &choice);

		if (choice == 1)
		{
			printf("Import Customer's Details & Shopping List");									
            printf("\n=========================================\n");
            struct Customer c = readCustomer(s);
            printCustomer(c);

            float bill = calcBill(c);
            printf("%40s", "");
            printf("Total Cost: %.2f", bill);

            if (bill > c.budget){
                printf("Customer has insufficenet Funds - ORDER NOT PROCESSED");
            }

            else if (bill <= c.budget){
                s.cash += bill;
            }
		} 

        else if (choice == 2)
        {
            struct Customer newCust;

            char* custName = malloc(sizeof(char)*50);
            int custBudget;
            

            printf("%20s", "");
			printf("Live Mode");							
            printf("\n=========================================\n");

            fflush(stdin);
            printf("New Customer, please enter your name:\n");
            scanf("%s", custName);
            printf("Customer Name: %s \n", custName);

            fflush(stdin);
            printf("Please enter your budget:");
            scanf("%d", &custBudget);
            printf("Customer Budget: %d \n", custBudget);
            fflush(stdin);

            newCust.name = custName;
            newCust.budget = custBudget;

            char pay;
            newCust.index = 0;

            while (strcmp(&pay, "p") != 0)
            {

                fflush(stdin);
                printf("Enter Product Name:\n");
                char* custProd = malloc(sizeof(char)*50);
                scanf("\n%[^\n]%*c", custProd);
                printf("Product: %s \n", custProd);
                printf("\n");

                struct Product newCustProds = {custProd, getProduct(s, custProd).price};

                fflush(stdin);
                printf("Enter Quantity:");
                int custQty;
                scanf("%d", &custQty);
                printf("Quantity: %d \n", custQty);
                fflush(stdin);

                struct ProductStock newCustShoppingList = {newCustProds, custQty};

                printf("Pay <p> or Continue Shopping <c>:");
                printf("\n");
                fflush(stdin);
                scanf("%s", &pay);

                newCust.shoppingList[newCust.index] = newCustShoppingList;
                newCust.index++;
            }


            printCustomer(newCust);

            float bill = calcBill(newCust);
            printf("%40s", "");
            printf("Total Cost: %.2f", bill);

            if (bill > newCust.budget){
                printf("Customer has insufficenet Funds - ORDER NOT PROCESSED");
            }

            else if (bill <= newCust.budget){
                s.cash += bill;
            }            
        }


        else if (choice == 3)
        {
            printf("Check Shop Stock");							
            printf("\n=========================================\n");

            printShop(s);
		} 

        else if (choice == 4)
        {
            printf("Close Program");
			break;
	    }
    }
}



// Program main method
int main(void)
{

    struct Shop s = createAndStockShop();
    // printShop(s);

    app_display(s);

    struct Customer c = readCustomer(s);
    // float bill = calcBill(c);
    // printf("%f", bill);
    // printCustomer(c);


    return 0;
}

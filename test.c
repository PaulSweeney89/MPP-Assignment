#include <stdio.h>
#include <string.h>
int main (void)
{
    int addProd = 1;
    char prodName[20];
    int qty;
    char payCont[4];
    int prods, c;
    char *p;
    for (prods = 0; prods<addProd; prods++)
    {
        printf("Enter Product:\n");
        fgets(prodName, 20, stdin);
        //Remove `\n` from the name.
        if ((p=strchr(prodName, '\n')) != NULL)
            *p = '\0';
        printf("%s\n", prodName);

        fflush(stdin);
        printf("Enter Quantity:\n");
        scanf("%d", &qty);
        //Remove `\n` from the name.
        // if ((p=strchr(qty, '\n')) != NULL)
        //     *p = '\0';
        printf("%d\n", qty);


        printf("Would you like to pay <p> or continue shopping <c>\n");
        scanf(" %s", payCont);
        if (strcmp(ayCont, "c")==0)
        {
            addProd++;
        }
        //Remove the \n from input stream
        while ( (c = getchar()) != '\n' && c != EOF );
    }
    return 0;
}//end main
# serversideFinal
# serversideFinal
##carts:

https://127.0.0.1:8000/haitiApp/carts/


###GET:
    This returns all the carts in the database
    
    
###Post: 
    Input: None

    Output: 
    [{"id": 1, "customer_id": 1, "totalPrice": "0.00"}]

##cartsByID 

https://127.0.0.1:8000/haitiApp/carts/{id}


###GET:
    this gets cart with specific id
    
###Patch:
    Input {'name':'ProductName', 'method' : 'ADD'}

    Output: [{"id": 1, "customer_id": 1, "totalPrice": "3.00"}]
    
   
###DELETE:
    this deletes the specific cart


##Order:
https://127.0.0.1:8000/haitiApp/orders/

###GET
    this gets all order in the database
    
    
###POST
    INPUT {"cartID": 1}
    OUTPUT: [{"id": 2, "customer_id": 1, "orderDate": "2019-05-14T21:01:29.745Z", "status": "Order Received", "cartID_id": 1}

##Order by ID
https://127.0.0.1:8000/haitiApp/orders/{id}


###GET
    gets the order with specific ID
    
    
###Patch
    INPUT {"status: "Order Received"}
    Output {"id": 3, "customer_id": 1, "orderDate": "2019-05-14T21:02:02.375Z", "status": "Order Received", "cartID_id": 1}


###DELETE
    this deletes specific order with the id


##Vendors:


##GET:
    this returns all user who are customers

##patchVendor:


##PATCH:

https://127.0.0.1:8000/haitiApp/vendors/{id}
    input:
    isVendor: Boolean(True/False)

##DELETE:

    this deletes specific user who are vendors

##Farmers:

##GET: 
this returns all user who are farmers




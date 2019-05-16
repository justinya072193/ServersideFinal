# serversideFinal
# serversideFinal
## carts:

https://127.0.0.1:8000/haitiApp/carts/


### GET:
    This returns all the carts in the database
    
    
### Post: 
    Input: None

    Output: 
    [{"id": 1, "customer_id": 1, "totalPrice": "0.00"}]

## cartsByID 

https://127.0.0.1:8000/haitiApp/carts/{id}


### GET:
    this gets cart with specific id
    
### Patch:
    Input {'name':'ProductName', 'method' : 'ADD'}

    Output: [{"id": 1, "customer_id": 1, "totalPrice": "3.00"}]
    
   
### DELETE:
    this deletes the specific cart


## Order:
https://127.0.0.1:8000/haitiApp/orders/

### GET
    this gets all order in the database
    
    
### POST
    INPUT {"cartID": 1}
    OUTPUT: [{"id": 2, "customer_id": 1, "orderDate": "2019-05-14T21:01:29.745Z", "status": "Order Received", "cartID_id": 1}

## Order by ID
https://127.0.0.1:8000/haitiApp/orders/{id}


### GET
    gets the order with specific ID
    
    
### Patch
    INPUT {"status: "Order Received"}
    Output {"id": 3, "customer_id": 1, "orderDate": "2019-05-14T21:02:02.375Z", "status": "Order Received", "cartID_id": 1}


### DELETE
    this deletes specific order with the id


## Vendors:


## GET:
    this returns all user who are customers

## patchVendor:


## PATCH:

https://127.0.0.1:8000/haitiApp/vendors/{id}
    input:
    isVendor: Boolean(True/False)

## DELETE:

    this deletes specific user who are vendors

## Farmers:

## GET: 
this returns all user who are farmers


## products/create

https://127.0.0.1:8000/products/create

User must be logged in and has admin access (customer object "isAdmin" field is True) to use. 
If not authenticated, returns HTTP response Bad Request.

## GET:
    
    This returns a form to create a new product.

## POST:
    
    Submits form to create a new product.

## products/

https://127.0.0.1:8000/products/

Login required for all methods.

## GET:

    Returns all product details

        [{
            "id": 1,
            "productName": "Test Product",
            "productDescription": "Test Description",
            "productPrice": "10.00",
            "productImages": [
                {
                    "id": 1,
                    "product_id": 1,
                    "img": "products/productImages/Haiti-Coffee-Products_ElQ83Vq.png",
                    "uploadedAt": "2019-05-15T21:27:46.702Z"
                }
            ]
        }]

## PATCH:

    Changes a products details with a request body. User must be admin.

    Input:
        {
            "id": 1,
            "productName": "Test Product changed",
            "productDescription": "Test Description changed",
            "productPrice": "1.00",
        }

    Response:

        {
            "id": 1,
            "productName": "Test Product changed",
            "productDescription": "Test Description changed",
            "productPrice": “1.00",
            "productImages": [
                {
                    "id": 1,
                    "product_id": 1,
                    "img": "products/productImages/Haiti-Coffee-Products_ElQ83Vq.png",
                    "uploadedAt": "2019-05-15T21:27:46.702Z"
                }
            ]
        }

## DELETE:

    Deletes a product and related images. User must be admin

    Input:
        {
            "id":1
        }

    Response:

        "Deleted product and related images successfully."

## products/<int:product_id>/manage-images

https://127.0.0.1:8000/products/1/manage-images

User must be logged in and have admin status to use.

## GET:

    Returns form to add an image to the product specified in url.

## POST:
    
    Submits form to add the image to the product.

## DELETE:

    Deletes an image for the product specified in url.

    Input:
        {
            "id":1
        }

    Response:

        Deleted Image successfully.

## products/<int:product_id>/images

https://127.0.0.1:8000/products/1/images

## GET:
    
    Returns all images for given product.

    Response:
        [
            {
                "id": 3,
                "product_id": 2,
                "img": "products/productImages/Screen_Shot_2019-05-15_at_2.26.43_PM.png",
                "uploadedAt": "2019-05-15T22:22:04.815Z"
                }
        ]

## haitiApp/users/create-address

https://127.0.0.1:8000/haitiApp/users/create-address

User must be logged in.

## GET:

    Returns form to create address for user.

## POST:

    Submits form to add address to user profile.

## haitiApp/users/address

https://127.0.0.1:8000/haitiApp/users/address

User must be logged in.

## GET:

    Return current users addresses.

    Response:
        {
            "id": 1,
            "addressLine1": "1234 5th Ave NW",
            "addressLine2": "",
            "city": "Seattle",
            "state": "WA",
            "postalCode": "98105",
            "country": "United States"
        }

## PATCH:

    Updates the current users address with input from user via JSON input in request body.

    Input:
        {
            "id": 1,
            "addressLine1": "2345 5th Ave NW",
            "addressLine2": "",
            "city": "Seattle",
            "state": "WA",
            "postalCode": "98105",
            "country": "United States"
        }

    Response:
        {
            "id": 1,
            "addressLine1": "2345 5th Ave NW",
            "addressLine2": "",
            "city": "Seattle",
            "state": "WA",
            "postalCode": "98105",
            "country": "United States"
        }

## DELETE:
    
    Deletes an address from current users profile given via JSON input in request body.

    Input:
        {
            "id":1
        }

    Response:
        "Deleted address successfully."


## auth

    These endpoints behave all the same except they link the User to a Customer object to extend the user fields.

    I have included a function "testAdmin" to create an Admin user to test other endpoints for this assignment.




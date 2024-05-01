import json
import datetime
from decimal import Decimal
from sqlalchemy import func
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with, reqparse
from .models import  *
from .instances import cache



api = Api(prefix = '/api')

############ CATEGORY DETAILS ############
CategoryDetails = reqparse.RequestParser()
CategoryDetails.add_argument('categoryName')
CategoryDetails.add_argument('categoryDescription')



response_fields = {
    "messageId" : fields.String,
    "message"   : fields.String
}

## Category API
class Category(Resource):
    @auth_required("token")
    # @cache.cached(timeout=50)
    def get(self):
        all_categories = db.session.query(Categories).all()
        categories_list = []

        user_role = current_user.roles[-1]

        if user_role == "admin":

            for category in all_categories:
                category_data = {
                    "name":         category.categoryname,
                    "description":  category.categoryDescription,
                    "active":       category.categoryactive
                }
                categories_list.append(category_data)
   
        else:

            for category in all_categories:
                if category.categoryactive:
                    category_data = {
                        "name":         category.categoryname,
                        "description":  category.categoryDescription
                    }
                    categories_list.append(category_data)

        
        return categories_list

    @marshal_with(response_fields)
    @auth_required("token")
    @roles_required("admin")
    def put(self, categoryName):
        args = CategoryDetails.parse_args()
        category = db.session.query(Categories).filter(Categories.categoryname == args["categoryName"]).first()
    

        if category is None:
            Error = {"messageId": "C002", "message": "The provided Category does not exist."}
            return Error, 404 

        if (category.categoryDescription == args["categoryDescription"]):
            Error = {"messageId": "P008", "message": "The provided entry remains the same."}, 400
            return Error

        else:  
            
            category.categoryDescription = args["categoryDescription"] 
            db.session.commit()
            success = {"messageId": "200OK", "message": "The Category was Modified successfully."}
            return success


    @auth_required("token")
    # @roles_required("admin")
    @roles_accepted("admin", "manager")
    @marshal_with(response_fields)
    def post(self):
        args = CategoryDetails.parse_args()
        category = db.session.query(Categories).filter(Categories.categoryname == args["categoryName"]).first()

        user_role = current_user.roles[-1]

        if  user_role == "admin":
            if category is None :
                new_category  = Categories(
                        categoryname         = args["categoryName"],
                        categoryDescription  = args["categoryDescription"],
                        categoryactive       = True   
                        )
                
                db.session.add(new_category)
                db.session.commit()

                success = {"messageId": "200OK", "message": "The Category was created successfully."}

                return success
            else:
                Error = {"messageId": "C001", "message": "The provided Category already exists."}, 400
                return Error
            

        if  user_role == "manager":
            if category is None :
                new_category  = Categories(
                        categoryname         = args["categoryName"],
                        categoryDescription  = args["categoryDescription"],
                        categoryactive       = False   
                        )
                
                db.session.add(new_category)
                db.session.commit()

                success = {"messageId": "200OK", "message": "The Category was created successfully. Kindly wait for the Admin Approval."}

                return success
            else:
                Error = {"messageId": "C001", "message": "The provided Category already exists."}, 400
                return Error
          #contains all the request arguments

    
    @auth_required("token") 
    @roles_required("admin")
    # @cache.cached(timeout=50)
    @marshal_with(response_fields)
    def delete(self, categoryName):

        category = db.session.query(Categories).filter(Categories.categoryname == categoryName).first()

        if category:
            db.session.delete(category)
            db.session.commit()
            success =  {"messageId": "200OK", "message": "The Category was deleted successfully."}
            return success

        if category is None:
            Error = {"messageId": "C002", "message": "The provided Category does not exist."}
            return Error, 400
        

  
api.add_resource(Category, "/admin/categories", "/admin/categories/<string:categoryName>")


############ PRODUCT DETAILS ############

ProductDetails = reqparse.RequestParser()

ProductDetails.add_argument('categoryName')
ProductDetails.add_argument('productName')
ProductDetails.add_argument('productDescription')
ProductDetails.add_argument('productPrice')
ProductDetails.add_argument('productStockQuantity')
ProductDetails.add_argument('productUOM')





## Product API
class Product(Resource):

    @auth_required("token")
    def get(self):
        all_products = db.session.query(Products, Categories).join(Categories, Categories.categoryid == Products.categoryId).all()
        products_list = []

        for product in all_products:
            product_data = {
                "productName":         product.Products.productName,
                "categoryName":        product.Categories.categoryname,  
                "productDescription":  product.Products.ProductDescription,
                "price":               str(product.Products.price),     ## To be converted back to decimal later
                "quantity":            str(product.Products.quantity),  ## To be converted back to decimal later
                "uom":                 product.Products.uom            
                }
            products_list.append(product_data)
        return products_list
    
  
    @auth_required("token")
    @roles_required("manager")
    @marshal_with(response_fields)
    def put(self):
        args = ProductDetails.parse_args()
        product = db.session.query(Products).filter(Products.productname == args["productName"]).first()

        if (product.ProductDescription == args["ProductDescription"] & product.price == args["productPrice"] & product.quantity == args["productStockQuantity"]  & product.uom == args["productUOM"]):
            
            Error = {"messageId": "P008", "message": "The provided entry remains the same."}, 400
            return Error

        else:  
            product.ProductDescription = args["ProductDescription"] 
            product.price = args["productPrice"] 
            product.quantity = args["productStockQuantity"]  
            product.uom = args["productUOM"]

            db.session.commit()
            success = {"messageId": "200OK", "message": "The Product was Modified successfully."}
            return success

    @auth_required("token")
    @roles_required("manager")
    @marshal_with(response_fields)
    def post(self):
        args = ProductDetails.parse_args()
        product = db.session.query(Products).filter(Products.productName == args["productName"]).first()
        category =  db.session.query(Categories).filter(Categories.categoryname == args["categoryName"]).first()

        if product is None:

            if int(args["productPrice"]) <= 0:
                Error = {"messageId": "P001", "message": "The price entered for the product cannot be less than or equal to Zero. Kindly enter a price higher than zero."}
                return Error, 400
            
            if int(args["productStockQuantity"]) <= 0:
                Error = {"messageId": "P002", "message": "The Stock Quantity entered for the product cannot be less than or equal to Zero. Kindly enter a quantity higher than zero."}
                return Error, 400


            if category is None:
                Error = {"messageId": "P003", "message": "The entered Category does not exist. Kindly enter a valid Category."}
                return Error, 400
            
            new_product  = Products(
                    productName         = args["productName"],
                    ProductDescription  = args["productDescription"],
                    quantity            = args["productStockQuantity"],
                    price               = args["productPrice"],
                    uom                 = args["productUOM"],
                    categoryId          = category.categoryid
                    )
            
            db.session.add(new_product)
            db.session.commit()

            success =  {"messageId": "200OK", "message": "The Product was added successfully."}
            return success
            
        else:
            
            Error = {"messageId": "P004", "message": "The Product already exists. Kindly enter a new Product."}
            return Error, 400
        
    
    @auth_required("token")
    @roles_required("manager")
    @marshal_with(response_fields)
    def delete(self, productName):
        
        product = db.session.query(Products).filter(Products.productName == productName).first()
        # category = db.session.query(Categories).filter(Categories.categoryname == categoryName).first()

        if product is None:
            Error = {"messageId": "P006", "message": "The provided Product does not exist."}
            return Error, 400
        
        
        db.session.delete(product)
        db.session.commit()

        success = {"messageId": "200OK", "message": "The Product was deleted successfully."}
        return success
        
api.add_resource(Product, "/admin/product", "/admin/product/<string:productName>")


# ############ MARKET DETAILS ############

class Market(Resource):

    @auth_required("token")
    def get(self):        
        categories = Categories.query.all()

        cat_prodcuts = []


        for category in categories:
            data = {
            'category_id': category.categoryid,
            'category_name': category.categoryname,
            'category_description': category.categoryDescription,
            'products': [
                {
                    'product_id': product.productId,
                    'product_name': product.productName,
                    'product_description': product.ProductDescription,
                    'price': float(product.price),
                    'quantity': float(product.quantity),
                    'uom': product.uom
                }
                    for product in category.products
                ]
            }
            cat_prodcuts.append(data)
        return cat_prodcuts

api.add_resource(Market, "/admin/market")


# ############ SHOPPING CART ############

CartDetails = reqparse.RequestParser()

CartDetails.add_argument('product_id')
CartDetails.add_argument('qty_requested')

class ShoppingCart(Resource):

    #To display the shopping cart    
    @auth_required("token")
    @roles_required("shopper")
    def get(self):
        allCart = db.session.query(cartDetails).all()
        all_items = []

        for cart in allCart:
            data = {
                'id'            :   cart.cardId, 
                'user_id'       :   cart.userId,
                'product_id'    :   cart.productId,
                'product_name'  :   cart.product.productName,
                'category_name' :   cart.product.category.categoryname,
                'qty_requested' :   float(cart.qtyrequested),
                'net_price'     :   float(cart.netprice),
                'uom'           :   cart.product.uom,
                'active'        :   cart.cartactive
            }

            all_items.append(data)

        return all_items
    
    # To edit the quantity
    @auth_required("token")
    @roles_required("shopper")
    def put(self):
        args = CartDetails.parse_args()
        user_id = current_user.id
        product = db.session.query(Products).filter(Products.productId == args["product_id"]).first() 
        cartitem = db.session.query(cartDetails).filter(cartDetails.productId == args["product_id"]).filter(cartDetails.userId == user_id).first() 
        
        qty_requested = float(args["qty_requested"])

        if qty_requested<0:
            Error = {"messageId": "C001", "message": "The quantity requested is less than zero. Kindly enter a valid Quantity."}
            return Error, 400
            
        if qty_requested == 0:
            Error = {"messageId": "C003", "message": "The requested quantity is 0. Kindly enter a valid Quantity."}
            return Error, 400
        
        net_price   = product.price * Decimal(qty_requested)

        cartitem.qtyrequested = qty_requested
        cartitem.netprice     = net_price
        db.session.commit()
            
        success = {"messageId": "200OK", "message": "The Item was modified successfully."}
        return success



    
    # To add to the shopping cart
    @auth_required("token")
    @roles_required("shopper")
    def post(self):
        args = CartDetails.parse_args()
        user_id = current_user.id
        product = db.session.query(Products).filter(Products.productId == args["product_id"]).first() 
        cartitem = db.session.query(cartDetails).filter(cartDetails.productId == args["product_id"]).filter(cartDetails.userId == user_id).first() 
        qty_requested = float(args["qty_requested"])


        if qty_requested<0:
            Error = {"messageId": "C001", "message": "The quantity requested is less than zero. Kindly enter a valid Quantity."}
            return Error, 400
            
        if qty_requested == 0:
            Error = {"messageId": "C003", "message": "The requested quantity is 0. Kindly enter a valid Quantity."}
            return Error, 400


        if not cartitem:
            if product.quantity < qty_requested:
                Error = {"messageId": "C001", "message": "The quantity requested exceeds the requested quantity. Kindly enter a valid Quantity."}
                return Error, 400
                        
            net_price = product.price * Decimal(qty_requested)

            new_cart_item = cartDetails(
                userId          =   user_id,
                productId       =   args["product_id"],
                qtyrequested    =   qty_requested,
                netprice        =   net_price,
                cartactive      =   False

            )

            db.session.add(new_cart_item)
            db.session.commit()

            message  = "{quantity} {uom} of item {prodname} was added to the cart successfully. Kindly check the bottom of the page for cart modification.".format(quantity = qty_requested, uom = product.uom, prodname = product.productName)
                

            success =  {"messageId": "200OK", "message": message}
            return success
        

        else:
            modified_qty = cartitem.qtyrequested + Decimal(qty_requested)

            if product.quantity < modified_qty:
                Error = {"messageId": "C004", "message": "The quantity requested exceeds the requested quantity. Kindly enter a valid Quantity."}
                return Error, 400
            
            net_price    = product.price * Decimal(modified_qty)

            cartitem.qtyrequested = modified_qty
            cartitem.netprice = net_price


            db.session.commit()
            
            message  = "{quantity} {uom} of item {prodname} was added to the cart successfully. Kindly check the bottom of the page for cart modification.".format(quantity = modified_qty, uom = product.uom, prodname = product.productName)
            success = {"messageId": "200OK", "message": message}
            return success


    # To delete from the shopping cart
    @auth_required("token")
    @roles_required("shopper")
    def delete(self, productId):
        user_id = current_user.id
        cartitem = db.session.query(cartDetails).filter(cartDetails.productId == productId).filter(cartDetails.userId == user_id).first() 
        # category = db.session.query(Categories).filter(Categories.categoryname == categoryName).first()

        if cartitem is None:
            Error = {"messageId": "C005", "message": "The provided Item does not exist."}
            return Error, 400
        
        
        db.session.delete(cartitem)
        db.session.commit()

        success = {"messageId": "200OK", "message": "The Item was removed from the Cart Successfully."}
        return success

api.add_resource(ShoppingCart, "/admin/cart", "/admin/cart/<int:productId>")


# ############ SUMMARY CART ############

class SummaryCart(Resource):

    @auth_required("token")
    @roles_required("shopper")
    def post(self):

        # 1) Fetch the cart items placed for user where items are active (user id needed)
        user_id = current_user.id
        cart_items = db.session.query(cartDetails).filter(cartDetails.userId==user_id).filter(cartDetails.cartactive == True).all() 
        total_price = 0
        items_data = []

        # 2) Convert the cart item details into json, remove Qty from Products amd delete the Cart item details.
        for cart_item in cart_items:
            total_price += cart_item.netprice
            item_dict = {
                "productId":    cart_item.productId,
                "qtyrequested": float(cart_item.qtyrequested),
                "categoryId":   cart_item.product.categoryId,
                "netprice":     float(cart_item.netprice)          
            }
            items_data.append(item_dict)

            # product = db.session.query(Products).filter(Products.productId == cart_item.productId).first() 
            cart_item.product.quantity -= cart_item.qtyrequested

            db.session.delete(cart_item)
            

        # 3) Obtain the other parameters and insert into the Order Table

        items_json = json.dumps(items_data)
        order_date = datetime.datetime.now()
        order_status = "Placed"
        
        new_order = OrderDetails(
                userId          = user_id,
                orderDate       = order_date,
                orderstatus     = order_status,
                items           = items_json,
                totalprice      = total_price
            )

        db.session.add(new_order)
        

        db.session.commit()

            

        success =  {"messageId": "200OK", "message": "Order Placed Successfully."}
        return success
        

    @auth_required("token")
    @roles_required("shopper")
    def delete(self):
        user_id = current_user.id
        cart_items = db.session.query(cartDetails).filter_by(userId=user_id).all() 

        for cart_item in cart_items:
            db.session.delete(cart_item)

        db.session.commit()

        success = {"messageId": "200OK", "message": "All the Items were successfully removed from the cart."}
        return success

api.add_resource(SummaryCart, "/admin/summary")



# # ############ ORDER DETAILS ############

# class Order(Resource):

#     def get(self):

#         all_orders = OrderDetails.query.all()
#         unique_dates = db.session.query(func.date(OrderDetails.orderDate)).distinct().all()


#         cat_prodcuts = []

#         for date in unique_dates:
#             orders_date = db.session.query(OrderDetails).filter(func.date(OrderDetails.orderDate) == date).all()
#             total_price = 0
#             orders_placed = []
#             email = 

#             for order in orders_date:
#                 total_price += order.totalprice
#                 items_array = json.loads(OrderDetails.items)
                
#                 items_list = [item for item in items_array]
    



#             data = {
#             'category_id': category.categoryid,
#             'category_name': category.categoryname,
#             'category_description': category.categoryDescription,
#             'products': [
#                 {
#                     'product_id': product.productId,
#                     'product_name': product.productName,
#                     'product_description': product.ProductDescription,
#                     'price': float(product.price),
#                     'quantity': float(product.quantity),
#                     'uom': product.uom
#                 }
#                     for product in category.products
#                 ]
#             }
#             cat_prodcuts.append(data)
#         return cat_prodcuts
#     # [{date,ttlprice,[{ord,em,cat,prod,qty,subt}]},{date,ttlprice,[{ord,em,cat,prod,qty,subt}]}]




    
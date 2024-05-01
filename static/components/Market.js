
export default {
    template: `
    <div>
    <div class="container-fluid mt-5 bg-light">
      <h2>Market</h2>

      <div v-for="category in fetchCategoryProduct" :key="category.category_id">
        <h4>{{ category.category_name }}</h4>

          <table>
            <thead>
              <tr>
                <th>Product Name</th>
                <th>Product Description</th>
                <th>Price</th>
                <th>Stock Quantity</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in category.products" :key="product.product_id">

                <td>{{ product.product_name }}</td>
                <td>{{ product.product_description }}</td>
                <td>Rs. {{ product.price.toFixed(2) }}</td>
                <td>{{ product.quantity }} {{ product.uom }}</td>
                <td>
                  <input type="number" placeholder="Quantity" v-model="requestedQty"/>
                  <button class="btn btn-sm btn-success" @click="purchaseProduct(product.product_id)">
                    Purchase?
                  </button>
                </td>
              </tr>


            </tbody>
          </table>
      </div>
    </div>
    
    <div class="container-fluid mt-5 bg-light">
      <h2>Summary</h2>
      <table>
            <thead>
              <tr>
                <th>Product Name</th>
                <th>Requested Quantity</th>
                <th>Calculated Price</th>
                <th>Modify Qty.</th>
                <th>Send to Cart?</th>
                <th>Delete?</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="cartItem in fetchShoppingCart" :key="cartItem.id">

                <td>{{ cartItem.product_name }}</td>
                <td>{{ cartItem.qty_requested }} {{cartItem.uom}}</td>
                <td>
                  Rs. {{ cartItem.net_price.toFixed(2) }}
                </td>
                <td>
                  <input type="number" placeholder="Quantity" v-model="modifiedQty"/>
                  <button class="btn btn-sm btn-warning" @click="modifyItem(cartItem.product_id)">
                    Modify Qty.?
                  </button>
                </td>
                <td>
                  <button class="btn btn-success" v-if="!cartItem.active" @click="confirmItem(cartItem.product_id)">Confirm</button>
                  <p v-else>Sent to Cart</p>
                </td>
                <td>
                  <button class="btn btn-danger" @click="deleteItem(cartItem.product_id)">Delete</button>
                </td>
              </tr>
            </tbody>

      </table>
    </div>
  </div>`,
     
 
    data() {
        return {
            fetchCategoryProduct: null,
            fetchShoppingCart: null,
            requestedQty:null,
            modifiedQty: null,

            token: localStorage.getItem('auth-token'),
          };
    },

    
  
    methods: {
        // Fetches the list of products based on categories
        async fetchProductsByCategory() {

          const catProd = await fetch('/api/admin/market', {
            headers: {
              'Authentication-Token': this.token,
              'Content-Type': 'application/json',
            }
          })

          const data = await catProd.json().catch((e) => {})
          if (catProd.ok) {

              this.fetchCategoryProduct = data
              console.log('CAT PROD data:', this.fetchCategoryProduct);
          } else {
              this.error = cat.status
          }       
        },
      
        // Executes the post api on click of Purchase
        async purchaseProduct(productId) {
          
          const requestBody = {
            product_id    :   productId,
            qty_requested :   this.requestedQty,
          }

          const response = await fetch(`/api/admin/cart`, {
            method: 'POST',
            headers: {
                'Authentication-Token': this.token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
          })
          
          const data = await response.json()
          if (response.ok) {
            alert(data.message)
            location.reload()
            }
          else{
            alert(data.message)
          };


        },


        // Executes on click of delete
        async deleteItem(productId) {
          const del = await fetch(`/api/admin/cart/${productId}`, {
              method: 'DELETE',
              headers: {
              'Authentication-Token': this.token,
              'Content-Type': 'application/json'
            },
          })
          const data = await del.json();
          if (del.ok) {
            alert(data.message);
            window.location.reload();
          }
        },

        // Executes on modification of qty.
        async modifyItem(productId) {

          const requestBody = {
            product_id    :   productId,
            qty_requested :   this.modifiedQty,
          }

          const response = await fetch(`/api/admin/cart`, {
            method: 'PUT',
            headers: {
                'Authentication-Token': this.token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
          })
          
          const data = await response.json()
          if (response.ok) {
            alert(data.message)
            location.reload()
            }
          else{
            alert(data.message)
          };
        },

        async confirmItem(prodId) {
          const cat = await fetch(`/activate/item/${prodId}`, {
            headers: {
              'Authentication-Token': this.token,
            },
          })
          const data = await cat.json()
          if (cat.ok) {
            alert(data.message)
            location.reload(); 
          }
        }
   
    },
  
    async mounted() {         
        //  fetches list of categories and products
      this.fetchProductsByCategory();

      //  fetches list items in the shopping cart
      const cart = await fetch('/api/admin/cart', {
        headers: {
        'Authentication-Token': this.token,
        },
      })
      const data = await cart.json().catch((e) => {})

      if (cart.ok) {
          this.fetchShoppingCart = data
          console.log('CART: ', this.fetchShoppingCart)
      } else {
          this.error = cart.status
      }


    },
              
}

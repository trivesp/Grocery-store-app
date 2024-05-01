
export default {
    template: `<div>
    <div class = "container-fluid mt-5 bg-light">
      <h1>Orders Placed</h1>

        <div class = "container-fluid mt-5">
            <h4>Current Date</h4>
            <table>
                <thead>
                <tr>
                    <th>Order No            </th>
                    <th>User Email          </th>
                    <th>Category            </th>
                    <th>Product             </th>
                    <th>Quantity Ordered    </th>
                    <th>Price               </th>
                </tr>
                </thead>

                <tbody>
                <tr v-for="cartItem in dayPurchases" > 
                    <th>Order No            </th>
                    <th>User Email          </th>
                    <th>Category            </th>
                    <th>Product             </th>
                    <th>Quantity Ordered    </th>
                    <th>Sub-Total           </th>
                </tr>
                </tbody>
            </table>

            <h4 class = "mt-5 x-3"> Total Price :          Rs. {{ totalPrice }} <h4>
        </div>

        
        
    </div>`,
 


    data() {
      return {
        fetchShoppingCart: null,

        token: localStorage.getItem('auth-token'),
      };
    },

    computed:{
      totalPrice(){
        return this.fetchShoppingCart.filter(item => item.active).reduce((acc, item) => acc + item.net_price, 0);
      }
    },

  
    methods: {
      async createProduct(){
          const cat = await fetch('/api/admin/product', {
              method: 'POST',
              headers: {
                'Authentication-Token': this.token,
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(this.product),
            })

            const data = await cat.json()
            if (cat.ok) {
              alert(data.message)
              window.location.reload();
              }
            else{
              alert(data.message)
            }

      },

      async clearAll(){
        const del = await fetch(`/api/admin/summary`, {
          method: 'DELETE',
          headers: {
          'Authentication-Token': this.token,
          'Content-Type': 'application/json'
          },
        })
        const data = await del.json();
        if (del.ok) {
          alert(data.message);
          location.reload()
        }
      
      },
    },

    async mounted() {         
      //  fetches list items in the shopping cart
      const cart = await fetch('/api/admin/cart', {
        headers: {
        'Authentication-Token': this.token,
        },
      })
      const data = await cart.json().catch((e) => {})

      if (cart.ok) {
          this.fetchShoppingCart = data
      } else {
          this.error = cart.status
      }


    },
        
        
}




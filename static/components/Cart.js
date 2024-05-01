
export default {
    template: `<div>
    <div class = "container-fluid mt-5 bg-light">
      <h1>Shopping Cart</h1>

      <table>
        <thead>
          <tr>
            <th>Product Name  </th>
            <th>Category      </th>
            <th>Quantity      </th>
            <th>Sub-Total     </th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="cartItem in fetchShoppingCart" :key="cartItem.id" v-if="cartItem.active">
            <td>{{ cartItem.product_name }}                    </td>
            <td>{{ cartItem.category_name }}                   </td>
            <td>{{ cartItem.qty_requested }} {{cartItem.uom}}  </td>
            <td>Rs. {{ cartItem.net_price.toFixed(2) }}        </td>
          </tr>
        </tbody>
      </table>

      <h4 class = "mt-5 x-3"> Total Price :          Rs. {{ totalPrice }} <h4>

      <div class="container-fluid mt-5 bg-light vertical-center">
        <button class="btn btn-lg btn-success" @click="checkOut()"> Check Out! </button>
        <button class="btn btn-lg btn-danger" @click="clearAll()"> Clear All</button>
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
      async checkOut(){
        const cout = await fetch(`/api/admin/summary`, {
          method: 'POST',
          headers: {
          'Authentication-Token': this.token,
          'Content-Type': 'application/json'
          },
        })
        const data = await cout.json();
        if (cout.ok) {
          alert(data.message);
          location.reload()
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




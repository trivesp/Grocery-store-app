
export default {
    template: `<div>

    <div class = "container-fluid mt-5 bg-light">
        <h3>Create a New Category</h3>
        <p> Please note that this needs to be approved by the Administrator.</p>
        <input type="text" placeholder="Category Name" v-model="category.categoryName"/>
        <input type="text" placeholder="Category Description" v-model="category.categoryDescription" />
        <button class = "btn btn-success" @click="createCategory"> Create Category</button>
    </div>


    <div class = "container-fluid mt-5 bg-light">
        <h3>Create a New Product</h3>
        <input type="text" placeholder="Product Name" v-model="product.productName"/>
        <input type="text" placeholder="Product Description" v-model="product.productDescription" />

        <select class="form-select" aria-label="Categories" name="productcat" v-model="product.categoryName" required>
          <option selected value = "">Select the Category</option>
          <option v-for="category in fetchCategories" :value="category.name">{{ category.name }}</option>

      </select>


        <input type="number" placeholder="Price" v-model="product.productPrice" />
        <input type="number" placeholder="Stock Quantity" v-model="product.productStockQuantity" />

        <select class="form-select" aria-label="ProductQtyUnit" name="productqtyunit" v-model="product.productUOM" required>
          <option selected value = "">Select the default Unit</option>
          <option value="Units">Units</option>
          <option value="Kg">Kilograms (Kg)</option>
          <option value="G">Grams (g)</option>
          <option value="L">Liters (L)</option>
          <option value="g">MilliLiters (ml)</option>
        </select>

        <button class = "btn btn-success" @click="createProduct"> Create Product</button>
    </div>


    
    <div class = "container-fluid mt-5 bg-light">
    <h3>View all the existing Products</h3>
    <table>
        <thead>
            <tr>
                <th>Product Name            </th>
                <th>Product Description     </th>
                <th>Category     </th>
                <th>Price     </th>
                <th>Quantity     </th>
                <th>Delete?     </th>
            </tr>
        </thead>
        
        <tbody>
          <tr v-for="product in fetchProduct" :key="product.productName">
            <td>{{ product.productName }}</td>
            <td>{{ product.productDescription }}</td>
            <td>{{ product.categoryName }}</td>
            <td>Rs. {{ parseFloat(product.price).toFixed(2) }} / {{ product.uom }}</td>
            <td> {{ parseFloat(product.quantity).toFixed(2) }} {{product.uom}}</td>
            <td><button class="btn btn-danger" @click="deleteProduct(product.productName)">Delete</button></td>
          </tr>
        
        </tbody>
    </table>

    </div>
    </div>`,
 
    data() {
      return {
        fetchProduct: [],
        fetchCategories: [],
        category:{
          categoryName: null,
          categoryDescription: null          
        },
        product: {
          productName: null,
          productDescription: null,
          categoryName: null,
          productPrice: null,
          productStockQuantity: null,
          productUOM: null
        },
        token: localStorage.getItem('auth-token'),
      }
    },

  
    methods: {
                  async createCategory(){
                    const cat = await fetch('/api/admin/categories', {
                        method: 'POST',
                        headers: {
                          'Authentication-Token': this.token,
                          'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(this.category),
                      })

                      const data = await cat.json()
                      if (cat.ok) {
                        alert(data.message)
                        location.reload()
                        }
                      else{
                        alert(data.message)
                      }

                },

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

                async deleteProduct(productName) {
                  const del = await fetch(`/api/admin/product/${productName}`, {
                      method: 'DELETE',
                      headers: {
                          'Authentication-Token': this.token,
                          'Content-Type': 'application/json',
                      },
                  });
              
                  const data = await del.json();
              
                  if (del.ok) {
                      alert(data.message);
                      window.location.reload();
                  }
                }
              ,
            },



            async mounted() {
              //  fetch list of categories
                const cat = await fetch('/api/admin/categories', {
                    headers: {
                      'Authentication-Token': this.token,
                    },
                })

              //  fetch list of products
                const prod = await fetch('/api/admin/product', {
                  headers: {
                  'Authentication-Token': this.token,
                  },
              })


              const datacat = await cat.json().catch((e) => {});
              if (cat.ok) {
                  console.log('Category data:', datacat);
                  this.fetchCategories = datacat;
              } else {
                  this.error = cat.status;
              }
          
              const dataprod = await prod.json().catch((e) => {});
              if (prod.ok) {
                  console.log('Product data:', dataprod);
                  this.fetchProduct = dataprod;
              } else {
                  this.error = prod.status;
              }

              },
        
        
        }




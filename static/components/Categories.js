
export default {
    template: `<div>
    <div class = "container-fluid mt-5 bg-light">
        <h3>Create a New Category</h3>
        <input type="text" placeholder="Category Name" v-model="category.categoryName"/>
        <input type="text" placeholder="Category Description" v-model="category.categoryDescription" />
        <button class = "btn btn-success" @click="createCategory"> Create Category</button>
    </div>

    <div class = "container-fluid mt-5 bg-light">
    <h3>View all the existing Categories</h3>
    <table>
        <thead>
            <tr>
                <th>Category Name            </th>
                <th>Category Description     </th>
                <th>Delete Category?     </th>
                <th>Modify Category?     </th>
                <th>Approved Category? </th>
            </tr>
        </thead>
        
        <tbody>
          <tr v-for="category in fetchCategories" :key="category.name">
              <td>{{ category.name }}</td>
              <td>{{ category.description }}</td>
              <td>
                <button class="btn btn-danger" @click="deleteCategory(category.name)">Delete</button>
              </td>

              <td>
                <input type="text" placeholder="Modified Category Description" v-model="modifiedDescription" />
                <button class="btn btn-warning" @click="modifyCategory(category.name)">Modify</button>
              </td>
              <td>
                <button class="btn btn-primary" v-if="!category.active" @click="approvecat(category.name)">Activate Category?</button>
                <p v-else>Approved</p>
              </td>

            
          </tr>
        </tbody>

    </table>

    </div>
    </div>`,
  
    data() {
      return {
        fetchCategories: [],
        modifiedDescription: null,
        category: {
          categoryName: null,
          categoryDescription: null,
          // categoryActive:null,
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
                      console.log("testdata ",data )
                      if (cat.ok) {
                        alert(data.message)
                        location.reload()
                        }
                      else{
                        alert(data.message)
                      }

                },

                async approvecat(catname) {
                  const cat = await fetch(`/activate/category/${catname}`, {
                    headers: {
                      'Authentication-Token': this.token,
                    },
                  })
                  const data = await cat.json()
                  if (cat.ok) {
                    alert(data.message)
                    location.reload(); 
          
                  }
                },


                async deleteCategory(catname) {
                    const del = await fetch(`/api/admin/categories/${catname}`, {
                        method: 'DELETE',
                        headers: {
                        'Authentication-Token': this.token,
                        'Content-Type': 'application/json'
                      },
                    })
                    const data = await del.json();
                    if (del.ok) {
                      alert(data.message);
                      this.fetchCategories = this.fetchCategories.filter(category => category.name !== categoryName);
                      location.reload()
                    }
                

                },

                async modifyCategory(catname) {

                  const modifiedCategory = {
                      categoryName: catname,
                      categoryDescription: this.modifiedDescription,
                  };


              
                  const response = await fetch(`/api/admin/categories/${catname}`, {
                      method: 'PUT',
                      headers: {
                          'Authentication-Token': this.token,
                          'Content-Type': 'application/json',
                      },
                      body: JSON.stringify(modifiedCategory),
                  })
                  
                  const data = await response.json()
                      if (response.ok) {
                        alert(data.message)
                        location.reload()
                        }
                      else{
                        alert(data.message)
                      };
              
                  // Handle the response as needed
              }
              
              //   async modifyCategory(catname) {
              //     const modifiedCategory = {
              //       categoryDescription: this.category.categoryModDescription,
              //   };
            
              //     console.log('cattest')
              //     console.log(this.category)
              //     const response = await fetch(`/api/admin/categories/${catname}`, {
              //         method: 'PUT',
              //         headers: {
              //             'Authentication-Token': this.token,
              //             'Content-Type': 'application/json',
              //         },
              //         body: JSON.stringify(modifiedCategory),
              //     });
              
              // }
              ,
              
            },



            async mounted() {
                const cat = await fetch('/api/admin/categories', {
                    headers: {
                    'Authentication-Token': this.token,
                    },
                })
                const data = await cat.json().catch((e) => {})

                if (cat.ok) {
                    this.fetchCategories = data
                } else {
                    this.error = cat.status
                }
            },
        
        
        }




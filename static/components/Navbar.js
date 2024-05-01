export default {
    template: `
    <nav class="navbar navbar-expand-lg bg-success">
    <div class="container-fluid">
       <a class="navbar-brand" href="#">Grocery Store</a>
     <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
       <span class="navbar-toggler-icon"></span>
     </button>
     <div class="collapse navbar-collapse" id="navbarNavDropdown">
       <ul class="navbar-nav">

         <li class="nav-item" v-if="role=='admin'">
           <router-link class="nav-link" to="/users">Users</router-link>
         </li>

         <li class="nav-item" v-if="role=='admin'">
           <router-link class="nav-link" to="/category">Categories</router-link>
         </li>

         <li class="nav-item" v-if="role=='manager'">
           <router-link class="nav-link" to="/product">Products</router-link>
         </li>

          <li class="nav-item" v-if="role=='manager'">
            <router-link class="nav-link" to="/orders">Orders</router-link>
          </li>

         <li class="nav-item" v-if="role=='shopper'">
           <router-link class="nav-link" to="/market">Market</router-link>
         </li>

         <li class="nav-item" v-if="role=='shopper'">
           <router-link class="nav-link" to="/cart">Shopping Cart</router-link>
         </li>

         <li class="nav-item" v-if="is_login">
           <button class="nav-link" @click='logout' >logout</button>
         </li>
   
       </ul>


     </div>
    </div>
   </nav>`,
    data() {
      return {
        role: localStorage.getItem('role'),
        is_login: localStorage.getItem('auth-token'),
      }
    },
    methods: {
      logout() {
        localStorage.removeItem('auth-token')
        localStorage.removeItem('role')
        this.$router.push({ path: '/login' })
      },
    },
  }
// `<nav class="navbar navbar-expand-lg bg-success">
//      <div class="container-fluid">
//         <a class="navbar-brand" href="#"><bold>GrocStore</bold></a>
//       <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
//         <span class="navbar-toggler-icon"></span>
//       </button>
//       <div class="collapse navbar-collapse" id="navbarNavDropdown">
//         <ul class="navbar-nav">
//           <li class="nav-item">
//             <router-link class="nav-link active" aria-current="page" to="/">Home</router-link>
//           </li>

//           <li class="nav-item" v-if="role=='admin'">
//             <router-link class="nav-link" to="/users">Users</router-link>
//           </li>

//           <li class="nav-item" v-if="role=='admin'">
//             <router-link class="nav-link" to="/users">Categories</router-link>
//           </li>

//           <li class="nav-item" v-if="role=='manager'">
//             <router-link class="nav-link" to="/products">Products</router-link>
//           </li>

//           <li class="nav-item" v-if="role=='shopper'">
//             <router-link class="nav-link" to="/products">Shopping Cart</router-link>
//           </li>


//           <li class="nav-item" v-if="is_login">
//             <button class="nav-link" @click='logout' >logout</button>
//           </li>
    
//         </ul>


//       </div>
//      </div>
//     </nav>
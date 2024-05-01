import Home from './components/home.js'
import Login from './components/login.js'
import signup from './components/Signup.js'
import AdminAllUsers from './components/AdminAllUsers.js'
import Categories from './components/Categories.js'
import Products from './components/Products.js'
import Cart from './components/Cart.js'
import Market from './components/Market.js'
import Orders from './components/Orders.js'


const routes = [
    {path: '/', component: Home, name : Home},
    {path: '/login', component: Login, name: Login},
    {path: '/signup', component: signup},
    {path: '/users', component: AdminAllUsers },
    {path: '/category', component: Categories },
    {path: '/product', component: Products },
    {path: '/cart', component: Cart },
    {path: '/market', component: Market },
    {path: '/orders', component: Orders },
]

export default new VueRouter({
    routes,
})
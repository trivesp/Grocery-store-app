import AdminHome from "./AdminHome.js"
import ShopperHome from "./ShopperHome.js" 
import StoreManagerHome from "./StoreManagerHome.js" 

export default {
    template: `<div>
    <AdminHome v-if="userRole=='admin'" />
    <ShopperHome v-if="userRole=='shopper'" />
    <StoreManagerHome v-if="userRole=='manager'" />
    </div>`,

    data()  {
        return {
        userRole: localStorage.get('role'),
        authToken: localStorage.get('auth-token')
        }
    },
    components: {
        AdminHome,
        ShopperHome,
        StoreManagerHome,
    },
}

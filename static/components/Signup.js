export default {
    template: `<div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="row border rounded-3 p-3 bg-white shadow-lg box-area" style="width:500px">
        <div class="col rounded-4 justify-content-center align-items-center flex-column border">
            <div class="row align-items-center">
                
                <form>
                    <div class="header-text mb-4 text-center">
                        <h1 style = "font-family: Poppins, sans-serif;">Sign Up</h1>
                    </div>
                
                    <div class="form-outline input-group mb-3">
                        <input type="text" class="form-control form-control-lg bi-light fs-6" placeholder = "Name" name = "Name" v-model="cred.Name">   
                    </div>

                    <div class="form-outline input-group mb-3">
                        <input type="email" class="form-control form-control-lg bi-light fs-6" placeholder = "example@email.com" name = "email" v-model="cred.email">   
                    </div>

                    <div class="form-outline input-group mb-3">
                        <input type="password" class="form-control form-control-lg bi-light fs-6" placeholder = "Password" name = "password" v-model="cred.password">   
                    </div>

                    <div class="form-outline input-group mb-5">
                        <input type="password" class="form-control form-control-lg bi-light fs-6" placeholder = "Re-enter Password" name = "password2" v-model="cred.password2">   
                    </div>

            
                    <div class="input-group mb-3 d-flex justify-content-center">
                        <button class="btn btn-lg btn-success mx-5" type = "submit" @click='register'>Register</button>
                    </div>

                    <div class="input-group mb-3 d-flex justify-content-center">
                        <div class="signup">
                            <button class="btn btn-secondary mx-5 mb-2" type = "submit" name = "go" @click='backtologin'>Return back to login screen</button>
                        </div>   
                    </div>

                    <div class='text-success'>{{success}}</div>
                    <div class='text-danger'>*{{error}}</div>

                </form>
            </div>
            
        </div>

    </div>

</div>`,
data(){
 return{
     cred:{
         "Name" : null,
         "email": null,
         "password": null,
         "password2": null
     },
     error: null,

 }
},

methods: {
    async register() {

        console.log("async register begin")

        const res = await fetch('/user-signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.cred),
        })
        console.log(res)
        const data = await res.json()
        if (res.ok) {
          console.log(data)
          alert("User created successfully.")
          this.$router.push({ path: '/login' })
        } else {
            alert(data.message)
            this.error = data.message
        }
        console.log("async login end")
      },

      backtologin(){
        console.log('backtologin')
        this.$router.push({ path: '/login' })
      },
    },
}
export default {
    template: `<div>
    <div v-if="error"> {{error}}</div>


    <div class="container justify-content-center align-items-center mt-5">
        <table class = "styled-table">
                <thead>
                    <tr>
                        <th>User Email          </th>
                        <th>User Role          </th>
                        <th>Approval Status     </th>
                        <th>Manager ?     </th>
                    </tr>
                </thead>

                <tbody>
                <tr v-for="user in fetchUsers" :key="user.id">
                    <td>{{ user.email }}</td>
                    <td>{{ user.role }}</td>
                    <td>
                      <button class="btn btn-primary" v-if="!user.active" @click="approve(user.id)">Approve</button>
                    </td>
                    <td>
                      <button class="btn btn-warning" v-if='user.role === "Common Shopper"' @click="shift(user.id)">Manager</button>
                    </td>
                </tr>
              </tbody>

        </table>

        </div>
    
    </div>`,
    data() {
      return {
        fetchUsers: [],
        token: localStorage.getItem('auth-token'),
        error: null,
      }
    },
    methods: {
      async approve(manId) {
        const res = await fetch(`/activate/manager/${manId}`, {
          headers: {
            'Authentication-Token': this.token,
          },
        })
        const data = await res.json()
        if (res.ok) {
          alert(data.message)
          location.reload(); 

        }
      },

      async shift(manId) {
        const res = await fetch(`/shift/user/${manId}`, {
          headers: {
            'Authentication-Token': this.token,
          },
        })
        const data = await res.json()
        if (res.ok) {
          alert(data.message)
          location.reload(); 

        }
      }

    },
    async mounted() {
      const res = await fetch('/users', {
        headers: {
          'Authentication-Token': this.token,
        },
      })
      const data = await res.json().catch((e) => {})
      if (res.ok) {
        console.log(data.role)
        this.fetchUsers = data
      } else {
        this.error = res.status
      }
    },
  }
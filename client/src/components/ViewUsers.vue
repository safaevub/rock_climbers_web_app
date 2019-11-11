<template>
    <div class="container">
        <div class="jumbotron mt-5">
            <div class="col-sm-8 mx-auto">
              <h1 class="text-center">Users</h1>
              <table class="table col-md-10 mx-auto">
                <tbody>
                  <div v-for="(single,index) in user_info" :key="index">
                    <td>User: {{user_info[index]["name"]}}</td>
                    <router-link
                      :to= 'user_info[index]["link"]'
                      v-slot="{ href, route, navigate, isActive, isExactActive }">
                      <td
                        :class="[isActive && 'router-link-active', isExactActive && 'router-link-exact-active']">
                        <a :href="href" @click="navigate">View entries</a>
                      </td>
                    </router-link>
                    <router-link
                      :to= 'user_info[index]["viewLicense"]'
                      v-slot="{ href, route, navigate, isActive, isExactActive }">
                      <td
                        :class="[isActive && 'router-link-active', isExactActive && 'router-link-exact-active']">
                        <a :href="href" @click="navigate">View license</a>
                      </td>
                    </router-link>
                    <router-link
                      :to= 'user_info[index]["giveLicense"]'
                      v-slot="{ href, route, navigate, isActive, isExactActive }">
                      <td
                        :class="[isActive && 'router-link-active', isExactActive && 'router-link-exact-active']">
                        <a :href="href" @click="navigate">Give license</a>
                      </td>
                    </router-link>
                  </div>
                </tbody>
              </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import jwtDecode from 'jwt-decode'

export default {
  data () {
    const token = localStorage.usertoken
    const decoded = jwtDecode(token)
    return {
      user_info: [
        {

        }
      ],
      first_name: decoded.identity.first_name,
      last_name: decoded.identity.last_name,
      email: decoded.identity.email,
      id: decoded.identity.id

    }
  },
  methods: {
    view_users () {
      const path = 'http://localhost:5000/viewusers'
      axios.get(path)
        .then((res) => {
          this.user_info = res.data.user_info
          console.log(this.user_info)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    }
  },
  created () {
    this.view_users()
  }
}
</script>

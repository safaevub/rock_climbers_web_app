<template>
    <div class="container">
        <div class="jumbotron mt-5">
            <div class="col-sm-8 mx-auto">
                <h1 class="text-center">PROFILE</h1>
            </div>
            <table class="table col-md-6 mx-auto">
                <tbody>
                    <tr>
                        <td>First Name</td>
                        <td>{{first_name}}</td>
                    </tr>
                    <tr>
                        <td>Last Name</td>
                        <td>{{last_name}}</td>
                    </tr>
                    <tr>
                        <td>Email</td>
                        <td>{{email}}</td>
                    </tr>
                    <tr>
                        <td>Type of profile logged in </td>
                        <td v-for="(single,index) in accessType" :key="index">
                        {{ single }}
                        </td>
                    </tr>
                    <tr v-for="(single,index) in accessType" :key="index">
                        <td v-if="single=='user'">
                            <router-link class="nav-link" to="/user/license/">My licenses</router-link>
                        </td>
                    </tr>
                    <tr v-for="(single,index) in accessType" :key="index">
                        <td v-if="single=='user'">
                            <router-link class="nav-link" to="/user/entries">My entries</router-link>
                        </td>
                    </tr>
                    <tr v-for="(single,index) in accessType" :key="index">
                        <td v-if="single=='admin'">
                            <router-link class="nav-link" to="/viewusers"> All instructors </router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import jwtDecode from 'jwt-decode'

export default {
  data () {
    const token = localStorage.usertoken
    const decoded = jwtDecode(token)
    return {
      first_name: decoded.identity.first_name,
      last_name: decoded.identity.last_name,
      email: decoded.identity.email,
      id: decoded.identity._id,
      accessType: decoded.identity.accessType
    }
  }
}

</script>

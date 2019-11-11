<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 mt-5 mx-auto">
                <!-- -->
                <h1> License </h1>
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col"> </th>
                      <th scope="col">Active From</th>
                      <th scope="col">Active to</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(license, index) in licenses" :key="index">
                      <td>Lisense {{ index+1}}</td>
                      <td>{{ license.date_from }}</td>
                      <td>{{ license.date_to }}</td>
                    </tr>
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
      licenses: [
        {
          date_from: '',
          date_to: ''
        }
      ],
      first_name: decoded.identity.first_name,
      last_name: decoded.identity.last_name,
      email: decoded.identity.email,
      id: decoded.identity.id

    }
  },
  methods: {
    getLicenses () {
      const token = localStorage.usertoken
      const decoded = jwtDecode(token)
      this.uID = decoded.identity.id
      try {
        if (this.$route.params.id != null) {
          this.uID = this.$route.params.id
        }
      } catch (err) {
        console.log(err)
      }

      const path = `http://localhost:5000/license/${this.uID}`
      axios.get(path)
        .then((res) => {
          this.licenses = res.data.license
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    }
  },
  created () {
    this.getLicenses()
  }
}
</script>

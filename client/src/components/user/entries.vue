<template>
    <div class="container">
    <div class="row">
       <div class="col-md-6 mt-5 mx-auto" >
        <tr v-for="(access, index) in accessType" :key="index">
          <td v-if="access=='user'">
           <button type="button" class="btn btn-success btn-sm">
                   <router-link class="nav-link" to="/user/addRoute">Add route</router-link>
                 </button>
           <button type="button" class="btn btn-success btn-sm">
             <router-link class="nav-link" to="/user/loadRoutes">Load routes from file</router-link>
           </button>
           </td>
           </tr>

     <table class="table table-hover">
     <thead>
       <tr>
         <th scope="col">Location</th>
         <th scope="col">Date</th>
         <th scope="col">Geo</th>
         <th scope="col">Route Name</th>
         <th scope="col">Grade</th>
         <th scope="col">Length</th>
         <th></th>
       </tr>
     </thead>
     <tbody>
       <tr v-for="(entry, index) in entries" :key="index">
         <td>{{ entry.location }}</td>
         <td>{{ entry.date }}</td>
         <td>{{ entry.geo }}</td>
         <td>{{ entry.routeName }}</td>
         <td>{{ entry.grade }}</td>
         <td>{{ entry.length }}</td>
         <td v-for="(access, index) in accessType" :key="index">

           <div class="btn-group" role="group" v-if="access=='user'">
           <button type="button" class="btn btn-success btn-sm" @click="onEditEntry(entry)">
                 Edit</button>
           <button type="button"
                     class="btn btn-danger btn-sm"
                     @click="onDeleteEntry(entry.list_id)">
                     Delete
           </button>
           </div>
         </td>
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
import router from '../../router'

export default {

  data () {
    const token = localStorage.usertoken
    const decoded = jwtDecode(token)
    return {
      entries: [],
      accessType: decoded.identity.accessType,
      uID: decoded.identity.id
    }
  },
  components: {
  },
  methods: {
    getEntries () {
      // const token = localStorage.usertoken
      // const decoded = jwtDecode(token)
      try {
        if (this.$route.params.id != null) {
          this.uID = this.$route.params.id
        }
      } catch (err) {
        console.log(err)
      }
      const path = `http://localhost:5000/getAllEntries/${this.uID}`
      axios.get(path)
        .then((res) => {
          this.entries = res.data.entries
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    onEditEntry (entry) {
      const listID = entry.list_id
      router.push({ name: 'editRoute', params: {id: listID} })
    },
    onDeleteEntry (listID) {
      const token = localStorage.usertoken
      const decoded = jwtDecode(token)
      const uID = decoded.identity.id
      const path = `http://localhost:5000/entries/${uID}/${listID}`
      axios.delete(path)
        .then(() => {
          this.getEntries()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getEntries()
        })
    }
  },
  created () {
    this.getEntries()
  }
}
</script>

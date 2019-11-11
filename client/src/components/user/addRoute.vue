<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 mt-5 mx-auto">
                <!-- -->
                <h1> Add new route </h1>
                <form v-on:submit.prevent="addEntry">
                    <div class="form-group">
                        <label for="routeName">Route name</label>
                        <input type="text" v-model="routeName" class="form-control" name="routeName" placeholder="Enter route">
                    </div>
                    <div class="form-group">
                        <label for="location">Location</label>
                        <input type="text" v-model="location" class="form-control" name="location" placeholder="Enter location">
                    </div>
                    <div class="form-group">
                        <label for="date">Date</label>
                        <input type="date" v-model="date" class="form-control" name="date">
                    </div>
                    <div class="form-group">
                        <label for="geo">GPS-location</label>
                        <input type="text" v-model="geo" class="form-control" name="geo" placeholder="Enter GPS-coordinates">
                    </div>
                    <div class="form-group">
                        <label for="grade">Routes grade</label>
                        <input type="text" v-model="grade" class="form-control" name="grade" placeholder="Enter routes grade">
                    </div>
                    <div class="form-group">
                        <label for="length">Routes length</label>
                        <input type="text" v-model="length" class="form-control" name="length" placeholder="Enter entries length">
                    </div>
                    <button class="btn btn-lg btn-primary btn-block" @click="onSubmit">Add entry</button>
                </form>
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
    return {
      routeName: '',
      location: '',
      date: '',
      geo: '',
      grade: '',
      length: ''
    }
  },
  methods: {
    onSubmit () {
      const payload = {
        location: this.location,
        date: this.date,
        geo: this.geo,
        routeName: this.routeName,
        grade: this.grade,
        length: this.length
      }
      this.addEntry(payload)
    },
    addEntry (payload) {
      const token = localStorage.usertoken
      const decoded = jwtDecode(token)
      const uID = decoded.identity.id
      const path = `http://localhost:5000/addentry/${uID}`
      axios.post(path, payload).then(res => {
        router.push({ name: 'Entries' })
      }).catch(err => {
        console.log(err)
      })
    }
  }

}
</script>

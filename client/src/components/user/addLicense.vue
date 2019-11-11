<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 mt-5 mx-auto">
                <!-- -->
                <h1> Add new license for user: </h1>
                <form v-on:submit.prevent="addLicense">
                    <div class="date_from">
                        <label for="date">Date from</label>
                        <input type="date" v-model="date_from" class="form-control" name="date" placeholder="Enter date">
                    </div>
                    <div class="date_to">
                        <label for="date">Date To</label>
                        <input type="date" v-model="date_to" class="form-control" name="date" placeholder="Enter date">
                    </div>
                    <br><br>
                    <button class="btn btn-lg btn-primary btn-block" @click="onSubmit">Add license</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import router from '../../router'

export default {
  data () {
    return {
      date_from: '',
      date_to: ''
    }
  },
  methods: {
    onSubmit () {
      const payload = {
        date_from: this.date_from,
        date_to: this.date_to
      }
      this.addLicense(payload)
    },
    addLicense (payload) {
      const uID = this.$route.params.id
      const path = `http://localhost:5000/addLicense/${uID}`
      axios.post(path, payload).then(res => {
        router.push({ name: 'ViewUsers' })
      }).catch(err => {
        console.log(err)
      })
    }
  }

}
</script>

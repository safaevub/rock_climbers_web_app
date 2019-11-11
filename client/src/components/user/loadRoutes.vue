<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
      <button v-on:click="submitFile()">Submit</button>
    </div>
  <p>Number of entries in CVS file: {{this.response.totNewEntries}} </p>
  <p>Number of entries added: {{this.response.totEntriesAdded}} </p>
  <p>Number of already existing entries: {{this.response.totDuplicates}} </p>
  <br>
  <br>
  <br>
    <h3 class="mt-4">The format of your CSV-file should be like this:</h3>
    <p>logType,location,date,geo,routeName,grade,length <br>
    climbEntry,'Location 1','yyyy-mm-dd','lat/long','Routename 1',5+,6 <br>
    climbEntry,'Location 2',2002-02-02,20N/20E,'Routename 2',6-,8<br>
    etc..<br><br><br></p>
    <button v-on:click="returnToEntries()">Return to your entries</button>
  </div>

</template>

<script>
import axios from 'axios'
import jwtDecode from 'jwt-decode'
import router from '../../router'

export default {
/* Defines the data used by the component */
  data () {
    const token = localStorage.usertoken
    const decoded = jwtDecode(token)
    return {
      file: '',
      response: {
        totNewEntries: '',
        totEntriesAdded: '',
        totDuplicates: ''
      },
      id: decoded.identity.id
    }
  },

  methods: {
    returnToEntries () {
      router.push({ name: 'Entries' })
    },

    handleFileUpload () {
      this.file = this.$refs.file.files[0]
    },
    submitFile () {
      const path = 'http://localhost:5000/pushEntries/' + this.id
      let formData = new FormData()
      formData.append('file', this.file)
      axios.post(path, formData)
        .then(res => {
          this.response.totNewEntries = res.data.totNewEntries
          this.response.totEntriesAdded = res.data.totEntriesAdded
          this.response.totDuplicates = res.data.totDuplicates
          console.log('SUCCESS!!')
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>

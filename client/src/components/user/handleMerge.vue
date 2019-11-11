<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 mt-5 mx-auto">
                <h1> Merge conflicts </h1>
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col"></th>
                      <th scope="col">Object to load</th>
                      <th scope="col"></th>
                      <th scope="col">Existing object</th>
                      <th scope="col"></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(conflict, index) in mergeConflicts" :key="index">
                      <td>{{ conflict.lId }}</td>
                      <td>
                          {{ conflict.loaObj[1] }}<br />
                          {{ conflict.loaObj[4] }}<br />
                          {{ conflict.loaObj[2] }}<br />
                      </td>
                      <td></td>
                      <td>{{ conflict.uId }}</td>
                      <td>
                          {{ conflict.useObj[1] }}<br />
                          {{ conflict.useObj[4] }}<br />
                          {{ conflict.useObj[2] }}<br />
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

export default {
  data () {
    const token = localStorage.usertoken
    const decoded = jwtDecode(token)
    return {
      mergeConflicts: [
        {
          uploadedObject: '',
          uId: '',
          mergeConflict: '',
          mId: ''
        }
      ],
      first_name: decoded.identity.first_name,
      last_name: decoded.identity.last_name,
      email: decoded.identity.email,
      id: decoded.identity.id

    }
  },
  methods: {
    getmergeConflicts () {
      const path = 'http://localhost:5000/getMergeConflicts/' + this.id
      axios.get(path)
        .then((res) => {
          this.mergeConflicts = res.data.mergeConflicts
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    }
  },
  created () {
    this.getmergeConflicts()
  }
}
</script>

import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Profile from '@/components/Profile'
import entries from '@/components/user/entries'
import license from '@/components/user/license'
import ViewUsers from '@/components/ViewUsers'
import addRoute from '@/components/user/addRoute'
import editRoute from '@/components/user/editRoute'
import handleMerge from '@/components/user/handleMerge'
import loadRoutes from '@/components/user/loadRoutes'
import RegisterAdmin from '@/components/RegisterAdmin'
import addLicense from '@/components/user/addLicense'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/adRegister',
      name: 'RegisterAdmin',
      component: RegisterAdmin
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile
    },
    {
      path: '/viewusers',
      name: 'ViewUsers',
      component: ViewUsers
    },
    {
      path: '/user/license',
      name: 'License',
      component: license
    },
    {
      path: '/user/license/:id',
      name: 'License',
      component: license
    },
    {
      path: '/user/entries',
      name: 'Entries',
      component: entries
    },
    {
      path: '/user/entries/:id',
      name: 'Entries',
      component: entries
    },
    {
      path: '/user/addroute',
      name: 'addRoute',
      component: addRoute
    },
    {
      path: '/user/editroute/:id',
      name: 'editRoute',
      component: editRoute
    },
    {
      path: '/user/handleMerge',
      name: 'handleMerge',
      component: handleMerge
    },
    {
      path: '/user/loadRoutes',
      name: 'loadRoutes',
      component: loadRoutes
    },
    {
      path: '/user/addLicense/:id',
      name: 'addLicense',
      component: addLicense
    }

  ]
})

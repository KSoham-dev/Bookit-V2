import { createRouter, createWebHistory } from 'vue-router'
import userLogin from '@/views/UserViews/userLogin.vue'
import libLogin from '@/views/LibrarianViews/libLogin.vue'
import userSignup from '@/views/UserViews/userSignup.vue'
import home from '@/views/MiscViews/home.vue'
import book_info from '@/views/MiscViews/book_info.vue'
import userProfile from '@/views/UserViews/userProfile.vue'
import userBooks from '@/views/UserViews/userBooks.vue'
import readBook from '@/views/MiscViews/readBook.vue'
import checkExpiry from '@/myModules/checkExpiry'
import books_requested from '@/views/UserViews/userBooksreq.vue'
import Cart from '@/views/UserViews/user_cart.vue'
import libProfile from '@/views/LibrarianViews/libProfile.vue'
import libAllReqBooks from '@/views/LibrarianViews/libAllReqBooks.vue'
import allBooks from '@/views/LibrarianViews/libAllBooks.vue'
import allSections from '@/views/LibrarianViews/libAllSec.vue'
import allIssuedBooks from '@/views/LibrarianViews/libAllIssuedBooks.vue'
import libStats from '@/views/LibrarianViews/libStats.vue'
import allAuthors from '@/views/LibrarianViews/libAllAuthors.vue'
import libReports from '@/views/LibrarianViews/libReports.vue'

const routes = [
    {
        path: '/user',
        name: 'user',
        children: [
            {
                path: 'login',
                name: 'userLogin',
                component: userLogin
            },
            {
                path: 'signup',
                name: 'userSignup',
                component: userSignup
            },
            {
                path: 'profile',
                name: 'userProfile',
                component: userProfile
            },
            {
                path: 'books',
                name: 'userBooks',
                component: userBooks
            },
            {
                path: 'books_req',
                name: 'userBooksReq',
                component: books_requested
            },
            {
                path: 'cart',
                name: 'userCart',
                component: Cart
            },
            {
                path: 'home',
                name: 'userHome',
                component: home
            }
        ]
    },
    {
        path: '/lib',
        name: 'lib',
        children: [
            {
                path: 'home',
                name: 'libHome',
                component: home
            },
            {
                path: 'login',
                name: 'libLogin',
                component: libLogin
            },
            {
                path: 'profile',
                name: 'libProfile',
                component: libProfile
            },
            {
                path: 'book_requests',
                name: 'allReqBooks',
                component: libAllReqBooks
            },
            {
                path: 'all_books',
                name: 'allBooks',
                component: allBooks
            },
            {
                path: 'all_sections',
                name: 'allSections',
                component: allSections
            },
            {
                path: 'books_issued',
                name: 'allIssuedBooks',
                component: allIssuedBooks
            },
            {
                path: 'stats',
                name: 'libStats',
                component: libStats
            },
            {
                path: 'all_authors',
                name: 'allAuthors',
                component: allAuthors
            },
            {
                path: 'reports',
                name: 'libReports',
                component: libReports
            }
        ]
    },
    
    {
        path: '/read/:book_id',
        name: 'readBook',
        component: readBook
    },
    {
        path: '/book_info/:j',
        name: 'bookInfo',
        component: book_info
    },
    {
        path: '/',
        name: 'home',
        component: userLogin
    }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
router.beforeEach((to, from, next) => {
  if (to.path == '/' || to.path == '/lib/login' || to.path == '/user/signup') {
      next();
  }else{
        fetch('http://127.0.0.1:5000/auth/refresh_access',{
          method: 'GET',
          headers: {
              Authorization: `Bearer ${localStorage.getItem('ref_token')}`
          }
        })
        .then(resp => {
            if (!resp.ok){
                throw new Error(resp.statusText + " " + resp.status)
            }
            return resp.json()
        })
        .then(data => {
            localStorage.setItem('ac_token', data.ac_token);
        })
        .catch()
        checkExpiry();
        next();
  }
})




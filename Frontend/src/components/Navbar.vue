<template>
    <nav class="navbar">
        <img class="imglogo logohome" src="@/assets/Bookitwh.webp" height="100px" width="100px" alt="logo"/>
        
        <form autocomplete="off" class="d-flex search" role="search" @submit.prevent="search">
            <input class="inp1" type="search" name="search" placeholder="&#x1F50E;&#xFE0E; Type and press enter to search">
        </form>

        <div class="linklist">
            <ul><template v-if ="usr_role == 'user'">
                    <li class="navbar_links">   <router-link to="/user/home"> <img src="@/assets/home-5-line.webp" alt="home icon"/> </router-link></li>
                </template>
                <template v-if ="usr_role == 'librarian'">
                    <li class="navbar_links">   <router-link to="/lib/home"> <img src="@/assets/home-5-line.webp" alt="home icon"/> </router-link></li>
                </template>
                <template v-if ="usr_role == 'user'">
                    <li class="navbar_links">  <router-link to="/user/profile" class="navicons"> <img src="@/assets/user-line.webp" alt="user icon"/> Hello, {{ f_name }} </router-link> </li>
                </template>
                <template v-if ="usr_role == 'librarian'">
                    <li class="navbar_links">  <router-link to="/lib/profile" class="navicons"> <img src="@/assets/user-line.webp" alt="user icon"/> Hello, {{ f_name }}</router-link> </li>
                </template>
                <template v-if ="usr_role == 'user'">
                    <li class="navbar_links">   <router-link to="/user/cart" class="navicons"> <img src="@/assets/shopping-cart-line.webp" alt="shopping cart"/> </router-link></li>
                </template>
                    <li class="navbar_links"><button href="/logout" class="navicons" style="background-color: transparent; border: none;" @click="logout"><img src="@/assets/logout.webp" alt="shopping cart"/> </button></li>
            </ul>
        </div> 
    </nav>
    <template v-if="result.results && Object.keys(result.results).length > 0 && resultFlag">
        <div class="resultdiv">
            <button type="button" :class="{ close1: result.results.object === 'book', close2: result.results.object === 'section', close3: result.results.object === 'author'}"><img src="@/assets/cross.svg" @click="resultFlag = false"></button>
            <searchResults :result="result" :resultFlag="resultFlag"></searchResults>
        </div>
    </template>
    <template v-else-if="!Object.keys(result.results).length > 0 && resultFlag">
        {{ NoResult() }}
    </template>
</template>

<style scoped>
    a{
        text-decoration: none;
        color: rgb(255,255,255);
    }
    .navbar{
      height: 120px;
      background-color: rgb(35, 35, 35);
    }
    .navbar_links{
    display: inline-block;
    padding: 0 20px;
    color: rgb(255,255,255);
    text-decoration: none;
    }
    .linklist {
        position: absolute;
        bottom: 30px;
        left: 950px;
        gap: 5px;
    }
    .search{
    position: absolute;
    bottom: 45px;
    left: 350px;
    }
    .inp1{
      width: 500px;
      background: transparent;
      border: none;
      border-bottom: 2px solid rgb(255,255,255);
      color: rgb(255, 255, 255);
    }
    .inp1::placeholder {
      color: rgb(255,255,255);
      opacity: 1;
    }
    .navicons{
      color: rgb(255,255,255);
    }
    .imglogo{
        position: absolute;
        left: 13px;
    }
    .router-link-active{
        border-bottom: 2px solid rgb(255,255,255);
        padding: 10px;
    }
    .resultdiv{
        position: relative;
        top: 30px;
        left: 200px;
        background: #f5f5f5;
        padding: 60px;
        width: 1100px;
        height: auto;
        border: 1px solid black;
        box-shadow: 5px 5px 10px 1px rgba(0,0,0,0.3);
        border-radius: 10px;
    }
    .close1, .close2, .close3{
        border: none; 
        background: transparent; 
        position: absolute;
    }
    .close1{
    bottom: 390px;
    left: 1060px;
    }
    .close2, .close3{
    bottom: 570px;
    left: 1050px;
    }
</style>

<script>
import swal from 'sweetalert'
import searchResults from "@/components/searchResults.vue"
export default {
    name: "Navbar",
    data(){
            return{
        f_name: "",
        l_name: "",
        usr_id: "",
        usr_role: "",
        result: {
        results: {}
        },
        resultFlag: false
        }
    }, 
    mounted(){
        fetch("http://127.0.0.1:5000/auth/myinfo",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
            }
        }).then(res => res.json())
        .then(data => {
            this.f_name = data.user_details.f_name;
            this.l_name = data.user_details.l_name;
            this.usr_id = data.user_details.usr_id;
            this.usr_role = data.user_details.role;
            (this.usr_role)
    })
    .catch(err => console.log(err))
    },
    methods: {
        logout() {
            swal({
                title: "Logout",
                text: "Are you sure ?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((willLogout) => {
                if (willLogout) {
                    fetch('http://127.0.0.1:5000/auth/logout',{
                        method: 'GET',
                        headers: { 
                            'Authorization': `Bearer ${localStorage.getItem('ac_token')}`,
                        }
                    })
                    .then(res => {
                        localStorage.removeItem('ac_token')
                        fetch('http://127.0.0.1:5000/auth/logout',{
                        method: 'GET',
                        headers: { 
                            'Authorization': `Bearer ${localStorage.getItem('ref_token')}`,
                        }
                    })
                    .then(res1 => {
                        localStorage.removeItem('ref_token')
                        this.$router.push({path: '/'})
                        return res1.json()
                    })
                    .catch(
                        function(error) {
                            swal("Error fecthing data!", "It's us don't worry, we're on it", "error");
                            console.log(error)
                        }
                    )
                    return res.json()
                    })
                    .then(data => {
                        swal("Logged out!", "See you soon!", "success");
                    })
                    .catch(
                        function(error) {
                            swal("Error fecthing data!", "It's us don't worry, we're on it", "error");
                            console.log(error)
                        }
                    )     
                }
            });
        },
        search(ev){
            this.resultFlag = true
            fetch("http://127.0.0.1:5000/user/search",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                },
                body: JSON.stringify({
                    "item": ev.target.elements.search.value
                })
            }).then(res => res.json())
            .then(data => {
                this.result = data
            }).catch(err => console.log(err))
        },
        NoResult(){
            swal("No results found", "Please try again", "info");
        }
    },
    components: {
        searchResults
    }
}
</script>
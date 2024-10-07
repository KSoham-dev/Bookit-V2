<template>
<Navbar></Navbar>
<div class="bgup">
    <div class="row mainrowup">
        <div class="col-5 leftcolup">
            <Usermenu></Usermenu>    
        </div>
            
        <div class="col rightcolup bookstable">
                    <header class="display-4"> My Books </header><br /><br /><br />
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col"> Index </th>
                                <th scope="col"> Book Name </th>
                                <th scope="col"> Authors </th>
                                <th scope="col"> Days Passed </th>
                                <th scope="col"> Actions* </th>
                            </tr>
                        </thead>
                        <template v-for="(i,j) in user_books" >
                            <tbody>
                            <tr>
                                <td>{{ j }}</td>
                                <td>{{ i.book_name }}</td>
                                <td>{{Object.values(i.authors).join(',')}}</td>
                                <td>{{ i.days_passed }}</td>
                                <td>
                                <template v-if="i.days_passed < 7"> 
                                    <router-link :to="`/read/${i.book_id}`" class="action-btn btn btn-outline-primary btn-sm"> Read Book</router-link>
                                </template>
                                <template v-else>
                                    <button class="action-btn btn btn-outline-primary btn-sm" disabled> Disabled </button>
                                </template>
                                    <button class="action-btn btn btn-outline-primary btn-sm" @click="returnBook(i.book_id)"> Return Book</button></td>
                        </tr>
                            </tbody>
                        </template>
                    </table>
                    <router-link class="btn btn-outline-primary btn-sm" to="/user/home" style="margin-top: 70px;"> Browse More Books </router-link>
                    <div class="msgpassed">
                        * You can have books 7 days only, After that <i>Read Book</i> is disabled
                    </div>
                </div>
    </div>
</div>
<Footer></Footer>
</template>

<style scoped>
    *{
    overflow: hidden;   
    }
    .mainrowup{
        min-height: 100vh;
        }
    
    .leftcolup{
        background-image: url("@/assets/userbg.webp");
        background-size: cover;
        margin: 20px;
        margin-left: 30px;
        border-radius: 12px;
    }
    .updtfrm,.updtable{
      margin-top: 150px;
      text-align: center;
    }     
    .bookstable{
      text-align: center;
      margin-top: 75px;
     }

    .action-btn{
        margin: 5px;
    }
    .msgpassed{
        margin-top: 84px;
    }
</style>

<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import Usermenu from '@/components/Usermenu.vue'
import swal from 'sweetalert'
export default {
    name: "userBook",
    mounted() {
        fetch("http://127.0.0.1:5000/user/books",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
            }
        }).then(res => res.json())
        .then(data => {
            this.user_books = data
        })
        .catch(err => console.log(err))
        
    },
    components: {
        Navbar,
        Footer,
        Usermenu
    },
    data(){
        return{
            user_books: {},
        }
    },
    methods: {
        returnBook(book_id){
            swal({
                title: "Return the book?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            }).then((willDelete) => {
                if (willDelete) {
                    fetch(`http://127.0.0.1:5000/user/return_book`,{
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                        },
                        body: JSON.stringify({'book_id': book_id})
                    }).then(res => res.json())
                      .catch(err => console.log(err))
                }
                swal({
                    title: "Sucess",
                    text: "Book Returned",
                    icon: "success",
                    button: "OK",
                }).then(() => {
                    window.location.reload()
                })
                    
            })
            
        }
    }
}
</script>
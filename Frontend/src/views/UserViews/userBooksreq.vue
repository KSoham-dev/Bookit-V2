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
                                    <th scope="col"> Actions </th>
                                </tr>
                            </thead>
                            <template v-for="(i,j) in user_books" >
                                <tbody>
                                <tr>
                                    <td>{{ j }}</td>
                                    <td>{{ i.book_name }}</td>
                                    <td>{{Object.values(i.authors).join(', ')}}</td>
                                    <td>
                                        <button class="action-btn btn btn-outline-primary btn-sm" @click="cancelRequest(i.book_id)">Cancel Request</button>
                                    </td>
                            </tr>
                                </tbody>
                            </template>
                        </table>
                        <router-link class="btn btn-outline-primary btn-sm" to="/user/home" style="margin-top: 70px;"> Browse More Books </router-link>
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
    </style>
    
    <script>
    import Navbar from '@/components/Navbar.vue'
    import Footer from '@/components/Footer.vue'
    import Usermenu from '@/components/Usermenu.vue'
    import swal from 'sweetalert'
    export default {
        name: "userBook",
        mounted() {
            fetch("https://bookit-v2-s4t8.onrender.com/user/view_req_books",{
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
            cancelRequest(book_id){
                swal({
                    title: "Cancel the request?",
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                }).then((willDelete) => {
                    if (willDelete) {
                        fetch(`https://bookit-v2-s4t8.onrender.com/user/cancel_book_req`,{
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                            },
                            body: JSON.stringify({book_id: book_id})
                        }).then(res => res.json())
                        .then(data => {
                        }).catch(err => console.log(err))
                        swal({
                        title: "Sucess",
                        text: "Book Request Cancelled",
                        icon: "success",
                        button: "OK",
                    }).then(() => {
                        window.location.reload()
                    })
                    }  
                })
                
            }
        }
    }
    </script>
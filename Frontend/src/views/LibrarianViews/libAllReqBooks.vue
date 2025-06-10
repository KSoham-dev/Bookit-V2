<template>
    <Navbar></Navbar>
    <div class="bgup">
        <div class="row mainrowup">
            <div class="col-5 leftcolup">
                <Libmenu></Libmenu>
            </div>
                <div class="col rightcolup">
                    <header class="display-4">Book Requests</header><br /><br /><br />
                    <table class="table">
                        <thead>
                            <th scope="col">User Id</th>
                            <th scope="col">Book Requested</th>
                            <th scope="col">Action</th>
                        </thead>
                        <tbody>
                            <template v-for="(i, j) in books_req">
                                
                                <template v-for="(k, l) in i.Books">
                                    <tr>
                                        <td>{{ i.usr_id }}</td>
                                        <td>{{ k.book_name }}</td>
                                        <td><button class="btn btn-outline-primary btn-sm m-2" @click="acceptReq(i.usr_id,k.book_id)">Approve</button>
                                            <button class="btn btn-outline-primary btn-sm" @click="rejectReq(i.usr_id,k.book_id)">Reject</button>
                                        
                                        </td>
                                    </tr>
                                </template>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>
    </div>
    <Footer></Footer>
</template>

<style scoped>
*{
 overflow: hidden;   
}
.leftcolup{
      background-image: url("@/assets/libbg.webp");
      background-size: cover;
      margin: 20px;
      margin-left: 30px;
      border-radius: 12px;
    }
.table{
    margin-left: 40px;
}
.mainrowup{
    min-height: 100vh;
}
.lefttextup{
    padding: 110px;
}

.usrmenu{
    margin-left: 80px;
    margin-top: 40px;
}
    .rightcolup{
    text-align: center;
    margin-top: 75px;
    }
.router-link-active{
border-bottom: 2px solid rgb(0,0,0);
padding-bottom: 10px;
}
</style>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import swal from 'sweetalert';
import Libmenu from '@/components/Libmenu.vue';
export default {
    name: "LibAllReqBooks",
    mounted(){
        fetch("https://bookit-v2-s4t8.onrender.com/lib/get_all_req_books", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("ac_token"),
                "Content-Type": "application/json"
            },
            method: "GET"
        }).then(res => res.json())
        .then(data => this.books_req = data)
    },
    components: {
        Navbar,
        Footer,
        Libmenu
    },
    data(){
        return{
            books_req: {},
            index: 0
        }
    }, 
    computed:{
    },
    methods: {
        acceptReq(usr_id,book_id){
            fetch("https://bookit-v2-s4t8.onrender.com/lib/approve_request", {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("ac_token"),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "book_id": book_id,
                    "usr_id": usr_id
                })
            }).then(res => res.json())
            .then(data => {
                if(data.message == "Book request approved"){
                    swal({
                        title: "Done",
                        text: data.message,
                        icon: "success",
                        button: "OK",
                    }).then(() => {window.location.reload()})
                }
                
            })
        },
        rejectReq(usr_id,book_id){
            fetch("https://bookit-v2-s4t8.onrender.com/lib/reject_request", {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("ac_token"),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "book_id": book_id,
                    "usr_id": usr_id
                })
            }).then(res => res.json())
            .then(data => {
                if(data.message == "Book request rejected"){
                    swal({
                        title: "Done",
                        text: data.message,
                        icon: "success",
                        button: "OK",
                    }).then(() => {window.location.reload()})
                }
                
            })
        }   
    }
}
</script>
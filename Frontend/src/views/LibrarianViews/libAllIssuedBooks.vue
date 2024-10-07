<template>
    <Navbar></Navbar>
    <div class="bgup">
        <div class="row mainrowup">
            <div class="col-5 leftcolup">
                <Libmenu></Libmenu>
            </div>
                <div class="col rightcolup">
                    <header class="display-4">Books Issued</header><br /><br /><br />
                    <table class="table">
                        <thead>
                            <th scope="col">User Id</th>
                            <th scope="col">Book Name</th>
                            <th scope="col">Days Issued</th>
                            <th scope="col">Action</th>
                        </thead>
                        <tbody>
                            <template v-for="(i, j) in books_issued">
                                <tr>
                                    <td>{{ i.usr_id }}</td>
                                    <td>{{ i.book.book_name }}</td>
                                    <td>{{ i.days_issued }}</td>
                                    <td><button class="btn btn-outline-primary btn-sm" @click="revokeAccess(i.usr_id,i.book.book_id)"> Revoke </button></td>
                                </tr>
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
    name: "allIssuedBooks",
    mounted(){
        fetch('http://127.0.0.1:5000/lib/get_all_issued_books', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('ac_token')
            },
        }).then(res => res.json())
        .then(data => {
            this.books_issued = data
        }).catch(err => {
            console.log(err)
        })
    },
    components: {
        Navbar,
        Footer,
        Libmenu
    },
    data(){
        return{
            books_issued: {}
        }
    }, 
    computed:{
    },
    methods: {
        revokeAccess(usr_id,book_id){
            swal({
                title: "Are you sure?",
                text: "Do you really want to revoke access from the user to this book?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            }).then((willRevoke) => {
                if (willRevoke) {
                    fetch('http://127.0.0.1:5000/lib/revoke_issued_book', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + localStorage.getItem('ac_token')
                    },
                    body: JSON.stringify({
                        "usr_id": usr_id,
                        "book_id": book_id
                    })
                    }).then(res =>{
                    if(res.status == 200){
                        swal("Success", "Book revoked successfully", "success").then(() => {
                            window.location.reload();
                        })
                    }
                    })
                    .catch(err => {
                        console.log(err)
                    })
                }
            });
        }
    }   
}
</script>
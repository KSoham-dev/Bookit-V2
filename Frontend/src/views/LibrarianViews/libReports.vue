<template>
    <Navbar></Navbar>
    <div class="bgup">
        <div class="row mainrowup">
            <div class="col-5 leftcolup">
                <Libmenu></Libmenu>
            </div>
                <div class="col rightcolup updtfrm text-center mt-5">
                    <header class="display-4 mb-3"> Generate Reports </header>
                    <div class="msg">
                        Welcome, you can generate reports here
                    </div>
                    <table class="table">
                        <thead>
                            <th>Index</th>
                            <th scope="col">Report Name</th>
                            <th scope="col">Action</th>
                        </thead>
                        <tbody>
                            <tr>
                                <th> 1 </th>
                                <td>Issued Books Report (.csv)</td>
                                <td><button class="btn btn-outline-primary btn-sm" @click="issuedReport()">Generate</button></td>
                            </tr>
                            <tr>
                                <th> 2 </th>
                                <td>Requested Books Report (.csv)</td>
                                <td><button class="btn btn-outline-primary btn-sm" @click="reqReport()">Generate</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
        </div>
    </div>
    <Footer></Footer>
</template>

<style scoped>
.leftcolup{
      background-image: url("@/assets/libbg.webp");
      background-size: cover;
      margin: 20px;
      margin-left: 30px;
      border-radius: 12px;
    }
.msg{
    font-size: 20px;
    margin-bottom: 50px;
    font-style: oblique;
}
.btn{
    margin-bottom: 20px;
}
.table{
    width: 70%;
    margin-left: 140px;
    position: relative;
    top: 50px;
}
</style>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import swal from 'sweetalert';
import Libmenu from '@/components/Libmenu.vue';
export default {
    name: "libReports",
    mounted(){
    },
    components: {
        Navbar,
        Footer,
        Libmenu
    },
    data(){
        return{
        }
    }, 
    methods:{
        issuedReport(){
            fetch("http://127.0.0.1:5000/lib/issued_books_csv",{
                method: "GET",
                headers: {
                    "Content-type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                }
            }).then(res => res.json())
            .then(data => {
                if(data.msg == "Successful"){
                    swal("Success", "Reports will be delivered shortly to your mailbox", "success");
                }
                else{
                    swal("Error", "Something went wrong", "error");
                }
            })
        },
        reqReport(){
            fetch("http://127.0.0.1:5000/lib/requested_books_csv",{
                method: "GET",
                headers: {
                    "Content-type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                }
            }).then(res => res.json())
            .then(data => {
                if(data.msg == "Successful"){
                    swal("Success", "Reports will be delivered shortly to your mailbox", "success");
                }
                else{
                    swal("Error", "Something went wrong", "error");
                }
            })
        }
    }   
}
</script>
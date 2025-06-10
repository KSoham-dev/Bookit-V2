<template>
    <Navbar></Navbar>
    <div class="bgup">
        <div class="row mainrowup">
            <div class="col-5 leftcolup">
                <Libmenu></Libmenu>    
            </div> 
            <template v-if="flag & !updtflag">
                <div class="col rightcolup addfrm">
                    <button class="closebtn"><img src="@/assets/cross.svg" alt="Close Button" @click="flag=false"/></button>
                    <Addbkfrm :Books="books" :flag="flag"></Addbkfrm>
                </div>
            </template>
            <template v-if="!flag & updtflag">
                <div class="col rightcolup addfrm">
                    <button class="closebtn"><img src="@/assets/cross.svg" alt="Close Button" @click="updtflag=false"/></button>
                    <Updtbkfrm :Books="books" :flag="updtflag" :bk_id="bk_id"></Updtbkfrm>
                </div>
            </template>
            <template v-if="!flag & !updtflag">
                <div class="col rightcolup bookstable">
                    <header class="display-4">All Books </header><br /><br /><br />
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col"> Index </th>
                                <th scope="col"> Book Name </th>
                                <th scope="col"> Authors </th>
                                <th scope="col"> Section </th>
                                <th scope="col"> Actions </th>
                            </tr>
                        </thead>
                        <template v-for="(i,j) in books" >
                            <template v-if="i.book_section">
                                <tbody>
                                <tr>
                                    <td>{{ j }}</td>
                                    <td>{{ i.book_name }}</td>
                                    <td>{{ i.book_authors.author_names.join(", ")}}</td>
                                    <td>{{ i.book_section.section_name }}</td>
                                    <td>
                                        <button class="action-btn btn btn-outline-primary btn-sm m-2" @click="deleteBook(i.book_id)"> Remove </button>
                                        <button class="action-btn btn btn-outline-primary btn-sm" @click="updtflag=true, bk_id=i.book_id"> Update </button>
                                    </td>
                                </tr>
                                </tbody>
                            </template>
                        </template>
                    </table> 
                    <div class="addbk m-5">
                        <button class="addbkbtn btn btn-outline-primary btn-lg" @click="flag=true"> Add a Book </button>
                    </div>
                </div>
            </template>
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
        margin-bottom: 200px;
    }
    .usriconup{
      border: 8px solid black;
      position: relative;
      left: 90px;
      margin-bottom: 30px;
      border-radius: 50%;
      width: 174px;
      height: 174px;
      padding: 15px;
     }
    .lefttextup{
      padding: 110px;
    }
    .bookstable{
      text-align: center;
      margin-top: 75px;
     }
    .router-link-active{
    border-bottom: 2px solid rgb(0,0,0);
    padding-bottom: 10px;
    }
    .addfrm{
        text-align: center;
        margin-top: 80px;
        margin-bottom: 100px;
    }
    /* .addfrm{
        background-color: wheat;
        height: 50%;
        margin-top: 75px;
        border-radius: 12px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    } */
    .closebtn {
    position: relative;
    left:300px;
    top: 30px;
    border: none;
    background: transparent;
    }
</style>
    
<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import Libmenu from '@/components/Libmenu.vue'
import Addbkfrm from '@/components/Addbkfrm.vue'
import Updtbkfrm from '@/components/Updtbkfrm.vue'
import swal from 'sweetalert'
export default {
    name: "allBooks",
    mounted() {
        fetch("https://bookit-v2-s4t8.onrender.com/books",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
            }
        }).then(res => res.json())
        .then(data => {
            this.books = data
        })
        .catch(err => console.log(err))
        
    },
    components: {
        Navbar,
        Footer,
        Libmenu,
        Addbkfrm,
        Updtbkfrm
    },
    data(){
        return{
            books: {},
            flag: false,
            updtflag: false,
            bk_id: 0
        }
    },
    computed: {
    },
    methods: {
        deleteBook(id){
            swal({
                title: "Are you sure?",
                text: "Do you want to really delete this book?",
                icon: "warning",
                buttons: true,
                dangerMode: true
            }).then((willDelete) => {
                if(willDelete){
                    
                    fetch("https://bookit-v2-s4t8.onrender.com/books/delete_book",{
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                    },
                    body: JSON.stringify({
                        "book_id": id
                    })
                    }).then(res => res.json())
                    .then(data => {
                        if(data.message == "Book deleted successfully"){
                            swal({
                                title: "Done",
                                text: "Book deleted successfully",
                                icon: "success",
                                button: "OK",
                            }).then(() => {
                                location.reload()
                            })
                        }
                    })
                }
            })
        }
    }
}
</script>
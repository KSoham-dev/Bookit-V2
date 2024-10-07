<template>
<Navbar></Navbar>
<div class="container">

    <div class="row">
        <div class="col-5 bookimgcol">
            <img src="@/assets/singlebook.webp" height="350px" width="350px" class="bookimg">
            <div class="container booklinkmenu">
                <div class="row">
                    <div class="col">
                        <template v-if= "usr_role != 'user'" >
                            <button class="btn btn-outline-primary btn-block actlinks" disabled> Add to Cart </button>
                        </template>
                        <template v-else>
                            <button class="btn btn-outline-primary btn-block actlinks" @click="addItemToCart"> Add to Cart </button>
                        </template>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <template v-if="books_issued.includes(book_id) || books_req.includes(book_id) || usr_role != 'user'">
                            <button class="btn btn-outline-primary  actlinks" disabled> Request this book </button>
                        </template>
                        <template v-else>
                            <button class="btn btn-outline-primary  actlinks" @click="requestBook"> Request Book </button>
                        </template>
                    </div>
                </div>

                <div class="row">
                    <div class="col">
                        <template v-if='usr_role != "user"' >
                            <button class="btn btn-outline-primary actlinks" disabled> Buy PDF for {{book.book_price}} </button>
                        </template>
                        <template v-else>
                            <a :href="get_url_for_download" :download="this.book.book_name"> <button class="btn btn-outline-primary actlinks" @click="BuyBook"> Buy PDF for {{book.book_price}} </button> </a>
                        </template>
                    </div>
                </div>
            </div>
        </div>

        <div class="col aboutbook text-align-left">
            <h1 class="display-3 bookname">{{book.book_name}}</h1>
            <template v-if="book.book_section">
            <span class="authorname">
                By {{ joinedAuthorNames }} | Section: {{ book.book_section.section_name }}
            </span>
            </template>
            <div class="book_desc">
                    {{book.book_description}}
            </div>

            <div class="author_desc">
                <template v-if="(book.book_authors)">
                    <template v-if="(Object.values(book.book_authors)).length > 1">
                        <h1 class="display-5"> About Authors </h1><br/>
                    </template>
                    <template v-else>
                        <h1 class="display-5"> About Author </h1><br/>
                    </template>
                </template>
                <div class="container mt-5">
                    <div class="row">
                        <template v-for="(i,j) in book.book_authors">
                            <div class="col">
                                <h1 class="display-6" style="font-size: 30px;">{{i.author_name}}</h1><br/>
                                {{i.author_description}}<br/><br>
                            </div>
                        </template>
                    </div>
                </div>
            </div>
        </div>


        <div class="container feedback">
            <div class="row feedback">
                <h1 class="display-5"> Feedbacks</h1>
                    <template v-if="book.book_feedbacks">
                        <template v-for="(i,j) in book.book_feedbacks">
                            <div class="col infeed" style="margin-top: 50px">
                                <h1 class="display-6" style="font-size: 30px;"> {{i[0]}}</h1>
                                {{i[1]}}
                            </div>
                        </template>
                    </template>
                    <template v-else>
                        <div class="col infeed" style="margin: 50px">
                            <span style="font-size: 26px;"> No Feedbacks Yet</span> 
                        </div>
                    </template> 
            </div>
            <div class="row addfeed">
                <div class="col"></div>
                <div class="col"></div>
                    <template v-if="fdbUserIdList.includes(usr_id)">
                        <div class="col">
                            <button class="btn btn-outline-primary"  disabled> Add Feedback </button>
                        </div>
                        <div class="col">
                            <button class="btn btn-outline-primary" @click="RemoveFeedback"> Remove Feedback </button>
                        </div>
                    </template>
                    <template v-else>
                        <div class="col">
                            <template v-if="!this.formflag">
                                <button class="btn btn-outline-primary" @click="formflag = true"> Add Feedback </button>
                            </template>
                            <template v-if="this.formflag">
                                <div class="formdiv">
                                    <form @submit.prevent="SendFeedback" class="fdbform">
                                        <button type="button" class="close"><img src="@/assets/cross.svg" @click="formflag = false"></button>
                                        <span style="position: relative; right: 21px; font-weight: bold;">Feedback:</span> <input class="form-control" type="text" name="fdb" placeholder="Enter your feedback">
                                        <input class="btn btn-outline-primary" type="submit" value="Submit Feedback">
                                    </form>
                                </div>
                            </template>
                        </div>
                        <div class="col"></div>
                    </template>
                <div class="col"></div>
                <div class="col"></div>
            </div>
        </div>
        {{ fetch_section_books }}
        <div class="container seemore">
            <template v-if="book.book_section">
                <strong>More Books in {{book.book_section.section_name}} </strong>
            </template>
            <div class="row">
                <template v-for="(i,j) in section_books">
                    <div class="col colimghomevb">
                        <button @click="RedirectToBook(j)" class="book_link" style="border:none; background:transparent">
                            <div class="divincolvb">
                                <img src="@/assets/singlebook.webp" height="210px">
                                <div class="imglabel mt-4">
                                    {{i}}
                                </div>
                            </div>
                        </button>
                    </div>
                </template>
            </div>
        </div>
    </div>
</div>

<Footer></Footer>
</template>

<style scoped>
.bookimgcol{
    height: 100vh;
    margin-top:50px;
    }
    .aboutbook{
    height: 100vh;
    margin-top:50px;
    }
    
    .actlinks{
    margin-bottom: 40px;
    width: 250px;
    }
    .booklinkmenu{
    text-align: center;
    position: relative;
    top: 150px;
    right: 90px;
    }
    
    .book_desc{
    height: 450px;
    width:  450px;
    position: relative;
    top:200px;
    left:25px;
    text-align: center;
    }
    .divincolvb{
    width: 210px;
    text-align: center;
    margin:20px;
    }
    .colimghomevb{
    margin: 40px 10px 0 20px; 
    vertical-align:bottom;
    }
    .feedback{
    margin-top: 50px;
    }
    .author_desc{
        position: relative;
        bottom: 40px;
    }
    .infeed{
    margin-top: 20px;
    margin-left: 20px;
    }
    .addfeed{
        margin-top: 60px;
        margin-bottom: 90px;
    }
    .book_link{
        text-decoration: none;
        color: black;
        font-weight: bold;
    }
    .seemore{
        margin-bottom: 60px;
    }
    .formdiv{
        position: relative;
        bottom: 160px;
        left: 160px;
        background: #f5f5f5;
        padding: 60px;
        width: 500px;
        height: 300px;
        border: 1px solid black;
        box-shadow: 5px 5px 10px 1px rgba(0,0,0,0.3);
        border-radius: 10px;
    }
    .formdiv .form-control{
        margin: 10px;
        border-radius: 0;
        border: none;
        background: none;
        border-bottom: 1px solid black;
    }
    .formdiv .btn{
        margin-top: 30px;
        margin-left: 90px;
    }
    .close{
        border: none; 
        background: none; 
        position: relative;
        bottom:55px; 
        left:400px;
    }
    
</style>

<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'

export default {
    name: "book_info",
    mounted(){
        this.book_id = parseInt(this.$route.params.j,10)
        fetch("http://127.0.0.1:5000/auth/myinfo",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
            }
        }).then(res => res.json())
        .then(data => {
            this.usr_role = data.user_details.role;
            this.usr_id = data.user_details.usr_id
    })
    .catch(err => console.log(err))
    fetch("http://127.0.0.1:5000/user/user_book_info",{
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
            "Content-Type": "application/json"
        },
        method: "GET"
    }).then(res => res.json())
    .then(data => {
        this.books_issued = data.owned_books
        this.books_req = data.requested_books
    })
    .catch(err => console.log(err))
    fetch(`http://127.0.0.1:5000/books/book`,{
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({"book_id": this.book_id})
    }).then(res => res.json())
    .then(data => {
        this.book = data
    })
    .catch(err => console.log(err))
    
    },
    components: {
        Navbar,
        Footer
    },
    data(){
        return{
            book_id: 0,
            usr_role: "",
            books_issued: [],
            books_req:[],
            book: {},
            usr_id: 0,
            section_books: [],
            section_books_ids: [],
            formflag: false
        }
    },
    computed: {
        joinedAuthorNames() {
            let l = []
            for ( let author of Object.values(this.book.book_authors)) {
                    l.push(author.author_name)
            }
            return l.join(", ")
        },
        fdbUserIdList() {
            let l = []
                if (this.book.book_feedbacks) {
                    for (let i of this.book.book_feedbacks){
                        l.push(i[2])
                    }
                }
                return l
            },
            fetch_section_books(){
            if(this.book.book_section){
                fetch(`http://127.0.0.1:5000/sections/section`,{
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                    "Content-Type": "application/json"
                },
                method: "POST",
                body: JSON.stringify({"section_id": this.book.book_section.section_id})
                }).then(res => res.json())
                .then(data => {
                    let l = Object.values(data.section_books).map(bk => bk);
                    let l1 = Object.keys(data.section_books).map(bk_id => bk_id);
                    this.section_books = l;
                    this.section_books_id = l1;
                })
                .catch(err => console.log(err))
            }   
        },
        get_url_for_download(){
            return `data:application/pdf;base64,${this.book.book_content_base64_encoded}`
        }
    },
    methods: {
        addItemToCart() {
            fetch("http://127.0.0.1:5000/user/check_cart",{
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                    "Content-Type": "application/json"
                },
                method: "GET"
            }).then(res => {return res.json()})
            .then(data => {
                if (data.msg == "Cart is not present") {
                    fetch("http://127.0.0.1:5000/user/create_cart",{
                        headers: {
                            "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                            "Content-Type": "application/json"
                        },
                        method: "POST"
                    }).then(res => {return res.json()})
                    .then(data => {
                        fetch("http://127.0.0.1:5000/user/add_to_cart",{
                            headers: {
                                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                                "Content-Type": "application/json"
                            },
                            method: "POST",
                            body: JSON.stringify({"book_id": this.book_id})
                        }).then(res => {return res.json()})
                        .then(data => {
                            if (data.msg == "Book added sucessfully"){
                                swal("Done", "Book added to cart successfully", "success")
                            } else{
                                swal("Book Exists", "The book already exists in your cart", "info")
                            }
                        })
                        .catch(err => console.log(err))
                    })
                    .catch(err => console.log(err))
                } else{
                        fetch("http://127.0.0.1:5000/user/add_to_cart",{
                                headers: {
                                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                                    "Content-Type": "application/json"
                                },
                                method: "POST",
                                body: JSON.stringify({"book_id": this.book_id})
                        }).then(res => {return res.json()})
                        .then(data => {
                            if (data.msg == "Book added sucessfully"){
                                swal("Done", "Book added to cart successfully", "success")
                            } else{
                                swal("Book Exists", "The book already exists in your cart", "info")
                            }
                        })
                        .catch(err => console.log(err))
                }
            })
        },
        requestBook(){
            fetch("http://127.0.0.1:5000/user/request_book",{
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                    "Content-Type": "application/json"
                },
                method: "POST",
                body: JSON.stringify({"book_id": this.book_id})
            }).then(res => {return res.json()})
            .then(data => {
                swal("Done", "Book requested successfully", "success")
            })
            .catch(err => console.log(err))
        },
        BuyBook(){
            swal("Payment Successfull", "Thank you for purchasing with us", "success")
        },
        RedirectToBook(j){
            this.$router.push({path: `/book_info/${this.section_books_id[j]}`}).then(() => {window.location.reload();})  
        },
        RemoveFeedback(){
            swal({
                title: "Are you sure?",
                text: "Once deleted, you will not be able to recover this feedback!",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            }).then((willDelete) => {
                if (willDelete) {
                        fetch("http://127.0.0.1:5000/user/remove_feedback",{
                        headers: {
                            "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                            "Content-Type": "application/json"
                        },
                        method: "POST",
                        body: JSON.stringify({"book_id": this.book_id})
                        }).then(res => {return res.json()})
                        .then(data => {
                            swal("Done", "Feedback removed successfully", "success")
                        })
                        .catch(err => console.log(err))
                        swal("Done", "Feedback removed successfully", "success").then(() => {window.location.reload();})
                    }
                })
        },
        SendFeedback(e){
            e.preventDefault()
            const data = new FormData(e.target);
            const feedback = Object.fromEntries(data.entries()).fdb;
            this.formflag = false
            fetch("http://127.0.0.1:5000/user/add_feedback",{
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                    "Content-Type": "application/json"
                },
                method: "POST",
                body: JSON.stringify({"book_id": this.book_id, "feedback": feedback})
            }).then(res => {return res.json()})
            .then(data => {
                swal("Done", "Feedback added successfully", "success").then(() => {window.location.reload();})
            })
            .catch(err => console.log(err))
        }
    }
}


</script>
<template>
<Navbar></Navbar>
<div class="bgup">
    <div class="row mainrowup">
        <div class="col-5 leftcolup">
            <Usermenu></Usermenu>
        </div>
        <div class="col rightcolup">
            <header class="display-4"> My Cart </header>
            <template v-if="Object.values(cart_books).length > 0">
                <table class="table">
                    <thead>
                        <th scope="col"> Index </th>
                        <th scope="col"> Product </th>
                        <th scope="col"> Price </th>
                        <th scope="col"> Action </th>
                    </thead>
                    <tbody>
                        <template v-for="(i,j) in cart_books">
                            <tr>
                                <th> {{ j }} </th>
                                <td> {{ i.book_name }} </td>
                                <td> {{ i.book_price }} </td>
                                <td> <button class="btn btn-outline-primary" @click="RemoveFromCart(i.book_id)"> Remove </button> </td>
                            </tr>
                        </template>
                    </tbody>
                </table>
                <div class="total" style="text-align: right; margin: 30px 110px 0 ">
                    <strong> Total Price: </strong> {{ total_price_cal }}
                </div>
                <div class="buy">
                    <button class="btn btn-outline-primary mt-5 buybtn" @click="DownloadBooks"> Proceed to Buy </button>
                </div>
            </template>
            <template v-else>
                <router-link to="/user/home" class="btn btn-outline-primary" style="margin-top: 210px;"> Add Books Now </router-link>
            </template>
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
    background-image: url("@/assets/userbg.webp");
    background-size: cover;
    margin: 20px;
    margin-left: 30px;
    border-radius: 12px;
}
.mainrowup{
    min-height: 100vh;
}
.rightcolup{
    margin-top: 80px;
    text-align: center;
}
.table{
    text-align: center;
    margin-top: 75px;
}

</style>

<script>
import Navbar from "@/components/Navbar.vue"
import Footer from "@/components/Footer.vue"
import Usermenu from "@/components/Usermenu.vue"
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
export default{
    name: "Cart",
    mounted(){
        fetch("https://sohamk.pythonanywhere.com/user/check_cart",{
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                    "Content-Type": "application/json"
                },
                method: "GET"
            }).then(res => {return res.json()})
            .then(data => {
                if (data.msg == "Cart is not present") {
                    fetch("https://sohamk.pythonanywhere.com/user/create_cart",{
                        headers: {
                            "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                            "Content-Type": "application/json"
                        },
                        method: "POST"
                    }).then(res => {return res.json()})
                    .then(() => {
                        fetch("https://sohamk.pythonanywhere.com/user/get_cart",{
                        headers: {
                            "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                            "Content-Type": "application/json"
                        },
                        method: "GET"
                        }).then(res => {return res.json()})
                        .then(data => {
                            this.cart_books = data
                        })
                    })
                }
            })
            fetch("https://sohamk.pythonanywhere.com/user/get_cart",{
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                    "Content-Type": "application/json"
                },
                method: "GET"
            }).then(res => {return res.json()})
            .then(data => {
                this.cart_books = data
            })
        },
    data(){
        return{
            book_ids: [],
            cart_books: {},
            total_cart_price: 0
        }
    },
    components: {
        Navbar,
        Footer,
        Usermenu
    },
    methods: {
        RemoveFromCart(book_id){
            swal({
                    title: "Are you sure?",
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                }).then((willDelete) => {
                    if (willDelete) {
                        fetch("https://sohamk.pythonanywhere.com/user/remove_from_cart",{
                            headers: {
                                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`,
                                "Content-Type": "application/json"
                            },
                            method: "POST",
                            body: JSON.stringify({
                                "book_id": book_id
                            })
                        }).then(res => {return res.json()})
                        swal({
                        title: "Sucess",
                        text: "Book Removed from Cart",
                        icon: "success",
                        button: "OK",
                    }).then(() => {
                        window.location.reload()
                    })
                    }
                })
        },
        DownloadBooks(){
            swal({
                    title: "Payment Successful",
                    text: "Thanks for your purchase",
                    icon: "success",
                    button: "OK",
            }).then(() => {
                let l_pdfs = {}
                for (var i in this.cart_books) {
                    l_pdfs[this.cart_books[i].book_name] = this.cart_books[i].book_content
                }
                const zip = new JSZip();
                const pdfFolder = zip.folder('Books');
                for(var i in l_pdfs) {
                    pdfFolder.file(`${i}.pdf`, l_pdfs[i], { base64: true });
                }
                zip.generateAsync({ type: 'blob' }).then((content) => {
                    saveAs(content, 'Books.zip');
                });
            })
        }
    },
    computed:{
        total_price_cal(){
            let total_cart_price = 0
            for (var i in this.cart_books) {
                total_cart_price += this.cart_books[i].book_price
            }
            return total_cart_price
        }
    }
}
</script>
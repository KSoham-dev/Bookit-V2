<template>
            <div class="readbookbg" style="height: 100vh; width: 100vw; text-align: center;" >
                <iframe :src="'data:application/pdf;base64,' + book.book_content_base64_encoded" width="50%" height="100%"></iframe>
                <button class="btn btn-primary backbtn" @click="$router.go(-2)"> Go Back </button>
            </div>
            <div>
                
            </div>
</template>

<style scoped>
.readbookbg{
      background-image: url("@/assets/bgreadbook.png");
      overflow: hidden;
    }
.backbtn{
    position: absolute;
    bottom: 300px;
    right: 1200px;
}
    
</style>
<script>
export default {
    name: 'readBook',
    mounted() {
        fetch("https://sohamk.pythonanywhere.com/books",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
            }
        }).then(res => res.json())
        .then(data => {
            this.books = data
            for (const book of Object.values(this.books)){
               if(book.book_id == this.$route.params.book_id){
                   this.book = book
               }
           }
        })
        .catch(err => console.log(err))
        
    },
    data() {
        return {
            books: {},
            book: {}
        }
    }
}
</script>
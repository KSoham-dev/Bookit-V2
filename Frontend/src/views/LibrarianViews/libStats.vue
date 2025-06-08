<template>
<Navbar></Navbar>
    <div class="bgup">
        <div class="row mainrowup">
            <div class="col-5 leftcolup">
                <Libmenu></Libmenu>
            </div>
                <div class="col rightcolup">
                    <header class="display-4 mb-4">Statistics</header>
                    <div class="img1 mb-4" >
                        <h1 class="display-6" style="font-size: 30px;"> Distribution of books issued within sections</h1><br/>
                        <img :src="img1_src" width="500" height="300" >
                    </div>
                    <div class="img2">
                        <h1 class="display-6" style="font-size: 30px;"> Distribution of books within sections</h1><br/>
                        <img :src="img2_src" width="500" height="300">
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
import Navbar from '../../components/Navbar.vue'
import Footer from '../../components/Footer.vue'
import Libmenu from '../../components/Libmenu.vue'
export default {
    name: "libStats",
    data(){
        return {
            img1_src: "",
            img2_src: ""

        }
    },
    components: {
        Navbar,
        Footer,
        Libmenu
    },
    mounted(){
        fetch('https://sohamk.pythonanywhere.com/lib/get_stats', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('ac_token')
            },
        }).then(res => res.json())
        .then(data => {
            this.img1_src = data.img1_src
            this.img2_src = data.img2_src
        }).catch(err => {
            console.log(err)
        })
    }
}
</script>
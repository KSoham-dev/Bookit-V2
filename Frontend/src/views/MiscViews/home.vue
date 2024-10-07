<template>
    <Navbar></Navbar>
    <div class="container mainhome" action="/login" style="margin-top: 50px; text-align: center;">
        <template v-for="(section, i) in sections">
            <template v-if="Object.keys(section.section_books).length  > 0">
                <strong>Section: {{ section.section_name }}</strong><br/><br/>
                {{section.section_description}}
            </template>
            <div class="row" style="margin-bottom: 50px; text-align: center;">
                <template v-for="(book, j) in section.section_books">
                    <div class="row colimghome">
                        <div class="col"></div>
                        <div class="col" style="padding-left: 80px;">
                            <router-link :to="`/book_info/${j}`">
                                <div class="divincol">
                                    <img src="@/assets/singlebook.webp" class="bkimg" height="210px"/>
                                        <div class="imglabel">
                                            <span class="imgtext">{{book}}</span>
                                        </div>
                                </div>
                            </router-link>
                        </div>
                        <div class="col"></div>
                    </div>
                </template>
            </div>
        </template>
    </div>
    <Footer></Footer>
</template>


<style scoped>

.bghome, .mainhome{
    min-height: 100vh;
}

.divincol{
  width: 210px;
  text-align: center;
  margin:20px;
}

.bkimg{
  border-radius: 5px;
}
.colimghome{
   margin: 40px 10px 0 20px; 
   vertical-align:bottom;
}
.imglabel{
  margin:30px;
}
a{
  text-decoration: none;
  color: black;
  font-weight: bold;
}

</style>

<script>
import Navbar from "@/components/Navbar.vue"
import Footer from "@/components/Footer.vue"
export default {
    name: "home",
    components: {
        Navbar,
        Footer 
    },
    data() {
        return {
            usr_id: 0,
            sections: {}
        }
    },
    mounted(){
        fetch("http://127.0.0.1:5000/auth/myinfo",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
            }
        }).then(res => res.json())
        .then(data => {
            this.usr_id = data.user_details.usr_id;
        })
        .catch(err => console.log(err))
        fetch("http://127.0.0.1:5000/sections",{
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                }
            }).then(res => res.json())
            .then(data => {
                this.sections = data
                console.log(data)
        })
        .catch(err => console.log(err))
    }
}
</script>
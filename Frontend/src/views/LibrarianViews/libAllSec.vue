<template>
<Navbar></Navbar>
    <div class="bgup">
        <div class="row mainrowup">
            <div class="col-5 leftcolup">
                <Libmenu></Libmenu>
            </div>
                <div class="col rightcolup">
                    <header class="display-4 mb-5"> Sections </header>
                    <table class="table">
                        <thead>
                            <th scope="col">Index</th>
                            <th scope="col">Section Name</th>
                            <th scope="col">Section Description</th>
                            <th scope="col">Date Created</th>
                            <th scope="col">Action</th>
                        </thead>
                        <tbody>
                            <template v-for="(i, j) in sections">
                                    <tr>
                                        <td>{{ j }}</td>
                                        <td>{{ i.section_name }}</td>
                                        <td>{{ i.section_description }}</td>
                                        <td>{{ i.section_date_created }}</td>

                                        <td><button class="btn btn-outline-primary btn-sm m-2" 
                                            @click="updtflag = true, updt_section_name = i.section_name, 
                                            updt_section_desc = i.section_description, updt_section_id = i.section_id">
                                                Update
                                            </button>
                                            <button class="btn btn-outline-primary btn-sm" @click="removeSection(i.section_id)">Remove</button>
                                        </td>
                                    </tr>
                            </template>
                        </tbody>
                    </table>
                    <template v-if="updtflag">
                        <div class="formdiv">
                            <form @submit.prevent="updateSection" class="fdbform">
                                <button type="button" class="close"><img src="@/assets/cross.svg" @click="updtflag = false"></button>
                                <span style="position: relative; right: 130px; font-weight: bold;">Enter Name:</span> <input class="form-control" type="text" name="section_name" :value="updt_section_name">
                                <span style="position: relative; right: 100px; font-weight: bold;">Enter Description:</span> <input class="form-control" type="text" name="section_description" :value="updt_section_desc">
                                <input class="btn btn-outline-primary" type="submit" value="Submit">
                            </form>
                        </div>
                    </template>
                    <template v-if="addflag">
                        <div class="formdiv">
                            <form @submit.prevent="addSection" class="fdbform">
                                <button type="button" class="close"><img src="@/assets/cross.svg" @click="addflag = false"></button>
                                <span style="position: relative; right: 130px; font-weight: bold;">Enter Name:</span> <input class="form-control" type="text" name="section_name" placeholder="Section Name">
                                <span style="position: relative; right: 100px; font-weight: bold;">Enter Description:</span> <input class="form-control" type="text" name="section_description" placeholder="Section Description">
                                <input class="btn btn-outline-primary" type="submit" value="Submit">
                            </form>
                        </div>
                    </template>
                    <button class="btn btn-outline-primary btn-lg m-5" @click="addflag = true">Add Section</button>
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
    
    .formdiv{
        position: relative;
        bottom: 330px;
        left: 93px;
        background: #f5f5f5;
        padding: 60px;
        width: 500px;
        height: 320px;
        border: 1px solid black;
        box-shadow: 5px 5px 10px 1px rgba(0,0,0,0.3);
        border-radius: 10px;
    }
    .formdiv .form-control{
        margin-top: 5px;
        margin-bottom: 10px;
        border-radius: 0;
        border: none;
        background: none;
        border-bottom: 1px solid black;
    }
    .formdiv .btn{
        margin-top: 30px;
        margin-left: 30px;
    }
    .close{
        border: none; 
        background: transparent; 
        position: absolute;
        bottom: 260px; 
        left: 450px;
    }
</style>

<script>
import Navbar from "@/components/Navbar.vue"
import Footer from "@/components/Footer.vue"
import Libmenu from "@/components/Libmenu.vue" 
export default{
    name: "allSections",
    data(){
        return{
            sections: {},
            updtflag: false,
            addflag: false,
            updt_section_name: "",
            updt_section_desc: "",
            updt_section_id: ""
        }
    },
    mounted(){
        fetch("http://127.0.0.1:5000/sections",{
            method: "GET",
            headers:{
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
            }
        }).then((response) => {
            return response.json()
        }).then((data) => {
            this.sections = data
        })
    },
    components:{
        Navbar,
        Footer,
        Libmenu
    },
    methods:{
        updateSection(ev){
            const data = new FormData(ev.target);
            const dataJson = Object.fromEntries(data.entries());
            let dataToSend = {...dataJson, section_id: this.updt_section_id}
            fetch("http://127.0.0.1:5000/sections/update_section",{ 
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                },
                body: JSON.stringify(dataToSend)
            }).then((response) => {
                if (response.status == 200){
                    swal("Done", "Section Updated", "success").then(() => {window.location.reload()})
                } 
            }).catch((error) => {
                console.log(error)
            })
        },
        removeSection(section_id){
            swal({
                title: "Are you sure?",
                text: "Do you really want to remove this section?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            }).then((willDelete) => {
                if (willDelete) {
                    fetch(`http://127.0.0.1:5000/sections/delete_section`,{
                        method: "POST",
                        headers:{
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                        },
                        body: JSON.stringify({section_id: section_id})
                    }).then((response) => {
                        if (response.status == 200){
                            swal("Done", "Section Removed", "success").then(() => {window.location.reload()})
                        }
                    })
                }
            })
        },
        addSection(ev){
            const data = new FormData(ev.target);
            const dataJson = Object.fromEntries(data.entries());
            fetch("http://127.0.0.1:5000/sections/add_section",{
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                },
                body: JSON.stringify(dataJson)
            }).then((response) => {
                if (response.status == 200){
                    swal("Done", "Section Added", "success").then(() => {window.location.reload()})
                }
            }).catch((error) => {
                console.log(error)
            })
        
        }
    }
}
</script>
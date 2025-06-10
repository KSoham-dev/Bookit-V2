<template>
    <Navbar></Navbar>
    <div class="bgup">
        <div class="row mainrowup">
            <div class="col-5 leftcolup">
                <Usermenu></Usermenu>
            </div>
                <div class="col rightcolup updtfrm">
                    <header class="display-4"> Update Profile Details </header><br /><br /><br />
                    <form autocomplete="off" method="POST" @submit.prevent="sendData">
                        <input type="email" name="email" :placeholder="user.email" class="inp" disabled><br /><br /><br />
                        <input type="text" name="fname" placeholder="First Name" class="inp" required><br /><br /><br />
                        <input type="text" name="lname" placeholder="Last Name" class="inp" required><br /><br /><br />
                        <input type="password" name="pass" placeholder="Confirm your password" class="inp" required><br /><br /><br />
                        <input type="submit" value="Update" class="submit">
                    </form>
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
    .inp{
        width: 500px
    }
    .submit{
        width: 250px;
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
    .usernameup{
      position: relative;
      left: 50px;
    }
    .emailup{
      position: relative;
      left: 60px;
      top: 10px;
    }
    .updtfrm,.updtable{
      margin-top: 150px;
      text-align: center;
    }     
    .usrmenu{
      margin-left: 80px;
      margin-top: 40px;
    }
     .bookstable{
      text-align: center;
      margin-top: 75px;
     }
     a{
    text-decoration: none;
    font-weight: 700;
    color: rgb(0,0,0);
    }
    .submit{
    background: transparent;
    border-radius: 10px;
    box-shadow: 5px 5px 10px 1px rgba(0,0,0,0.3);
    }
    .inp{
    border: none;
    border-bottom: 1px solid black;
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
import Usermenu from '@/components/Usermenu.vue';
export default {
    name: "userProfile",
    mounted(){
        fetch("https://bookit-v2-s4t8.onrender.com/auth/myinfo",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
            }
        }).then(res => res.json())
        .then(data => {
            this.user = data.user_details
        })
        .catch(err => console.log(err))
    },
    components: {
        Navbar,
        Footer,
        Usermenu
    },
    data(){
        return{
            user: {},
        }
    }, 
    methods:{
        sendData(ev){
            const data = new FormData(ev.target);
            const dataJson = Object.fromEntries(data.entries());
            const dataToSend = JSON.stringify({...dataJson});
            fetch("https://bookit-v2-s4t8.onrender.com/auth/updtusr",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                },
                body: dataToSend
            })
            .then(function(response){
                if (!response.ok){
                    if(response.status == 401){
                        swal("Error!", "Invalid Password", "error")
                        throw new Error('HTTP error, status = ' + response.status)
                    }
                }
                return response.json();
            })
            .then(() => {swal("Success!", "Profile updated successfully", "success").then(() => {window.location.reload()})})
            .catch(err => console.log(err))
        }
    }   
}
</script>
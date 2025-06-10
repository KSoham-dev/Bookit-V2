<template>
      <div class="bg">
        <div class="container d-flex justify-content-center align-items-center min-vh-100">
          <div class="row whitebg">
            <div class="col-6 leftimg">
              <img class="imglogo" src="@/assets/Bookitwh.webp" height="100px" width="100px"/>
            </div>
            <div class="col-6 rightside d-flex justify-content-center align-items-center">
              <div class="role">
                <a href="/" style="font-weight: 100;">User</a> | <a href="/lib/login" style="font-weight: 100;">Librarian</a>
              </div>
              <div class="login">
                <header class="display-6"> Sign Up </header>
                <form autocomplete="off" method="POST" @submit.prevent="handleSubmit">
                    <input type="email" name="email" placeholder="Email" class="inp" required> <br /><br />
                    <input type="text" name="f_name" placeholder="First Name" class="inp" required><br /><br />
                    <input type="text" name="l_name" placeholder="Last Name" class="inp" required><br /><br />
                    <input type="password" name="password" placeholder="Password" class="inp" required><br /><br />
                    <input type="submit" value="Sign Up" class="submit" @mouseover="hovered = true" @mouseleave="hovered = false" 
                    :style="{
                      'box-shadow' : hovered ? '5px 5px 10px 1px rgba(0,0,0,0.4)' : '' , 
                      'background-color' : hovered ? 'rgb(225, 195, 150)' : '' , 
                      'color' : hovered ? 'white' : '',
                    }">
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer></Footer>
</template>
<script>
import swal from 'sweetalert';
import router from '@/router/index.js'
import Footer from '@/components/Footer.vue'
export default {
    name: 'userSignup',
    data(){
        return{
          hovered: false,
          success: false
        }
      },
        methods: {
          handleSubmit(ev){
            const data = new FormData(ev.target);
            const dataJson = Object.fromEntries(data.entries());
            const dataToSend = JSON.stringify({...dataJson, role: 'user'});
            fetch('https://bookit-v2-s4t8.onrender.com/auth/user/signup', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: dataToSend
            }).then(function(response) {
                if (!response.ok){
                    if (response.status == 409) {
                      swal("OOPS!", "Email already exists!", "error");
                    }
                    throw new Error('HTTP error, status = ' + response.status)
                }
                return response.json()
                }).then(function(data) {
                    swal("Done!", "User created successfully!", "success");
                    router.push('/')
                }).catch(function(error) {
                    console.log(error)
                })
          }
        },
        components: {
          Footer
        }
}
</script>
<style scoped>
@import '~bootstrap/dist/css/bootstrap.min.css';
*{
    font-family: 'Courier New', monospace;
  }
.bg{
    background-image: url("@/assets/bgfinal.webp");
    padding: 0 18px 0 18px;
}
.leftimg{
    background-image: url("@/assets/Signup.webp");
}
.leftimg{
    background-position: center;
    background-size: cover;
    position: relative;
    border-radius: 9px 0 0 9px;
}
.whitebg{
    width: 912px;
    height: 561px;
    border-radius: 9px;
    background: rgb(255, 255, 255);
    box-shadow: 5px 5px 10px 1px rgba(0, 0, 0, 0.3);
}
.rightside{
    position: relative;
}
.login header{
    font-weight: 710;
    text-align: center;
    margin-bottom: 48px;
}
.inp{
    width: 100%;
    background: transparent;
    border: none;
    border-bottom: 2px solid rgba(0,0,0,0.3);
}
.submit{
    width:100%;
    background: transparent;
    border-radius: 10px;
}
.signup{
    text-align: center;
    font-size: small;
    margin-top: 25px;
}
a{
    text-decoration: none;
    font-weight: 700;
    color: rgb(0,0,0);
}
.role{
    position: absolute;
    margin-bottom: 110%;
    margin-left: 50%;
}
.imglogo{
    position:absolute;
    top:10px;
    left:10px;
}
p{
    position: relative;
    top: 50px;
    background-color: rgba(0, 255, 0, 0.5);
}
</style>

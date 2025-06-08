<template>
    <div class="lefttextup">
    <img src="@/assets/user-line-black-big.webp" alt="Big user icon" class="usriconup"/>
    <span class="usernameup"><h1 class="display-6">{{user.f_name}}  {{user.l_name}}</h1></span>
    <span class="emailup"><h5>{{user.email}}</h5></span>
    <div class="usrmenu">
        <ul style="list-style-type: none;">
            <li class="usrmenu_links"><router-link to="/user/profile" active-class="active-link"> Edit Profile</router-link></li><br/>
            <li class="usrmenu_links"><router-link to="/user/books" active-class="active-link"> My Books</router-link> </li><br/>
            <li class="usrmenu_links"> <router-link to="/user/books_req" active-class="active-link"> Books requested</router-link></li><br/>
        </ul>
    </div>
</div>
</template>

<style scoped>
    a{
    text-decoration: none;
    font-weight: 700;
    color: rgb(0,0,0);
    } 
    .usrmenu{
      margin-left: 80px;
      margin-top: 40px;
    }
    .active-link{
    border-bottom: 2px solid rgb(0,0,0);
    padding-bottom: 10px;
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
</style>

<script>
    export default {
    name: "userProfile",
    mounted(){
        fetch("https://sohamk.pythonanywhere.com/auth/myinfo",{
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
    data(){
        return {
            user: {}
        }
    }
}
</script>
<template>
    <footer>
        <img src="@/assets/copyright-line.webp"> Bookit, 2024. All rights reserved
        <a href="/about" style="color: rgb(255,255,255); position: absolute; left: 1300px;"> About us </a>
    </footer>
</template>

<script>
export default {
    name: "Footer"
}
</script>

<style scoped>
footer{
    background-color: rgb(35, 35, 35);
    height: 60px;
    color: rgb(255, 255, 255);
    padding: 20px;
    }
a{
    text-decoration: none;
    font-weight: 700;
    color: rgb(0,0,0);
}
</style> 
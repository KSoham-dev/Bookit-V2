<template>
    <div class="frm">
        <header class="display-4"> Add a Book </header><br /><br /><br />
        <form autocomplete="off" @submit.prevent="addBook" enctype="multipart/form-data" >
            <strong><label for="book_name" style="position: relative; right: 260px;" class="label"> Book Name </label></strong><br /><br />
            <input type="text" name="book_name" placeholder="Book Name" class="inp" required><br /><br /><br />
            <strong><label for="book_description" style="position: relative; right: 225px;" class="label"> Book Description </label></strong><br /><br />
            <input type="text" name="book_description" placeholder="Book Description" class="inp" required><br /><br /><br />
            <strong><label for="price" style="position: relative; right: 250px;" class="label"> Book Price </label></strong><br /><br />
            <input type="text" name="price" placeholder="Book Price" class="inp" required><br /><br /><br />
            <strong><label for="section_id" style="position: relative; right: 260px;" class="label"> Section </label></strong><br/><br />
            <select name="section_id"  style="position: relative; right: 190px;" required>
                    <template v-for="(section,index) in sections">
                        <option :value="index"> {{section}} </option>
                    </template>
            </select><br/><br/><br/>
            <strong><label for="authors" style="position: relative; right: 250px;"> Author(s) </label></strong><br/><br />
            <select name="authors"  v-model="selected" style="position: relative; right: 190px;" multiple required>
                    <option v-for="(author,index) in authors" :value="index">{{author}}</option>
            </select><br/><br/><br/>

            <strong><label for="pdf" style="position: relative; right: 200px;"> Add Book Content </label></strong><br /><br />
            <input type="file" name="pdf" accept="application/pdf" style="position: relative; right: 90px;" required><br/><br/><br/><br/><br/>
            <input type="submit" value="Add" class="submit">
        </form>
    </div>
</template>


<style scoped>
.inp{
      border: 0px;
      border-bottom: 1px solid black;
      background-color: rgb(255,255,255);
      width: 500px;
}
.label{
      position: relative;
      right: 40px;
}
.submit{
    border-radius: 10px;
    background: transparent;
    border: 2px solid black;
    width: 250px;
}
.frm{
    margin-top: 80px;
}
</style>
<script>
export default {
    name: "Addbkfrm",
    props: {
        Books: Object,
        flag: Boolean
    },
    data(){
        return {
            sections: {},
            authors: {},
            content: "",
            selected: []
        }
    },
    computed(){
    },
    methods: {
        addBook(ev){
            const data = new FormData(ev.target);
            const dataJson = Object.fromEntries(data.entries());
            let file = ev.target.elements.pdf.files[0];
            var fileReader = new FileReader()
            fileReader.onload = (e) => {
                let content = e.target.result;
                const keys = Object.keys(dataJson);
                const lastKey = keys.pop();
                delete dataJson["authors"];
                delete dataJson[lastKey];
                fetch("https://bookit-v2-s4t8.onrender.com/books/add_book",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                },
                body: JSON.stringify({...dataJson, "content": content.slice(28), "authors": Object.values(this.selected)})
                }).then((response) => {
                    if (response.status == 200 ){
                        swal({
                            title: "Book Added",
                            text: "Book Added Successfully",
                            icon: "success"
                        }).then(() => {
                            window.location.reload();
                        })
                    }else{
                        swal("Error", "Book already exists", "error");
                    }
                    return response.json();
                }).catch((error) => {
                    console.log(error);
                })
            };
            fileReader.readAsDataURL(file);
        }
    },
    mounted(){
        fetch("https://bookit-v2-s4t8.onrender.com/sections/get_names",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
            },
        }).then((response) => {
            return response.json();
        }).then((data) => {
            this.sections = data;
        })
        fetch("https://bookit-v2-s4t8.onrender.com/authors/get_names",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
            },
        }).then((response) => {
            return response.json();
        }).then((data) => {
            this.authors = data;
        })
    }
}
</script>
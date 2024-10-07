<template>
    <template v-for="(bk,i) in Books">
        <template v-if="bk.book_id == bk_id">       
            <div class="frm">
                <header class="display-4"> Update Book Details </header><br /><br /><br />
                <form autocomplete="off" @submit.prevent="updateBook" enctype="multipart/form-data">
                    <strong><label for="book_id" style="position: relative; right: 275px;"> Book ID </label></strong><br /><br />
                    <input type="text" name="book_id" :placeholder="bk.book_id" class="inp" disabled><br /><br /><br />
                    <strong><label for="book_name" style="position: relative; right: 260px;"> Book Name </label></strong><br /><br />
                    <input type="text" name="book_name" placeholder="Book Name" class="inp" :value="bk.book_name" required><br /><br /><br />
                    <strong><label for="book_description" style="position: relative; right: 225px;"> Book Description </label></strong><br /><br />
                    <input type="text" name="book_description" placeholder="Book Description" class="inp" :value="bk.book_description" required><br /><br /><br />
                    <strong><label for="uprice" style="position: relative; right: 250px;"> Book Price </label></strong><br /><br />
                    <input type="text" name="price" placeholder="Book Price" class="inp" :value="bk.book_price" required><br /><br /><br />
                    <strong><label for="section_id" style="position: relative; right: 260px;"> Section </label></strong><br/><br /><label style="position: relative; left: 100px;">Current Section: {{bk.book_section.section_name}}</label>
                    <select name="section_id" style="position: relative; right: 300px;" required>
                        <template v-for="(section,j) in sections">
                            <template v-if="j == bk.book_section.section_id">
                                <option :value="j" selected>{{section}} </option>
                            </template>
                            <template v-else>
                                <option :value="j">{{section}} </option>
                            </template>
                        </template>
                    </select><br/><br/><br/>
                    <template v-if="bk.book_authors">
                        <strong><label for="authors" style="position: relative; right: 250px;"> Author(s) </label></strong><br/><br />
                        <label style="position: relative; left: 160px; bottom: 30px;">
                            Current Author(s): {{bk.book_authors.author_names.join(", ")}}
                        </label>
                        <select name="authors"  style="position: relative; right: 350px;" multiple>
                            <template v-for="(author,j) in authors">
                                <template v-if="bk.book_authors.author_names.includes(author)">
                                    <option :value="j" selected>{{author}}</option>
                                </template>
                                <template v-else>
                                    <option :value="j">{{author}}</option>
                                </template>
                            </template>
                        </select><br/><br/><br/>
                    </template>
                    <strong><label for="pdf" style="position: relative; right: 200px;"> Change Book Content </label></strong><br /><br />
                    <input type="file" name="pdf" accept="application/pdf" ><router-link :to="`/read/${bk.book_id}`" style="position: relative; left: 10px; text-decoration:none; color: black;"><i>View Current Content</i></router-link><br /><br /><br />
                    <input type="submit" value="Update" class="submit">
                </form>
            </div>
        </template>
    </template>
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
        flag: Boolean,
        bk_id: Number
    },
    data(){
        return {
            sections: {},
            authors: {},
            aut_selected: []
        }
    },
    computed(){
    },
    methods: {
        updateBook(ev){
            const data = new FormData(ev.target);
            const dataJson = Object.fromEntries(data.entries());
            let file = ev.target.elements.pdf.files[0];
            var fileReader = new FileReader()
            if(file){
                fileReader.onload = (e) => {
                let content = e.target.result;
                const keys = Object.keys(dataJson);
                const lastKey = keys.pop();
                delete dataJson["authors"];
                delete dataJson[lastKey];
                let selOptions = ev.target.elements.authors.selectedOptions;
                let l_aut = []
                for (const option of selOptions) {
                    l_aut.push(option.value);
                }
                let dataToSend = {...dataJson, "content": content.slice(28), "authors": l_aut, "book_id":this.bk_id}
                fetch("http://127.0.0.1:5000/books/update_book",{
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                    },
                    body: JSON.stringify(dataToSend)
                }).then((response) => {
                    return response.json();
                }).then((data) => {
                    if (data.message == "Book updated successfully"){
                        swal({
                            title: "Done",
                            text: "Book updated successfully",
                            icon: "success",
                            button: "OK",
                        }).then(() => {
                            window.location.reload();
                        })
                    }
                }).catch((error) => {
                    console.log(error);
                })
            };
                fileReader.readAsDataURL(file);
            } else{
                    delete dataJson["authors"];
                    const lastKey = Object.keys(dataJson).pop();
                    delete dataJson[lastKey];
                    let selOptions = ev.target.elements.authors.selectedOptions;
                    let l_aut = []
                    for (const option of selOptions) {
                        l_aut.push(option.value);
                    }
                    let dataToSend = {...dataJson, "authors":l_aut, content:"", "book_id":this.bk_id}
                    fetch("http://127.0.0.1:5000/books/update_book",{
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("ac_token")}`
                    },
                    body: JSON.stringify(dataToSend)
                    }).then((response) => {
                        return response.json();
                    }).then((data) => {
                        if (data.message == "Book updated successfully"){
                            swal({
                                title: "Done",
                                text: "Book updated successfully",
                                icon: "success",
                                button: "OK",
                            }).then(() => {
                                window.location.reload();
                            })
                        }
                    }).catch((error) => {
                        console.log(error);
                    })
                }
        }
    },
    mounted(){
        fetch("http://127.0.0.1:5000/sections/get_names",{
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
        fetch("http://127.0.0.1:5000/authors/get_names",{
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
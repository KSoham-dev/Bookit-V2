<template>
        <h1 class="display-6 mb-2 srchhead">Search Results</h1>
        <template v-if="result.results.object == 'book'">
            <div class="row">
                <template v-for="(book, i) in result.results.book_names">
                        <div class="col colimghome text-center">
                        <router-link :to="`/book_info/${result.results.book_ids[i]}`">
                            <div class="divincol">
                                <img src="@/assets/singlebook.webp" class="bkimg" height="210px"/>
                                <div class="imglabel mt-4">
                                    <span class="imgtext">{{book}}</span>
                                </div>
                            </div>
                        </router-link>
                    </div>
                </template>
            </div>
        </template>

        <template v-if="result.results.object == 'section'">
            <template v-for="(itm, i) in result">
                <template v-for="(section, i) in computeSection(itm)">
                    <div class="mb-3 display-6" style="font-size: 25px;">Section: {{ section.section_name }}</div>
                    <div class="desc mb-4">Description: {{section.section_description}}</div>
                    <div class="row" style="margin-bottom: 50px;">
                        <div class="mb-3">Books in {{ section.section_name }}:</div>
                        <template v-for="(book, j) in section.section_books">
                            <div class="col colimghome">
                                <router-link :to="`/book_info/${j}`">
                                    <div class="divincol text-center">
                                        <img src="@/assets/singlebook.webp" class="bkimg" height="210px"/>
                                        <div class="imglabel mt-4">
                                            <span class="imgtext">{{book}}</span>
                                        </div>
                                    </div>
                                </router-link>
                            </div>
                        </template>
                    </div>
                </template>
            </template>
        </template>

        <template v-if="result.results.object == 'author'">
            <template v-for="(itm, i) in result">
                <template v-for="(author, i) in computeAuthor(itm)">
                    <div class="mb-3 display-6" style="font-size: 25px;">Author: {{ author.author_name }}</div>
                    <div class="desc mb-4" style="font-size: 20px;">Description: {{author.author_description}}</div>
                    <div class="mb-3">Books by {{ author.author_name }}:</div>
                    <div class="row" style="margin-bottom: 50px;">
                        <template v-for="(book, j) in author.author_books">
                            <div class="col colimghome text-center">
                                <router-link :to="`/book_info/${j}`">
                                    <div class="divincol">
                                        <img src="@/assets/singlebook.webp" class="bkimg" height="210px"/>
                                        <div class="imglabel mt-4">
                                            <span class="imgtext">{{book}}</span>
                                        </div>
                                    </div>
                                </router-link>
                            </div>
                        </template>
                    </div>
                </template>
            </template>
        </template>
</template>

<style scoped>
.imgtext, a{
    color: black; 
    font-weight: bold;
    text-decoration: none;
}
.srchhead{
    position: relative; 
    bottom: 20px;
}
</style>

<script>
export default {
    name: "searchResults",
    props: {
        result: Object,
        resultFlag: Boolean
    },
    methods: {
        computeSection(itm){
            const {object:_, ...rest} = itm;
            return rest;
        },
        computeAuthor(itm){
            const {object:_, ...rest} = itm;
            return rest;
        }
    }
}
</script>

<template>
  <div>
    <v-layout row wrap>
        <v-flex
          v-for="loadedPicture in loadedPictures" :key="loadedPicture.id"
          class="pt-2 pr-3"
          xl3 lg4 md6 xs12
          style="position: relative;"
        >
          <div class="image-area pa-2" @click="openPicture(loadedPicture.id)">
            <v-img :src="getPictureUrl(loadedPicture.id)"/>
            <div class="image-date">
              {{getDateTime(loadedPicture.loadDate)}}
            </div>
          </div>
        </v-flex>
    </v-layout>
    <my-picture ref="myPicture"/>
  </div>
</template>

<script>
  import MyPicture from '../components/common/MyPicture'
  import gql from 'graphql-tag'

  export default {
    name: "myPictures",
    components: {MyPicture},
    data() {
      return {
        loadedPictures: []
      }
    },
    apollo: {
      query: {
        query: gql`
          query {
            getAllMyPictures {
              id
              text
              loadDate
            }
          }
        `,
        update(data) {

          this.loadedPictures = data.getAllMyPictures
        }
      }
    },
    methods: {
      getPictureUrl(pictureId) {
        return 'http://localhost:8000/picture?picture_id=' + pictureId
      },
      getDateTime(stringDatetime) {
        let datetime = new Date(stringDatetime)
        let day = datetime.getDate()
        let month = datetime.getMonth() + 1
        let year = datetime.getFullYear()
        let hour = datetime.getHours()
        let minute = datetime.getMinutes()
        return `${hour}:${minute} ${day}.${month}.${year}`
      },
      openPicture(imageId) {
        this.$refs.myPicture.openImage(imageId)
      }
    }
  }
</script>

<style scoped>
  .image-area {
    border-radius: 2px;
    border: 1px solid grey;
    max-width: 400px;
  }

  .image-date {
    position: absolute;
    left: 1px;
    top: 10px;
    background: rgba(0, 0, 0, 0.8);
    border-radius: 0 0 10px 0;
    padding: 10px;
  }
</style>
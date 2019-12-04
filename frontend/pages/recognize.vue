<template>
  <div>
    <upload-file-form
      ref="uploadFileForm"
      @selectedFiles="sendFile"
    />
    <v-btn @click="openChoiceFilesDialog" class="mt-5">
      Загрузить изображение
    </v-btn>
    <v-layout v-for="(loadedPicture, index) in loadedPictures" :key="loadedPicture.imageId" row wrap>
      <template>
        <v-flex xs3 class="pt-2 pr-3" style="position: relative;">
          <div class="image-area pa-2">
            <v-img :src="getPictureUrl(loadedPicture.imageId)"/>
          </div>
          <div class="remove-image">
            <v-btn @click="removeImage(index)" fab x-small color="white">
              <v-icon color="black">
                mdi-close
              </v-icon>
            </v-btn>
          </div>
        </v-flex>
        <v-flex xs9 class="pt-2 pl-4">
          <v-textarea
            label="Распознаный текст"
            v-model="loadedPicture.imageText"
            readonly
          />
        </v-flex>
      </template>
    </v-layout>
    <v-layout v-if="loadingPicturesCount" row wrap>
      <template>
        <v-flex xs3 class="pt-2 pr-3" style="position: relative;">
          <div class="image-area pa-2 pl-10">
            <v-progress-circular
              indeterminate
              color="primary"
              size="120"
            ></v-progress-circular>
          </div>
          <div class="remove-image">
            <v-btn @click="removeImage(index)" fab x-small color="white">
              <v-icon color="black">
                mdi-close
              </v-icon>
            </v-btn>
          </div>
        </v-flex>
        <v-flex xs9 class="pt-2 pl-4">
          <v-textarea
            label="Распознаный текст"
            readonly
          />
        </v-flex>
      </template>
    </v-layout>
  </div>
</template>

<script>
  import gql from 'graphql-tag'
  import UploadFileForm from "../components/common/UploadFileForm";

  export default {
    name: "recognize",
    components: {UploadFileForm},
    data() {
      return {
        loadedPictures: [],
        loadingPicturesCount: 0
      }
    },
    methods: {
      openChoiceFilesDialog() {
        this.$refs.uploadFileForm.openDialogFile()
      },
      sendFile(files) {
        files.forEach(file => {
          this.loadingPicturesCount += 1

          this.$apollo.mutate({
            mutation: gql`
            mutation($file:Upload!) {
              recognizeImage(file: $file){
                imageId
                imageText
              }
            }
          `,
            variables: {
              file: file
            },
            context: {
              hasUpload: true // activate Upload link
            }
          }).then(({data}) => {
            this.loadedPictures.push(data.recognizeImage)
            this.loadingPicturesCount -= 1
          })
        })
      },
      getPictureUrl(pictureId) {
        return 'http://localhost:8000/picture?picture_id=' + pictureId
      },
      removeImage(index) {
        this.loadedPictures.splice(index, 1)
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

.remove-image {
  position: absolute;
  top: 5px;
  right: 5px;
}
</style>
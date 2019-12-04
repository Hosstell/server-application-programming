<template>
  <div>
    <v-dialog v-model="dialog" width="600">
      <v-card>
        <v-card-title>
          <v-spacer/>
          <v-btn icon @click="closeDialog">
            <v-icon>
              mdi-close
            </v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-layout row wrap>
            <v-flex xs12>
              <v-img :src="getPictureUrl(mainImageId)"/>
            </v-flex>
            <v-flex xs12 class="pt-4">
              Все числа
            </v-flex>

            <v-flex xs2 v-for="child in children" class="pt-2 pr-2">
              <div>
                <v-img :src="getPictureUrl(child.id)"/>
              </div>
              <div>
                <v-text-field v-model="child.text" class="pa-0"/>
              </div>
            </v-flex>
          </v-layout>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn text @click="save" :loading="loading">
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import gql from 'graphql-tag'

  export default {
    name: "MyPicture",
    data() {
      return {
        dialog: false,
        mainImageId: null,
        children: [],
        loading: false
      }
    },
    apollo: {
      query: {
        query: gql`
          query($pictureId: String) {
            getPicture(pictureId:$pictureId) {
              id
              pictureSet {
                id
                text
              }
            }
          }
        `,
        variables() {
          return {
            pictureId: this.mainImageId
          }
        },
        update(data) {
          console.log(data.getPicture)
          this.children = data.getPicture.pictureSet
        }
      }
    },
    methods: {
       closeDialog() {
         this.dialog = false
       },
       openImage(imageId) {
         this.mainImageId = imageId
         this.dialog = true
       },
      getPictureUrl(pictureId) {
        return 'http://localhost:8000/picture?picture_id=' + pictureId
      },
      save() {
         let newText = []
         this.children.forEach(child => {
           newText.push({
             pictureId: child.id,
             newText: child.text
           })
         })

         this.loading = true
         this.$apollo.mutate({
           mutation: gql`
             mutation ($newText: [PictureText]) {
               newText(newText:$newText) {
                 result
               }
             }
           `,
           variables: {
             newText
           }
         }).then((data) => {
           this.loading = false
           this.closeDialog()
           console.log(data)
         })
      }
    }
  }
</script>

<style scoped>

</style>
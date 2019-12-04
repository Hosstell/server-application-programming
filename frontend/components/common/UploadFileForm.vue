<template>
  <form @change="handleFileChange" :class="{'full-width': fullWidth}">
    <input :id="id" type="file" class="hidden" multiple ref="input" :name="name">
    <label :for="id" class="cursor">
      <slot></slot>
    </label>
  </form>
</template>

<script>
  export default {
    name: 'UploadFileForm',
    props: {
      readonly: Boolean,
      fullWidth: Boolean,
      name: String
    },
    data () {
      return {
        id: Math.random().toString(36).substring(7)
      }
    },
    methods: {
      handleFileChange (event) {
        if (event.target.files.length) {
          this.$emit('selectedFiles', Array.from(event.target.files))
          let input = this.$refs.input
          input.type = 'text'
          input.type = 'file'
        }
      },
      openDialogFile () {
        document.getElementById(this.id).click()
      }
    }
  }
</script>

<style scoped>
  .hidden {
    display: none;
    cursor: pointer;
  }

  .cursor {
    cursor: pointer;
  }

  .full-width {
    width: 100%;
  }
</style>

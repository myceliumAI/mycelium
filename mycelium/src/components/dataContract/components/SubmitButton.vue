<template>
  <v-btn color="primary" :disabled="isDisabled" @click="submitObject">
    {{ buttonText }}
  </v-btn>
</template>

<script>
export default {
  name: 'SubmitButton',
  props: {
    isDisabled: {
      type: Boolean,
      default: false
    },
    buttonText: {
      type: String,
      default: 'Submit'
    }
  },
  emits: ['submitObject'],
  methods: {
    submitObject () {
      if (!this.isDisabled) {
        this.$emit('submitObject')
      }
    }
  }
}
</script>

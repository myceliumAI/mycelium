import js from '@eslint/js'
import vue from 'eslint-plugin-vue'

export default [
  js.configs.recommended,
  {
    files: ['**/*.vue'],
    plugins: {
      vue
    },
    rules: {
      ...vue.configs.essential.rules
    }
  },
  {
    ignores: ['dist/**', 'node_modules/**']
  }
]
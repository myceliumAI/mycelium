import eslintPluginVue from 'eslint-plugin-vue'
import js from '@eslint/js'
import * as vueParser from 'vue-eslint-parser'

// Get the recommended vue rules
const vueRules = eslintPluginVue.configs['vue3-recommended'].rules

export default [
  // Base ESLint recommended rules
  js.configs.recommended,
  
  // Vue specific configuration
  {
    files: ['src/**/*.{js,vue}'],
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: 'module',
      parser: vueParser,
      parserOptions: {
        ecmaVersion: 2024,
        sourceType: 'module',
        ecmaFeatures: {
          jsx: true
        }
      },
      globals: {
        // Browser globals
        window: 'readonly',
        document: 'readonly',
        console: 'readonly',
        setTimeout: 'readonly',
        setInterval: 'readonly',
        clearInterval: 'readonly',
        requestAnimationFrame: 'readonly',
        cancelAnimationFrame: 'readonly',
        // Vue 3 composition API globals
        defineProps: 'readonly',
        defineEmits: 'readonly',
        defineExpose: 'readonly',
        withDefaults: 'readonly',
        // Vite globals
        import: 'readonly',
      }
    },
    plugins: {
      vue: eslintPluginVue
    },
    rules: {
      ...vueRules,
      'vue/multi-word-component-names': 'off',
      'vue/require-default-prop': 'off',
      'no-console': 'off',
      'no-debugger': 'warn',
      // Disable v-html warning since we're using DOMPurify
      'vue/no-v-html': 'off',
      // Attribute order rules
      'vue/attributes-order': ['warn', {
        order: [
          'DEFINITION',
          'LIST_RENDERING',
          'CONDITIONALS',
          'RENDER_MODIFIERS',
          'GLOBAL',
          ['UNIQUE', 'SLOT'],
          'TWO_WAY_BINDING',
          'OTHER_DIRECTIVES',
          'OTHER_ATTR',
          'EVENTS',
          'CONTENT'
        ],
        alphabetical: false
      }]
    }
  }
]
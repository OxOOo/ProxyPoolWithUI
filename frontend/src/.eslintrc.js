module.exports = {
    root: true,
    env: {
        browser: true,
        node: true
    },
    parserOptions: {
        parser: 'babel-eslint'
    },
    extends: [
        '@nuxtjs',
        'plugin:nuxt/recommended'
    ],
    plugins: [
    ],
    // add your custom rules here
    rules: {
        semi: ['error', 'always'],
        indent: ['error', 4],
        'vue/html-indent': ['error', 4],
        camelcase: 'off',
        'no-return-await': 'off',
        'vue/no-parsing-error': 'off',
        'no-unused-vars': 'warn',
        'vue/html-self-closing': 'off',
        'prefer-const': 'warn',
        'vue/singleline-html-element-content-newline': 'off',
        'vue/no-unused-components': 'warn',
        'import/no-named-as-default': 'off',
        'vue/no-unused-vars': 'warn'
    }
};

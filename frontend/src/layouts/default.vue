<template>
    <div>
        <a-layout class="layout-main">
            <a-layout-sider collapsible>
                <div class="logo" />
                <a-menu v-model="url_path" theme="dark" mode="inline">
                    <a-menu-item key="/">
                        <NuxtLink to="/">
                            <a-icon type="home" />
                            <span>可用代理</span>
                        </NuxtLink>
                    </a-menu-item>
                    <a-menu-item key="/fetchers">
                        <NuxtLink to="/fetchers">
                            <a-icon type="retweet" />
                            <span>爬取器状态</span>
                        </NuxtLink>
                    </a-menu-item>
                    <a-menu-item key="github">
                        <a href="https://github.com/believedotchenyu/ProxyPoolWithUI" target="_blank">
                            <a-icon type="github" />
                            <span>Github主页</span>
                        </a>
                    </a-menu-item>
                </a-menu>
            </a-layout-sider>
            <a-layout>
                <a-layout-header style="background: #fff; padding: 0">
                </a-layout-header>
                <a-layout-content
                    :style="{ margin: '24px 16px', padding: '24px', background: '#fff' }"
                >
                    <Nuxt />
                </a-layout-content>
            </a-layout>
        </a-layout>
    </div>
</template>

<script>
export default {
    data () {
        return {
            url_path: []
        };
    },
    watch: {
        $route () {
            this.updateNav();
        }
    },
    mounted () {
        this.updateNav();
    },
    methods: {
        updateNav () {
            const data = /^\/[^/]*/.exec(this.$route.path || '');
            if (data) {
                this.url_path = [data[0]];
            } else {
                this.url_path = [];
            }
        }
    }
};
</script>

<style scoped>
.layout-main {
    min-height: 100vh;
}
.logo {
    height: 32px;
    background: rgba(255, 255, 255, 0.2);
    margin: 16px;
}
</style>

<style>
html {
  font-family:
    'Source Sans Pro',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    'Helvetica Neue',
    Arial,
    sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}
</style>

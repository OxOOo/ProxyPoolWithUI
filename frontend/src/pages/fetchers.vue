<template>
    <div>
        <a-row :gutter="16">
            <a-col :span="4">
                <a-card :body-style="{padding: '20px 24px 4px'}">
                    <p>
                        自动刷新:
                        <a-switch v-model="autoupdate" />
                    </p>
                    <p>刷新时间：{{ lastupdate }}</p>
                </a-card>
            </a-col>
            <a-col :span="4">
                <a-card :body-style="{padding: '20px 24px 43px'}">
                    <div style="text-align: center">
                        <a-button type="primary" @click="clearStatus">
                            清空统计信息
                        </a-button>
                        <a-tooltip title="清空`总共爬取代理数量`等，已经爬取到的代理不会删除">
                            <a-icon type="question-circle" />
                        </a-tooltip>
                    </div>
                </a-card>
            </a-col>
        </a-row>
        <br />
        <a-table
            :columns="columns"
            :data-source="fetchers"
            row-key="name"
            :pagination="false"
            :bordered="true"
        >
            <span slot="enableTitle">
                是否启用
                <a-tooltip>
                    <template #title>
                        <span>
                            在禁用之后，将不会再运行该爬取器。
                        </span>
                    </template>
                    <a-icon type="question-circle" />
                </a-tooltip>
            </span>
            <template slot="enable" slot-scope="enable, record">
                <a-switch :default-checked="enable" @change="enableChange(record)" />
            </template>
        </a-table>
    </div>
</template>

<script>
import moment from 'moment';

const columns = [
    {
        title: '名称',
        dataIndex: 'name'
    },
    {
        title: '当前可用代理数量',
        dataIndex: 'validated_cnt'
    },
    {
        title: '总共爬取代理数量',
        dataIndex: 'sum_proxies_cnt'
    },
    {
        title: '上次爬取代理数量',
        dataIndex: 'last_proxies_cnt'
    },
    {
        title: '上次爬取时间',
        dataIndex: 'last_fetch_date',
        customRender: (date) => {
            return date ? moment(date).format('YYYY-MM-DD HH:mm:ss') : '';
        }
    },
    {
        dataIndex: 'enable',
        slots: { title: 'enableTitle' },
        scopedSlots: { customRender: 'enable' }
    }
];

// const data = [
//     {
//         name: '1',
//         enable: true,
//         sum_proxies_cnt: 308,
//         last_proxies_cnt: 20,
//         last_fetch_date: moment().toDate()
//     }
// ];

export default {
    data () {
        return {
            fetchers: [],
            columns,
            autoupdate: true,
            lastupdate: '',
            handle: null
        };
    },
    mounted () {
        this.handle = setInterval(() => {
            if (this.autoupdate) { this.update(); }
        }, 2000);
        this.update();
    },
    destroyed () {
        if (this.handle) { clearInterval(this.handle); }
        this.handle = null;
    },
    methods: {
        async update () {
            const data = await this.$http.get('/fetchers_status');
            this.fetchers = data.fetchers;
            this.lastupdate = moment().format('HH:mm:ss');
        },
        async clearStatus () {
            await this.$http.get('/clear_fetchers_status');
            this.$message.success('清空成功');
        },
        async enableChange (fetcher) {
            if (fetcher.enable) {
                await this.$http.get('/fetcher_enable', { name: fetcher.name, enable: '0' });
            } else {
                await this.$http.get('/fetcher_enable', { name: fetcher.name, enable: '1' });
            }
            this.$message.success('修改成功');
            await this.update();
        }
    }
};
</script>

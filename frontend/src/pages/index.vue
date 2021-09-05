<template>
    <div>
        <a-row :gutter="16">
            <a-col :span="4">
                <a-card :body-style="{padding: '20px 24px 14px'}">
                    <a-statistic
                        :value="sum_proxies_cnt"
                        :value-style="{ color: '#3f8600' }"
                        style="margin-right: 50px"
                    >
                        <template #title>
                            <span>
                                全部代理数量
                                <a-tooltip title="目前数据库中的代理总数，包含没有通过验证的代理">
                                    <a-icon type="question-circle" />
                                </a-tooltip>
                            </span>
                        </template>
                    </a-statistic>
                </a-card>
            </a-col>
            <a-col :span="4">
                <a-card :body-style="{padding: '20px 24px 14px'}">
                    <a-statistic
                        title="当前可用代理数量"
                        :value="validated_proxies_cnt"
                        :value-style="{ color: '#3f8600' }"
                        style="margin-right: 50px"
                    >
                    </a-statistic>
                </a-card>
            </a-col>
            <a-col :span="4">
                <a-card :body-style="{padding: '20px 24px 14px'}">
                    <a-statistic
                        :value="pending_proxies_cnt"
                        :value-style="{ color: '#3f8600' }"
                        style="margin-right: 50px"
                    >
                        <template #title>
                            <span>
                                等待验证代理数量
                                <a-tooltip>
                                    <template #title>
                                        <span>
                                            表示这些代理的`下次验证时间`已经到了，但是还没有完成验证。
                                            如果该数字突然增大，有可能是爬取器突然网数据库中添加了一批代理，是正常现象，慢慢等待即可。
                                            如果该数字一直较大，则表示验证器忙不过来了。
                                        </span>
                                    </template>
                                    <a-icon type="question-circle" />
                                </a-tooltip>
                            </span>
                        </template>
                    </a-statistic>
                </a-card>
            </a-col>
            <a-col :span="4">
                <a-card :body-style="{padding: '20px 24px 4px'}">
                    <p>
                        自动刷新:
                        <a-switch v-model="autoupdate" />
                    </p>
                    <p>刷新时间：{{ lastupdate }}</p>
                </a-card>
            </a-col>
        </a-row>
        <br />
        <a-table
            :columns="columns"
            :data-source="proxies"
            :row-key="(r) => `${r.protocol}://${r.ip}:${r.port}`"
            :bordered="true"
        >
            <span slot="to_validate_date">
                下次验证时间
                <a-tooltip>
                    <template #title>
                        <span>
                            验证器会不断从数据库中取出满足`下次验证时间`在当前时间之前的代理进行验证。
                        </span>
                    </template>
                    <a-icon type="question-circle" />
                </a-tooltip>
            </span>
            <span slot="latency" slot-scope="latency">
                <a-tag
                    :color="latency < 2000 ? 'green' : (latency < 4000 ? 'orange' : 'red')"
                >
                    {{ latency }}
                </a-tag>
            </span>
        </a-table>
    </div>
</template>

<script>
import moment from 'moment';

const columns = [
    {
        title: '来自',
        dataIndex: 'fetcher_name'
    },
    {
        title: '代理类型',
        dataIndex: 'protocol'
    },
    {
        title: 'IP',
        dataIndex: 'ip'
    },
    {
        title: '端口',
        dataIndex: 'port'
    },
    {
        title: '延迟',
        dataIndex: 'latency',
        scopedSlots: { customRender: 'latency' }
    },
    {
        title: '上次验证时间',
        dataIndex: 'validate_date',
        customRender: (date) => {
            return date ? moment(date).format('YYYY-MM-DD HH:mm:ss') : '';
        }
    },
    {
        dataIndex: 'to_validate_date',
        slots: { title: 'to_validate_date' },
        customRender: (date) => {
            return date ? moment(date).format('YYYY-MM-DD HH:mm:ss') : '';
        }
    }
];

// const data = [
//     {
//         fetcher_name: '1',
//         protocol: 'http',
//         ip: '127.0.0.1',
//         port: 308,
//         validated: true,
//         validate_date: moment().toDate(),
//         to_validate_date: moment().toDate(),
//         validate_failed_cnt: 0
//     }
// ];

export default {
    data () {
        return {
            columns,
            proxies: [],
            sum_proxies_cnt: 0,
            validated_proxies_cnt: 0,
            pending_proxies_cnt: 0,
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
            const data = await this.$http.get('/proxies_status');
            this.proxies = data.proxies;
            this.sum_proxies_cnt = data.sum_proxies_cnt;
            this.validated_proxies_cnt = data.validated_proxies_cnt;
            this.pending_proxies_cnt = data.pending_proxies_cnt;
            this.lastupdate = moment().format('HH:mm:ss');
        }
    }
};
</script>

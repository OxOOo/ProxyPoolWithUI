import axios from 'axios';
import { Modal } from 'ant-design-vue';

const baseURL = process.env.AXIOS_BASE_URL;

const instance = axios.create({
    baseURL,
    timeout: 10000,
    withCredentials: true
});

function showModel (type, title, content) {
    return new Promise((resolve) => {
        setTimeout(() => {
            Modal.destroyAll();
            Modal[type]({
                title,
                content,
                onOk: () => {
                    resolve();
                }
            });
        }, 500);
    });
}

function never () {
    return new Promise(() => {});
}

async function handle (req) {
    let data = {};
    try {
        const res = await req;
        data = res.data;
    } catch (e) {
        await showModel('error', '网络错误', e.message);
        // throw e; // IE上会弹出错误提示
        await never();
    }
    if (!data.success) {
        await showModel('info', '错误', data.message);
        // throw new Error(data.message);
        await never();
    }
    return data;
}

class Http {
    constructor () {
        this.baseURL = baseURL;
    }

    async get (url, params) {
        params = params || {};
        return await handle(instance.get(url, { params }));
    }

    async post (url, params, data) {
        params = params || {};
        data = data || {};
        return await handle(instance.post(url, data, { params }));
    }
}

export default ({ req }, inject) => {
    inject('http', new Http({ }));
};

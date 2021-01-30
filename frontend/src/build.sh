#!/bin/bash

set -e

cd `dirname $0`

rm -rf dist # 删除已经存在的目录
npm run generate # 生成静态文件

rm -rf ../deployment
mv dist ../deployment

echo 'Done.'

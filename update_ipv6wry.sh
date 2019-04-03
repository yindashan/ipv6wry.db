#!/bin/bash bash

# 变量定义
VERSION='0.0.1'
ZXINC_URL='http://ip.zxinc.org/'
ZXINC_IP_7Z='http://ip.zxinc.org/ip.7z'
TMP_DIR='/tmp'
USER_AGENT="UpdateBot@Rhilip/${VERSION}"

# 获得历史存档，并得到最后一个更新历史
max_history_version=0
for i in $(ls './history'); do
   test_version=$((${i} + 0))
   [[ ${test_version} -gt ${max_history_version} ]] && max_history_version=${test_version}
done

# 请求当前页面信息并获取更新日期
now_version=$(($(curl -L "${ZXINC_URL}" -H "User-Agent: ${USER_AGENT}"  | grep -E -o "下载IPv6地址数据库 \(版本[0-9]{8}" | grep -E -o "[0-9]{8}" ) + 0))

# 比较查看是否存在更新
if [[ ${now_version} -gt ${max_history_version} ]]; then
    # 下载数据包到临时目录并解压缩
    wget ${ZXINC_IP_7Z} -P "${TMP_DIR}"
    7z x "${TMP_DIR}/ip.7z" -y -o"${TMP_DIR}/ipv6_${now_version}"

    # 复制`ipv6wry.db`文件到 `history/{date}/`, `./`
    mkdir "./history/${now_version}"
    cp ${TMP_DIR}/ipv6_${now_version}/*.db "./history/${now_version}"
    rm ./*.db  # 移除当前目录下的`ipv6wry.db`
    cp ${TMP_DIR}/ipv6_${now_version}/*.db "./"

    # 获得更新信息
    db_count=$(cat "${TMP_DIR}/ipv6_${now_version}/说明.txt" | grep -E -o "IP数据记录：[0-9]*" | grep -E -o "[0-9]*")
    db_size=$(cat "${TMP_DIR}/ipv6_${now_version}/说明.txt" | grep -E -o "数据库大小：.*MiB" | sed "s/数据库大小：//g")

    # 更新历史 (README.md中的 IP数据记录 | 数据库大小 信息)
    sed -i "s/当前版本: \`[0-9]\{8\}\`/当前版本: \`${now_version}\`/g"  README.md
    sed -i "s/<\!-- update info here -->/| ${now_version} \| ${db_count} \| ${db_size} \| \n<\!-- update info here -->/" README.md

    # 清理临时文件
    rm -rf "${TMP_DIR}/ipv6_${now_version}"
    rm "${TMP_DIR}/ip.7z"

    # 提交更新
    DATE=`date +%Y-%m-%d`
    git add .
    git commit -a -m ":arrow_up: Daily update at $DATE"
    git push
fi


# ipv6wry.db

当前版本: `20190225`

`ipv6wry.db`是国内较为精确的IPv6地址库，据其官网 [IPv6地址查询网站](http://ip.zxinc.org/index.htm) 说明：

> 收集了包括中国电信、联通、移动、广电、长城宽带、教育网、科技网等运营商的最新准确 IPv6 地址数据，
 包括最新最全的世界各国国别数据。希望能够通过大家的共同努力打造一个没有未知数据，没有错误数据的IP数据库。
 IP数据库大概不定期更新一次，请大家不定期更新最新的IP数据库！

> 因为IP地址数据是民间收集的，运营商也会不时的更改IP段，所以有点遗漏、错误是难免的。
 随数据库附送IP解压、查询软件。假如发现IP地址有不对的，或想提供新的IP地址，
 请到ZX IP小秘书提供IP地址数据，或者QQ、邮件联系ZX，以便及时更新IP数据库。谢谢！
 
因为本人最近需要使用ipv6数据库，但遗憾的是，GitHub上对纯真ip数据库(`qqwry.dat`)有较多的自动更新脚本，
而该`ipv6wry.db`的关注度较少，没有，所以便准备自己造个轮子2333。

# 目录说明

 - `history/`: 历史数据，子目录以`YYYYMMDD`8位日期格式组织，可以从这里获取历史ip库文件
 - `parser/`: IPDB格式解析脚本，来自官网文件解压。目前包含`cpp`,`python`的解析方式
 - `ipv6wry.db`: 当前最新的IPDB格式数据库（**主文件，国内精确到县市**），用于其他软件获取最新ip库
 - `ipv6wry-country.db`: IPDB格式数据库（仅精确到国家），用于其他软件获取最新ip库
 - `update_ipv6wry.sh`: 自动更新脚本，可以用来自行集成获取ip库能力

# IPDB格式说明

```
文件头
0~3	字符串	"IPDB"
4~5	short	版本号,现在是2
6	byte	偏移地址长度(2~8)
7	byte	IP地址长度(4或8或12或16, 现在只支持4(ipv4)和8(ipv6))
8~15	int64	记录数
16~23	int64	索引区第一条记录的偏移
24	byte	地址字段数(1~255)[版本2新增,版本1是2]
25~31	reserve	保留,用00填充

记录区
array 字符串[地址字段数]
	与qqwry.dat大致相同,但是没有结束IP地址
	01开头的废弃不用
	02+偏移地址[偏移长度]表示重定向
	20~FF开头的为正常的字符串,采用UTF-8编码,00结尾

索引区
struct{
	IP[IP地址长度]	little endian, 开始IP地址
	偏移[偏移长度]	little endian, 记录偏移地址
}索引[记录数];
```

# 依赖安装

```bash
sudo apt-get install p7zip-full
```

# 更新历史

| 日期 | IP数据记录 | 数据库大小 |
| :--: | :--------: | :-------: |
| 20190225 | 104038 | 1.47MiB |
<!-- update info here -->

# License

本Repo采用`GPL-2.0`协议，具体请见 `LICENSE` 文件

以下为ZX IP地址数据库相关协议

```
本协议是用户（您）和ZX公司（zxinc.org）之间关于使用ZX IP地址数据库（本数据库）达成的协议。您安装或者使用本数据库的行为将视为对本协的接受及同意。除非您接受本协议，否则请勿下载、安装或使用本数据库，并请将本数据库从计算机中移除。

1. 本数据库是免费许可软件，不进行出售。你可以免费的复制，分发和传播本数据库，但您必须保证每一份复制、分发和传播都必须是未更改过的，完整和真实的。
2. 您作为个人使用本数据库。您只能对本数据库进行非商业性的应用。
3. 任何免费软件以及非商业性网站均可无偿使用本数据库，但在其说明上均应注明本数据库的名称和来源为“ZX IP地址数据库”。
4. 本数据库为免费共享软件。我们对本数据库产品不提供任何保证，不对任何用户因本数据库所遭遇到的任何理论上的或实际上的损失承担责任，不对用户使用本数据库造成的任何后果承担责任。
5. 本数据库所收集的信息，均是从网上收集而来。数据库只包含IP与其对应的地址，但是这些数据不会涉及您的个人信息，因此也不会侵害您的隐私。
6. 欢迎任何人为我们提供正确详尽的IP地址。可登录网站（http://ip.zxinc.org）或论坛（http://bbs.zxinc.org）提交正确的IP与地址，以便我们修正并提高本数据库IP地址数据的准确性。

		ZX公司（zxinc.org）版权所有，保留一切解释权利 !
```
# AnyData
## 准备
### 依赖：
Python： 3.6.8

Flask： 用于启用API

Pandas： 用于数据分析

最好弄个Python的venv在里面


### 配代码以及环境
```sh
git clone https://github.com/huchengbei/AnyData.git
cd AnyData
# 在Python环境或者虚拟环境中
pip install -r requirements.txt
```
在Python的环境中，执行
```
flask run
```
即可开启服务

## API介绍

### 加载数据
- 127.0.0.1:5000/load_data
#### method： POST
#### 请求参数
| 参数名 | 必选 | 类型 | 说明 |
|:---:|:---|:--|:--|
| path | true | str | 文件绝对路径 |
#### 返回结果示例
**示例**
  ```
  post: {
    path='G:/PycharmProjects/AnyData/resources/the_poors.csv'
  }
  return : 'success'
 ```

### 获取表格所有列名
- 127.0.0.1:5000/get_column_list
#### method： POST
#### 请求参数
| 参数名 | 必选 | 类型 | 说明 |
|:---:|:---|:--|:--|
| id | true | int | 表格id |
#### 返回结果示例
**示例**
  ```
  post: {
    id=0
  }
 ```
 return 
 ```json
 [
    "序号",
    "姓名",
    "人数",
    "民族",
]
 ```

### 设置主key
- 127.0.0.1:5000/set_main_key
#### method： POST
#### 请求参数
| 参数名 | 必选 | 类型 | 说明 |
|:---:|:---|:--|:--|
| id | true | int | 表格id |
| main_key | true | str | 主key |
#### 返回结果示例
**示例**
  ```
  post: {
    id=0，
    main_key='证件号码'
  }
  return：'success'


### 筛选
- 127.0.0.1:5000/funnel
#### method： POST
#### 请求参数--JSON
```json
"condition": [
  {
	  "id": 表格id,
		"exist": 存在为1， 不存在为0
	},
	{
	  "id": 表格id,
	  "exist": 存在为1， 不存在为0
	}
  ...
],
"start": 开始的索引,
"num": 返回数量
}
```
#### 请求示例
```json
{
	"condition": [
		{
			"id": 0,
			"exist": 1
		},
		{
			"id": 1,
			"exist": 0
		}
	],
	"start": 2,
	"num": 5
}
```
#### 返回结果示例
**示例**
```json
{
    "total": 2889,
    "next_start": 7,
    "column_list": [
        "证件号码",
        "姓名",
        "与户主关系"
    ],
    "data": {
        "123456789009870001": {
            "证件号码": "123456789009870001",
            "姓名": "AAA",
            "与户主关系": "配偶"
        },
        "123456789009870002": {
            "证件号码": "123456789009870002",
            "姓名": "BBB",
            "与户主关系": "配偶"
        },
        "123456789009870003": {
            "证件号码": "123456789009870003",
            "姓名": "CCC",
            "与户主关系": "配偶"
        },
        "123456789009870004": {
            "证件号码": "123456789009870004",
            "姓名": "DDD",
            "与户主关系": "配偶"
        },
        "123456789009870005": {
            "证件号码": "123456789009870005",
            "姓名": "EEE",
            "与户主关系": "之女"
        }
    }
  }
```

### 对比
- 127.0.0.1:5000/diff
#### method： POST
#### 请求参数--JSON
```json
"ids": [
  一系列id,
  ...
],
"start": 开始的索引,
"num": 返回数量
}
```
#### 请求示例
```json
{
	"ids": [
		0,
		1
	],
	"start": 2,
	"num": 5
}
```
#### 返回结果示例
**示例**
```json
{
    "total": 7,
    "next_start": 7,
    "column_list": [
        "证件号码",
        "姓名",
        "证件号码_对比",
        "姓名_对比"
    ],
    "data": {
        "123456789009870001": {
            "证件号码": "123456789009870001",
            "姓名": "AAA",
            "证件号码_对比": "123456789009870001",
            "姓名_对比": "AAB"
        },
        "123456789009870002": {
            "证件号码": "123456789009870002",
            "姓名": "BBC",
            "证件号码_对比": "123456789009870002",
            "姓名_对比": "BBC"
        },
        "123456789009870003": {
            "证件号码": "123456789009870003",
            "姓名": "CCD",
            "证件号码_对比": "123456789009870003",
            "姓名_对比": "CCD"
        },
        "123456789009870004": {
            "证件号码": "123456789009870004",
            "姓名": "DDE",
            "证件号码_对比": "123456789009870004",
            "姓名_对比": "DDE"
        },
        "123456789009870005": {
            "证件号码": "123456789009870005",
            "姓名": "EEF",
            "证件号码_对比": "123456789009870005",
            "姓名_对比": "EEF"
        }
    }
}
```
 

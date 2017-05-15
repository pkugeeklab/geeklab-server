## 说明

本文档用于说明极客实验室后端API。

## 用户

### Model

| 字段           | 类型     | 说明                      |
| ------------ | ------ | ----------------------- |
| name         | String | 用户名，唯一，不可更改，可用于登录       |
| nickname     | String | 昵称，可更改                  |
| email        | String | 邮箱，唯一，暂时不可更改，需要验证，可用于登录 |
| wechat       | String | 微信openID                |
| role         | String | 权限，"user"/"admin"       |
| isActive     | Bool   | 默认为False                |
| isAuthorized | Bool   | 默认为False                |
| createdAt    | Time   | 用户建立时间                  |
| updatedAt    | Time   | 信息更新时间                  |
| avatar       | String | 使用微信头像                  |

### API

##### POST /user/register

参数说明

分为两种

第一种，从微信入口进入，自带wechat openID

| 字段       | 类型     | 是否必须 |
| -------- | ------ | ---- |
| name     | String | 必须   |
| nickname | String | 必须   |
| email    | String | 必须   |
| wechat   | String | 必须   |
| url      | String | 必须   |

第二种，从网页入口进入，需要之后绑定微信（暂时不做）

##### POST /user/login

分为两种登录方式

第一种，从微信进入，由微信服务器鉴权，获得用户名和登录信息

| 字段     | 类型     | 是否必须 |
| ------ | ------ | ---- |
| wechat | String | 必须   |

第二种，直接以用户名/邮箱登录，通过@符号区分

| 字段       | 类型     | 是否必须 |
| -------- | ------ | ---- |
| username | String | 必须   |

以json形式返回内容

| 字段     | 类型     | 说明                                    |
| ------ | ------ | ------------------------------------- |
| token  | String | 格式为xxxx;ooo;tttt，随机字符串、用户id、过期时间以分号隔开 |
| avatar | String | 用户头像                                  |
| error  | String | 如果有错误则返回此字段，否则不返回                     |

##### POST /user/logout (Login required)

退出所有以该用户登录的帐号。

| 字段    | 类型     | 是否必须 |
| ----- | ------ | ---- |
| token | String | 必须   |

以json形式返回内容，如果正常退出，则返回{}

| 字段    | 类型     | 说明                |
| ----- | ------ | ----------------- |
| error | String | 如果有错误则返回此字段，否则不返回 |

# 表单提交

## 活动预约

##### POST /apply/activity

提交预约信息

| 字段         | 类型     | 说明                                       |
| ---------- | ------ | ---------------------------------------- |
| title      | String | 活动标题                                     |
| people     | String | 参与活动人数                                   |
| username   | String | 姓名                                       |
| department | String | 院系                                       |
| telephone  | String | 电话                                       |
| email      | String | 电子邮件                                     |
| starttime  | String | 开始时间，格式为YYYY-MM-DD-HH-mm                 |
| stoptime   | String | 结束时间，格式为YYYY-MM-DD-HH-mm                 |
| desc       | String | 活动描述                                     |
| additional | String | 补充说明                                     |
| items      | String | 需要借的物品，选填，在列表['exp', 'speech', 'desk', 'projector', 'board', 'tv']中，以'-'连接 |

以json形式返回内容，如果正常退出，则返回{}

| 字段    | 类型     | 说明                                |
| ----- | ------ | --------------------------------- |
| error | Object | 如果有错误则返回此字段，否则不返回；错误格式为{字段: 错误类型} |
| ok    | Object | 成功提交则返回次字段，格式为{pdfid: xxxxx}      |

## 查询预约

##### GET /query/\<pdfid\>

| 字段    | 类型     | 说明                           |
| ----- | ------ | ---------------------------- |
| error | String | 如果有错误则返回此字段，否则不返回            |
| ok    | Object | 成功提交则返回次字段，格式为{pdfid: xxxxx} |

## 获取文件地址

##### GET /get-pdf/\<pdfid>

直接返回文件


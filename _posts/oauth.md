---
title: OAuth详细解读
date: 2016-02-29 16:07:14
tags:
 - oauth
---

本文包含OAuth协议的形象化描述，包括各个阶段请求的细节，包括参数解释（state, nonce, timestamp等）

来自维基百科:[OAuth](https://zh.wikipedia.org/wiki/OAuth)
>OAuth（开放授权）是一个开放标准，允许用户让第三方应用访问该用户在某一网站上存储的私密的资源（如照片，视频，联系人列表），而无需将用户名和密码提供给第三方应用

![oauth-flow](/images/oauth-flow.png)

OAuth协议的参与方：
> Google Resource Server是RS(Resource Server)，保存了client希望获得的资源（这里是用户在Google的消息流）

>Google Authorization Server是AS（Authorization Server），即授权服务器。Client访问RS，需要得到AS的授权凭证（即access token）

>Facebook是Client，希望得到Alice的同意，来访问其在Google的资源（即Alice的消息流）

>Alice 是Resource Owner(资源所有者)。


步骤解读：
(1)Facebook在自己的网页上放置一个链接，地址是 accounts.google.com/o/oauth2/oauth....用户单击后，跳转到Google AS页面（也可能是弹窗），注意带上了以下参数：

>redirect_uri:用户授权后，返回的Facebook页面

>client_id: Facebook在Google侧注册的client_id，Facebook还保存有对应的client_secret。后面会用到。

>state: Client的会话Id，不同的用户在Facebook点击上文的链接，产生不同的state字符串。防止恶意用户伪造一个URL，诱导其他用户去点击。即CSRF（cross site request forgery跨站请求伪造）攻击。详见:[跨站请求伪造](https://zh.wikipedia.org/wiki/%E8%B7%A8%E7%AB%99%E8%AF%B7%E6%B1%82%E4%BC%AA%E9%80%A0)

>response_type: 一般是code，表示 Authorization_code，即授权码

>scope: 资源类型，这里指用户的消息流

（2）（3）用户在Google的页面，同意了Facebook获取消息流的请求。当然如果用户没有在Google登录，则需要先登录。之后，Google通过302返回码，引导Alice的浏览器，访问 www.facebook.com/?code=xx&state=xx，参数说明：

>code: 即 Authorization_code用户的授权码，表示facebook已经得到用户的授权。

> state: 即步骤1中，facebook生成的state， google AS原样返回

（4）(5)步骤2的请求到了Facebook后台，Facebook后台向google AS发起了一个获取 access_token的请求，包含过期时间等信息。注意这次不是通过Alice的浏览器了。参数说明：

>code: 即步骤2得到的用户授权码。

>redirect_uri: 即步骤1的跳转url。这个仅作校验之用。

> client_id & client_secret: Facebook在Google AS注册得到的凭证

>grant_type：授权类型。往往由AS设置的固定值。

(6) 经过了以上步骤，终于，Facebook可以问google的RS请求用户Alice的消息流了。回顾一下，首先，通过 Authorization_code的方式，Facebook首先得到了Alice的许可。然后通过 access_token的方式，Facebook又得到了Google AS的许可（提供了 Authorization_code以及 client_id, client_secret）。

在更复杂的实现中，为了防止请求重放攻击，在有些请求的参数中，又加入了nonce和timestamp：

> nonce: 即 number [used only] once，就是只能用一次的随机数。可以有效防止重复攻击。但服务器端要记住所有已经用过的nonce，这对服务器来说，是个不小的负担。

> timestamp: 时间戳，一般只从1970年开始的毫秒数。和 nonce一起用，用于减轻服务器保存nonce的负担。服务器端会保留一个较旧的 timestamp_start，如果请求中的 timestamp 比 timestamp_start 还小，服务器直接拒绝请求，因为更早的nonce列表被服务器删除了，无法校验是否重复。


### 参考
[帮你深入理解OAuth2.0协议](http://blog.csdn.net/seccloud/article/details/8192707)
[oauth core 1.0 - nonce](http://oauth.net/core/1.0/#nonce)

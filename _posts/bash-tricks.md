---
title: Bash技巧
date: 2016-03-01 11:07:14
tags:
 - linux
 - bash
---

### 多个git帐号，多个ssh私钥

1. 用 ssh-keygen -f [用户名] 在某个目录下生成公钥和私钥文件
2. 在 ~/.ssh/config 文件中，增加如下内容：

{% codeblock lang:shell %}

host github.com
 HostName github.com
 IdentityFile ~/.ssh/id_rsa_github
 User git

{% endcodeblock %}


### 设置成 VIM 编辑格式

{% codeblock lang:shell %}

set -o vi

{% endcodeblock %}

### 指定帐号免登录

场景是，我有多台目标Linux机器，每个登录账户不同。
{% codeblock lang:shell %}

ssh-keygen -t rsa -f bob

{% endcodeblock %}
将在当前目录下，生成 bob, bob.pub两个文件。将 bob.pub的内容，贴到目标机器的 .ssh/authorized_keys 中。
登录时，指定 bob 私钥文件的路径即可：
{% codeblock lang:shell %}

ssh -i ./bob bob@host

{% endcodeblock %}
可选，用 ssh -v .. 调试可能出现的问题。

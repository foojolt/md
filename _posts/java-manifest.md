---
title: Java的Manifest文件
date: 2016-03-01 10:07:14
tags:
 - java
 - manifest
---

### Manifest文件的作用
Manifest，英文是货物清单。在Java中，每个jar包可以包含这么一个清单文件：META-INF/MANIFEST.MF

参考 [Working with Manifest Files: The Basics](https://docs.oracle.com/javase/tutorial/deployment/jar/manifestindex.html)

上面的链接中，提到了几种用法：
* 设置程序入口
* 设置classpath
* 密封某一个包 （seal package）
* Java Applet&Web Start 安全配置

### 设置classpath
这个一般是用不着的。只有在classpath太长，比如大于Linux命令行的最大长度，这样java命令就无法执行了。这时可以在 META-INF/MANIFEST.MF 中添加

{% codeblock lang:java %}
Class-Path: jar1-name jar2-name directory-name/jar3-name
{% endcodeblock %}

### 密封一个包
密封一个包的意思是，假如你提供了一个tool.jar包，包含一个类com.foo.tool.BigTool，你不希望别人的代码中，使用同样的包名 com.foo.tool，可以这样做：
{% codeblock lang:java %}
Name: com/foo/tool
Sealed: true
{% endcodeblock %}
效果是： 让JVM只能从tool.jar加载com.foo.tool包

### 更新Manifest文件

可以用一下命令获取一个jar包的manifest文件：

{% codeblock lang:shell %}
jar xvf foo.jar META-INF/MANIFEST.MF
{% endcodeblock %}

用文本编辑器修改后，update到jar包中：

{% codeblock lang:shell %}
jar uvf foo.jar META-INF/MANIFEST.MF
{% endcodeblock %}

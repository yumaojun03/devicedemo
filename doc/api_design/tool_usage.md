# api-blueprint 工具简介

## 概述

 API Blueprint是一套API描述标准，和Markdown一样，属于一种标记语言，可以把标记文稿转换成漂亮的接口文档，由于采用了MarkDown语法，比RAML更容易上手，
 而且有良好的生态支持，比如编辑器插件支持，渲染工具，mock工具，测试工具，等...

 关于其文档说明，简要的可以参考[使用 API-Blueprint 编写 API 文档](http://www.jianshu.com/p/d39c3553e25a), 
 而更详细的文档请查考[API Blueprint官方文档](https://apiblueprint.org/documentation/specification.html)


## 编辑器选择

  在官方的工具列表里面有很多插件可以选择，具体参考[编辑器列表](https://apiblueprint.org/tools.html#editors), 这里推荐使用vscode作为编辑器，
  在vscode里面搜索API Elements  就可以找到对于的插件安装即可，关于该插件的介绍请产考[vscdoe apielements插件地址](https://github.com/XVincentX/vscode-apielements)
  
  将你的文件保存成 apib结尾的文件，编辑器讲自动帮你完成，语法分析。该插件和apiary做了很多绑定，可以直接在线预览，具体请查看该插件的命令列表，
  也可以使用编辑器进行编辑完成后，在apiary上完成后面的 preview-mock-test。

## 语法学习

  学习 API Blueprint Language 非常简单, 只要你有用 markdown 写过东西, 那你一定能快速的掌握它.
  
  1. 首先, 简单过一遍官方的[指导手册](https://apiblueprint.org/documentation/)
  
  2. 查看官方提供的例子 . 一共也就 [10](https://github.com/apiaryio/api-blueprint/tree/master/examples) 多个, 耐心看完. 心里就大概有数了.
  
  3. 然后可以看一下 [语法规范](https://github.com/apiaryio/api-blueprint/blob/master/API%20Blueprint%20Specification.md) , 当前的稳定版本是 1A9。

  官方的解释器 是完全支持 1A9 格式的。而且官方有多种语言的解释器，具体请参考[解释器列表](https://apiblueprint.org/tools.html#parsers)
  ， 有了这个解析器，就可以很容易的扩展自己的相关工具了（比如代码生成等）。


## 例子

#### 编写设计文档

#### 生成HTML格式的文档

#### 模拟服务端

#### 客户端测试
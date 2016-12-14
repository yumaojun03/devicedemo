# swagger 工具简介

 swagger是一个RESTful API 的设计工具，官方提供3种工具：
 1. swagger-editor 在线编辑器，同时提供编辑-展现-客户端-服务端代码的生成
 2. swagger-ui 展示工具，将编辑器定义好的json描述文件友好展示的工具。
 3. swagger-codegen 生成服务端和客户端的代码。
 
因为swagger-editor集成了swagger-codegen功能，因此我们仅需要使用swagger-editor和
swagger-ui就够了。
 
## 编辑器(editor)

  可以使用在线编辑器，同时这个在线编辑器也可以本地部署，这里说明如何本地部署，
  部署完后，就可以基于本地的编辑器 编写 api的设计文档。
  
#### 部署本地编辑器
  
   安装docker，配置镜像加速，然后拉去镜像到本地运行
   
```
docker pull swaggerapi/swagger-editor
docker run -p 80:8080 swaggerapi/swagger-editor
```

#### 使用本地编辑器
  推荐使用vscode作为编辑器, 安装vscode的 Swagger View插件 就可以打造一个 swagger的编辑器了
  采用yaml编写，然后使用Swagger Preview 查看预览。
  
#### swagger2.0语法
    
  详情参考[swagger2.0官方规范](http://swagger.io/specification/)
  
  + 格式
  
    采用json， 因为yaml是json的一个超集，因此也可以使用。通常情况我们通过yaml来完成编辑，
    最后通过编辑器导出为json文件。
    
  + 文件结构
    
    为一个单独的文件，但是其中definitions部分可以被抽出来为一个独立文件，通过$ref进行引用，
    按照惯例，这个文件应该被命名为 swagger.json
    
  + 数据类型
  
    用于描述一个数据的数据类型，对象定义时使用。

|Common Name |type     |format   |Comments                                         |
| ---------- | :-----: | :-----: | ----------------------------------------------: |
|integer     |integer  |int32    |signed 32 bits                                   |
|long	     |integer  |int64	 |signed 64 bits                                   |
|float	     |number   |float	 |                                                 |
|double	     |number   |double	 |                                                 |
|string	     |string   |	     |                                                 |
|byte	     |string   |byte	 |base64 encoded characters                        |
|binary	     |string   |binary	 |any sequence of octets                           |
|boolean     |boolean  |	     |                                                 |
|date	     |string   |date	 |As defined by full-date - RFC3339                |
|dateTime    |string   |date-time|As defined by date-time - RFC3339                |
|password    |string   |password |Used to hint UIs the input needs to be obscured. |

  + 规范
  
  规范也就是语法，会安装此规范来编写API设计文档。以下列出了所有需要的关键字段

| 字段名      | 类型	     |  描述    
| ---------- | :-------: | ------:  
|swagger	 |string	 |必填项。表示使用的swagger的版本，必须为2.0
|info	     |[Info Object](http://swagger.io/specification/#infoObject)|必填项。提供API的一些元数据描述
|host	     |string	 |提供该API服务的主机名称或者IP，测试时 使用该地址进程测试。
|basePath	 |string	 |API的基本路径,这是相对的host。 如果不包括,API是直属host。 必须以"/"开头
|schemes	 |[string]   |API的传输协议的列表。 在"http","https","ws","wss"其中选择
|consumes	 |[string]   |一个MIME类型的api可以使用列表。 值必须是所描述的Mime类型
|produces	 |[string]   |MIME类型的api可以产生的列表。   值必须是所描述的Mime类型
|paths  	 |[路径对象](http://swagger.io/specification/#pathsObject)	 |必填项。可用的路径和操作的API
|definitions |[定义对象](http://swagger.io/specification/#definitionsObject)	 |一个对象数据类型定义
|parameters	 |[参数定义对象](http://swagger.io/specification/#parametersDefinitionsObject) | 定义请求参数的对象
|responses	 |[反应定义对象](http://swagger.io/specification/#responsesDefinitionsObject) | 定义请求响应对象
|securityDefinitions |[安全定义对象](http://swagger.io/specification/#securityDefinitionsObject)|	安全方案定义规范,比如认证
|security	 |[安全需求对象](http://swagger.io/specification/#securityRequirementObject) | 这里主要指使用哪种认证手段
|tags	     |[标签对象](http://swagger.io/specification/#tagObject)    | 没个RESTful中资源的标签，列表中的每个标记名称必须是唯一的
|externalDocs|[外部文档对象](http://swagger.io/specification/#externalDocumentationObject) |	额外的外部文档, 指向外部url
    

## 渲染器(ui)

  渲染器使用官方的swagger-ui，这里我们需要一个web服务器，用来渲染我们刚才编辑
  完成的api 设计文档。这里一般使用node 的 express为web框架来做这个简单的web服务器
  
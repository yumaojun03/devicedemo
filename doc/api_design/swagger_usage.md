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
  
#### swagger2.0语法
    
  详情参考[swagger2.0官方规范](http://swagger.io/specification/)
  
  + 格式
  
    采用json， 因为yaml是json的一个超集，因此也可以使用。通常情况我们通过yaml来完成编辑，
    最后通过编辑器导出为json文件。
    
  + 文件结构
    
    为一个单独的文件，但是其中
    
  + 数据结构


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
    

## 渲染器(ui)

  渲染器使用官方的swagger-ui，这里我们需要一个web服务器，用来渲染我们刚才编辑
  完成的api 设计文档。这里一般使用node 的 express为web框架来做这个简单的web服务器
  
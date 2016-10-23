# API 设计
> ROOT_URL /api/news/
## 目录相关api
>ROOT_URL /menu/
>URL /api/news/menu/
### 获取目录
>请求URL /api/news/menu/

>方法 GET

    获取所有目录
---
### 获取指定目录
>请求URL /api/news/menu/<id>/

>方法 GET

    获取指定目录，如未发现则返回404

### 添加目录
>请求URL /api/news/menu/<id>/child/

>方法 POST {name:string}

    添加目录,parent为目录ID
    如无parent参数，且用户为管理员，则添加为根目录，否则返回403
    如有parent参数，且用户具有父目录管理权限，则添加目录，返回目录详细，否则返回403
    
### 添加目录管理员
>请求URL /api/news/menu/<id>/administrators/
>方法 POST {person:number}

    添加目录管理员
    仅目录的拥有者有权添加
    如无parent参数，且用户为管理员，则添加为根目录，否则返回403
    如有parent参数，且用户具有父目录管理权限，则添加目录，返回目录详细，否则返回403
    
### 删除目录管理员
>请求URL /api/news/menu/<id>/administrators/<id>/
>方法 DELETE {person:number}

    删除目录管理员
    仅目录的拥有者有权添加
    如无parent参数，且用户为管理员，则添加为根目录，否则返回403
    如有parent参数，且用户具有父目录管理权限，则添加目录，返回目录详细，否则返回403

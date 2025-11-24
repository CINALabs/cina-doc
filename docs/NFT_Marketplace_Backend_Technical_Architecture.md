# NFT 市场后端 - 技术架构文档

## 1. 概述

`digital-fund-backend` 是一个使用 Go 语言编写的高性能后端服务，专为 NFT 市场或聚合器提供 API 支持。它采用了经典的分层架构，实现了业务逻辑、数据访问和 API 接口的清晰分离。

## 2. 技术栈

*   **开发语言:** [Go](https://go.dev/) (版本 1.24+)
*   **Web 框架:** [Gin](https://github.com/gin-gonic/gin) - 一个轻量级、高性能的 Go Web 框架。
*   **数据库 ORM:** [GORM](https://gorm.io/) - Go 语言领域功能最全面的 ORM 库之一。
*   **数据库:** [MySQL](https://www.mysql.com/) (通过 GORM 的 MySQL 驱动连接)。
*   **配置管理:** [Viper](https://github.com/spf13/viper) - 用于处理复杂的配置文件和环境变量。
*   **日志:** [Zap](https://github.com/uber-go/zap) - Uber 出品的高性能结构化日志库。
*   **API 文档生成:** [Swaggo](https://github.com/swaggo/swag) - 通过解析代码注释自动生成 Swagger/OpenAPI 文档。
*   **本地依赖:** 项目依赖于一个本地的共享库 `digital-fund-base`，用于存放跨项目复用的代码。

## 3. 项目结构与分层

项目采用了清晰的、关注点分离的分层架构。

```
src/
├── main.go       # 应用主入口，负责初始化和启动服务
├── api/          # API 接口层
│   ├── router/   # Gin 路由的定义
│   ├── v1/       # v1 版本 API 的请求处理器 (Handler)
│   └── middleware/ # Gin 的中间件 (如认证、缓存)
├── service/      # 业务逻辑层，处理核心业务流程
├── dao/          # 数据访问层，负责与数据库进行增删改查 (CRUD)
├── config/       # 配置文件的加载与管理
├── types/        # Go 的结构体定义，特别是 API 的请求和响应体
├── errcode/      # 自定义错误码
└── docs/         # Swaggo 生成的 Swagger 文档
```

### 3.1. `digital-fund-base` 共享库

*   `go.mod` 文件中的 `replace` 指令表明此项目依赖于一个本地的 `digital-fund-base` 仓库。
*   这个共享库的作用是存放多个后端服务（如果存在的话）之间可以复用的代码，例如：
    *   **GORM 模型定义:** 所有数据库表的 Go 结构体。
    *   **区块链工具:** 与 `go-ethereum` 交互的通用函数。
    *   **通用错误码和工具函数。**

## 4. 核心架构与数据流

一个典型的 API 请求会经过以下处理流程：

1.  **路由与中间件 (`api/router`, `api/middleware`):**
    *   用户的 HTTP 请求首先到达 Gin 引擎。
    *   Gin 引擎根据 `api/router/v1.go` 中定义的路由表，将请求匹配到对应的处理器。
    *   在到达处理器之前，请求会经过必要的中间件，例如 `AuthMiddleWare` 会检查请求头中的 Token 以验证用户身份，`CacheApi` 会尝试从缓存中直接返回响应。

2.  **API 处理器 (`api/v1`):**
    *   处理器（Handler）函数负责解析和校验请求。
    *   它会从 URL 路径、查询参数或请求体中提取数据，并将其绑定到 `types` 中定义的 Go 结构体上。
    *   处理器本身不包含复杂的业务逻辑，它的职责是调用 `service` 层的相应函数来处理请求。

3.  **业务逻辑层 (`service`):**
    *   `service` 层是业务逻辑的核心。它负责执行具体的任务，例如“获取一个 NFT 集合的详细信息及其最新的出价”。
    *   一个 service 函数可能会协调多个 `dao` 层函数。例如，它可能需要先从 `collections_dao` 获取集合信息，再从 `bids_dao` 获取出价信息。
    *   它也可能包含与区块链节点交互的逻辑（通过 `go-ethereum`），或者调用其他微服务。

4.  **数据访问层 (`dao`):**
    *   `dao` 层是唯一与数据库直接交互的层。
    *   它使用 GORM 来执行 SQL 查询。每个 `dao` 文件通常对应一个数据库表，并提供对该表的增、删、改、查方法。
    *   这种分层确保了业务逻辑与数据存储的解耦，未来如果需要从 MySQL 迁移到其他数据库，主要修改的将是 `dao` 层。

5.  **响应返回:**
    *   `service` 层将处理结果返回给 `api` 处理器。
    *   处理器将 Go 结构体序列化为 JSON 格式，并将其作为 HTTP 响应返回给客户端。

## 5. 数据库

*   项目使用 GORM 作为 ORM，这使得数据库操作更加便捷和安全，可以有效防止 SQL 注入。
*   数据库模型（表的结构体定义）很可能位于共享的 `digital-fund-base` 仓库中，以便在多个服务间复用。
*   使用的数据库是 MySQL。

## 6. 总结

`digital-fund-backend` 是一个遵循了现代 Go 开发实践的、健壮的 API 服务。其分层架构、对 ORM 和 Swagger 的使用，都表明了项目在设计时充分考虑了可维护性、可扩展性和开发效率。

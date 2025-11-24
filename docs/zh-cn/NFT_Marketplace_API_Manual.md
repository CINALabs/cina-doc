# NFT 市场后端 API - 接口文档

## 1. 概述

本文档定义了 NFT 市场后端的 API 接口。该后端服务使用 Go 语言和 Gin 框架构建，旨在为一个或多个前端应用提供获取 NFT 市场数据、查询用户资产和处理用户认证等功能。

所有接口的根路径为 `/api/v1`。

## 2. 认证

部分接口需要用户认证。认证流程如下：
1.  前端请求 `GET /user/{address}/login-message` 获取一段用于签名的随机文本。
2.  用户使用其钱包对该文本进行签名。
3.  前端将用户地址和签名结果提交到 `POST /user/login`。
4.  后端验证签名，如果成功，则为该用户生成一个 JWT (JSON Web Token) 或 Session，并在后续请求的 `Authorization` 头中携带。
5.  需要认证的接口会使用 `AuthMiddleWare` 中间件进行校验。

## 3. API 接口详情

### 3.1. 用户 (User)

*   **`GET /user/:address/login-message`**
    *   **功能:** 获取用户登录所需的签名信息。
    *   **路径参数:** `:address` - 用户的钱包地址。
    *   **返回:** `{ "message": "Welcome to..." }`

*   **`POST /user/login`**
    *   **功能:** 用户使用签名进行登录。
    *   **请求体:** `{ "address": "...", "signature": "..." }`
    *   **返回:** 登录成功后的 Token 或 Session 信息。

*   **`GET /user/:address/sig-status`**
    *   **功能:** 获取用户的签名状态（可能用于检查是否需要重新登录）。
    *   **路径参数:** `:address` - 用户的钱包地址。

### 3.2. NFT 集合 (Collections)

*   **`GET /collections/ranking`**
    *   **功能:** 获取 NFT 集合的排名信息，可能按交易量或市值排序。
    *   **中间件:** 结果会被缓存60秒。

*   **`GET /collections/:address`**
    *   **功能:** 获取指定 NFT 集合的详细信息。
    *   **路径参数:** `:address` - NFT 合约地址。

*   **`GET /collections/:address/items`**
    *   **功能:** 获取指定 NFT 集合下的所有 NFT (items) 列表。
    *   **路径参数:** `:address` - NFT 合约地址。

*   **`GET /collections/:address/bids`**
    *   **功能:** 获取对指定 NFT 集合的所有出价（Collection-level bids）。
    *   **路径参数:** `:address` - NFT 合约地址。

*   **`GET /collections/:address/history-sales`**
    *   **功能:** 获取指定 NFT 集合的历史销售记录。
    *   **路径参数:** `:address` - NFT 合约地址。

### 3.3. NFT 单品 (Items)

*   **`GET /collections/:address/:token_id`**
    *   **功能:** 获取单个 NFT 的详细信息。
    *   **路径参数:** `:address` - NFT 合约地址, `:token_id` - NFT 的 Token ID。

*   **`GET /collections/:address/:token_id/bids`**
    *   **功能:** 获取对单个 NFT 的所有出价。

*   **`GET /collections/:address/:token_id/owner`**
    *   **功能:** 获取单个 NFT 的当前所有者。

*   **`POST /collections/:address/:token_id/metadata`**
    *   **功能:** 请求后端刷新该 NFT 的元数据。

### 3.4. 用户资产 (Portfolio)

**注意:** 此组接口需要用户认证。

*   **`GET /portfolio/collections`**
    *   **功能:** 获取当前登录用户所拥有的所有 NFT 集合的列表。

*   **`GET /portfolio/items`**
    *   **功能:** 获取当前登录用户所拥有的所有 NFT 单品。

*   **`GET /portfolio/listings`**
    *   **功能:** 查询当前登录用户正在挂单出售的 NFT。

*   **`GET /portfolio/bids`**
    *   **功能:** 查询当前登录用户的所有有效出价。

### 3.5. 市场活动 (Activities)

*   **`GET /activities`**
    *   **功能:** 获取跨链的市场活动信息（如挂单、成交、出价等）。

### 3.6. 拍卖 (Auctions)

*   **`GET /auctions`**
    *   **功能:** 批量查询拍卖信息。

*   **`GET /auctions/detail`**
    *   **功能:** 查询单个拍卖的详细信息。
    *   **查询参数:** `?id=...`

### 3.7. 文件上传 (Upload)

*   **`POST /uploadFile/uploadNftFile`**
    *   **功能:** 上传文件，可能用于创建 NFT 时的图片或元数据上传。

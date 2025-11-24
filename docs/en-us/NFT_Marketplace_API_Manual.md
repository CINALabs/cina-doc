# NFT Marketplace Backend API - Interface Document

## 1. Overview

This document defines the API interfaces for the NFT Marketplace backend. This backend service is built using the Go language and Gin framework, aiming to provide functions such as fetching NFT market data, querying user assets, and handling user authentication for one or more frontend applications.

The root path for all interfaces is `/api/v1`.

## 2. Authentication

Some interfaces require user authentication. The authentication flow is as follows:
1.  Frontend requests `GET /user/{address}/login-message` to get a random text string for signing.
2.  User signs this text using their wallet.
3.  Frontend submits the user address and signature result to `POST /user/login`.
4.  Backend verifies the signature. If successful, it generates a JWT (JSON Web Token) or Session for the user, which is carried in the `Authorization` header of subsequent requests.
5.  Interfaces requiring authentication will be verified by the `AuthMiddleWare` middleware.

## 3. API Details

### 3.1. User

*   **`GET /user/:address/login-message`**
    *   **Function:** Get the signing message required for user login.
    *   **Path Params:** `:address` - User's wallet address.
    *   **Returns:** `{ "message": "Welcome to..." }`

*   **`POST /user/login`**
    *   **Function:** User logs in using signature.
    *   **Request Body:** `{ "address": "...", "signature": "..." }`
    *   **Returns:** Token or Session info after successful login.

*   **`GET /user/:address/sig-status`**
    *   **Function:** Get user's signature status (possibly used to check if re-login is needed).
    *   **Path Params:** `:address` - User's wallet address.

### 3.2. Collections

*   **`GET /collections/ranking`**
    *   **Function:** Get ranking information of NFT collections, possibly sorted by volume or market cap.
    *   **Middleware:** Result is cached for 60 seconds.

*   **`GET /collections/:address`**
    *   **Function:** Get detailed information of a specific NFT collection.
    *   **Path Params:** `:address` - NFT contract address.

*   **`GET /collections/:address/items`**
    *   **Function:** Get the list of all NFTs (items) under a specific NFT collection.
    *   **Path Params:** `:address` - NFT contract address.

*   **`GET /collections/:address/bids`**
    *   **Function:** Get all bids for a specific NFT collection (Collection-level bids).
    *   **Path Params:** `:address` - NFT contract address.

*   **`GET /collections/:address/history-sales`**
    *   **Function:** Get historical sales records of a specific NFT collection.
    *   **Path Params:** `:address` - NFT contract address.

### 3.3. Items

*   **`GET /collections/:address/:token_id`**
    *   **Function:** Get detailed information of a single NFT.
    *   **Path Params:** `:address` - NFT contract address, `:token_id` - Token ID of the NFT.

*   **`GET /collections/:address/:token_id/bids`**
    *   **Function:** Get all bids for a single NFT.

*   **`GET /collections/:address/:token_id/owner`**
    *   **Function:** Get the current owner of a single NFT.

*   **`POST /collections/:address/:token_id/metadata`**
    *   **Function:** Request backend to refresh metadata for this NFT.

### 3.4. Portfolio

**Note:** This group of interfaces requires user authentication.

*   **`GET /portfolio/collections`**
    *   **Function:** Get the list of all NFT collections owned by the currently logged-in user.

*   **`GET /portfolio/items`**
    *   **Function:** Get all NFT items owned by the currently logged-in user.

*   **`GET /portfolio/listings`**
    *   **Function:** Query NFTs currently listed for sale by the logged-in user.

*   **`GET /portfolio/bids`**
    *   **Function:** Query all active bids of the logged-in user.

### 3.5. Activities

*   **`GET /activities`**
    *   **Function:** Get cross-chain market activity information (such as listings, sales, bids, etc.).

### 3.6. Auctions

*   **`GET /auctions`**
    *   **Function:** Batch query auction information.

*   **`GET /auctions/detail`**
    *   **Function:** Query detailed information of a single auction.
    *   **Query Params:** `?id=...`

### 3.7. Upload

*   **`POST /uploadFile/uploadNftFile`**
    *   **Function:** Upload file, possibly used for uploading images or metadata when creating NFTs.

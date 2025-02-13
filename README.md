# BBC News Crawler
# BBC 新聞爬蟲

A Python-based web crawler that periodically scrapes interesting news from BBC's website and stores them in a SQLite database.

這是一個基於 Python 的網路爬蟲，定期從 BBC 網站抓取有趣的新聞並存儲在 SQLite 資料庫中。

## Features 功能特點

- Periodic news crawling from BBC website
- SQLite database storage
- Configurable crawling intervals
- News categorization and filtering
- Development container support for VS Code
- Web-based database management interface

- 定期從 BBC 網站爬取新聞
- SQLite 資料庫儲存
- 可配置的爬取間隔
- 新聞分類和過濾
- VS Code 開發容器支援
- 網頁版資料庫管理介面

## Deployment 部署

### Quick Start 快速開始

The easiest way to deploy is using Docker Compose:
最簡單的部署方式是使用 Docker Compose：

```bash
# Clone the repository 克隆儲存庫
git clone <repository-url>
cd bbc-news-crawler

# Start the services 啟動服務
docker-compose up -d

# View logs 查看日誌
docker-compose logs -f crawler
```

The crawler will start automatically and run every 60 minutes. You can access the database management interface at http://localhost:8080

爬蟲會自動啟動並每 60 分鐘運行一次。你可以在 http://localhost:8080 存取資料庫管理介面。

### Environment Variables 環境變數

You can configure the crawler by editing the `docker-compose.yml` file:
你可以通過編輯 `docker-compose.yml` 檔案來配置爬蟲：

```yaml
environment:
  - CRAWL_INTERVAL=10  # Crawling interval in minutes 爬取間隔（分鐘）
  - DB_PATH=/app/data/news.db  # Database path 資料庫路徑
```

### Managing the Deployment 管理部署

```bash
# Stop the services 停止服務
docker-compose down

# View service status 查看服務狀態
docker-compose ps

# View crawler logs 查看爬蟲日誌
docker-compose logs -f crawler

# Restart services 重啟服務
docker-compose restart

# Update and rebuild 更新並重建
git pull
docker-compose up -d --build
```

### Database Management 資料庫管理

The project includes a web-based SQLite database browser for easy data viewing and management.
專案包含一個網頁版的 SQLite 資料庫瀏覽器，方便查看和管理資料。

1. Access the web interface at http://localhost:8080
   在 http://localhost:8080 存取網頁介面

2. Features available in the interface:
   網頁介面提供的功能：
   - Browse and search news articles 瀏覽和搜尋新聞文章
   - View table structure 查看資料表結構
   - Execute custom SQL queries 執行自定義 SQL 查詢
   - Export data 匯出資料
   - View database statistics 查看資料庫統計

Example queries you can try:
你可以嘗試的查詢範例：

```sql
-- Get latest news
SELECT title, category, published_date 
FROM news 
ORDER BY published_date DESC 
LIMIT 10;

-- Count news by category
SELECT category, COUNT(*) as count 
FROM news 
GROUP BY category;

-- Search news by keyword
SELECT title, url, published_date 
FROM news 
WHERE title LIKE '%keyword%' 
OR content LIKE '%keyword%';
```

### Data Persistence 資料持久化

The database file is stored in the `./data` directory on your host machine:
資料庫檔案存儲在主機的 `./data` 目錄中：

```
./data/
  └── news.db  # SQLite database file 資料庫檔案
```

## Development 開發

### Using VS Code with Dev Container 使用 VS Code 與開發容器

1. Install VS Code and Docker
   安裝 VS Code 和 Docker

2. Install "Remote - Containers" extension in VS Code
   在 VS Code 中安裝 "Remote - Containers" 擴充功能

3. Clone the repository and open in VS Code
   克隆儲存庫並在 VS Code 中開啟
   ```bash
   git clone <repository-url>
   code bbc-news-crawler
   ```

4. When prompted, click "Reopen in Container"
   當提示時，點擊 "在容器中重新開啟"

### Traditional Setup 傳統設置

1. Clone the repository 克隆儲存庫
   ```bash
   git clone <repository-url>
   cd bbc-news-crawler
   ```

2. Create a virtual environment (recommended)
   建立虛擬環境（推薦）
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   安裝依賴
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database
   初始化資料庫
   ```bash
   python src/database/init_db.py
   ```

5. Run the crawler
   執行爬蟲
   ```bash
   python src/main.py
   ```

### Docker Setup Docker 設置

1. Build the image
   建立映像檔
   ```bash
   docker build -t bbc-news-crawler .
   ```

2. Run the container
   執行容器
   ```bash
   docker run -v $(pwd)/data:/app/data bbc-news-crawler
   ```

## Project Structure 專案結構

```
├── .devcontainer/    # VS Code development container configuration
├── src/
│   ├── crawler/      # Crawler related modules
│   ├── database/     # Database operations
│   └── main.py       # Entry point
├── tests/            # Test files
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation
```

## Configuration 配置

The crawler can be configured through environment variables:
爬蟲可以通過環境變數進行配置：

- `CRAWL_INTERVAL`: Crawling interval in minutes (default: 10)
  爬取間隔（分鐘，預設：10）
- `DB_PATH`: SQLite database path (default: news.db)
  SQLite 資料庫路徑（預設：news.db）

## Testing 測試

[Previous testing section content...]

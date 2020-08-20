## Scrapy Crawler for parsing product data from tesco.com

Crawler saves data to MySQL database.<br>
Make SQLAlchemy database migrations using Alembic. <br>
Models placed to <i><b>database/models</b></i>, migrations - <i><b>database/versions</b></i>

### Installation
```shell 
    $ git clone https://github.com/el-psycongro/tesco.git  
```
 ### Start spider
- Paste links for scraping into <b>requst_links.json</b>
- Build and start docker (DB migration and parsing will be start automatically) 
```shell 
    $ docker-compose run scrapy 
```
- **Get dump**
 >generate ```dump.sql``` in host machine 
```shell
     docker exec -i <container_name> mysqldump -uroot -proot --databases <db_name> --skip-comments > ./db_/dump.sql
```
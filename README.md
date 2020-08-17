## Scrapy Crawler for parsing product data from tesco.com

Crawler saves data to mysql database using sqlAlchemy.<br>
Models placed to <i><b>database/models</b></i>, migrations - <i><b>database/versions</b></i>
Paste links for scraping into <b>requst_links.json</b>
### Installation

>clone repo
```shell 
    $ git clone https://github.com/el-psycongro/tesco.git  
```
>select folder 
```shell 
    $ cd path/to/project  
```
 - **<b>Before start spider first time:**
    - configure connection in  <b>.env</b>
    - manually create table using exist migrations with command(into database folder inside "scrapy" container):  
    
```shell 
    $ docker-compose -f docker-compose.deploy.yml up 
```
```shell 
    $ docker-compose run scrapy bash 
```
```shell 
    $ cd path/to/database
```
```shell
    $ alembic upgrade head
```
 ### Start spider
 - **Docker**
    > parsing will be start automatically
    ```shell 
        $ docker-compose -f docker-compose.deploy.yml run scrapy scrapy crawl tesco
    ```

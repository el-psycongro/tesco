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
 ### Start spider
 - **Docker**
    > parsing will be start automatically
    ```shell 
        $ docker-compose -f docker-compose.deploy.yml run scrapy scrapy crawl tesco
    ```

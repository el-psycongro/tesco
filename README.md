## Scrapy Crawler for parsing product data from tesco.com

Crawler saves data to mysql database using sqlAlchemy.<br>
Models placed to <i><b>database/models</b></i>, migrations - <i><b>alembic/versions/</b></i>

- [Installation](#installation)
- [Start spider](#Start spider)

### Start spider
- **Step 1**
    <br><b>Before start spider first time:</b>
    - configure connection in  <b>.env</b> 
    - create table using exist migrations with command:
    ```shell
    $ alembic upgrade head
    ```
- **Step 2**
    - **Venv**
        > Spawns a shell within the virtualenv
        ```shell 
            $ pipenv shell
        ```
        >run spider
        ```shell
            $ scrapy crawl tesco -a url=*page_url* 
        ```
    - **Docker**
        > build docker from Dockerfile
        ```shell 
            $ docker build -t name_of_contaner
        ```
        > run docker and scrapy
        ```shell 
            $ docker run name_of_contaner scrapy crawl tesco -a url=*page_url*
        ```
    
### Installation

>clone repo
```shell 
    $ git clone https://github.com/el-psycongro/tesco.git  
```
>select folder 
```shell 
    $ cd path/to/project  
```
Below two option to installation and usage spider:
- **Venv**
    > install requirements using pipenv from pipfile
    ```shell 
        $ pipenv install
    ```
- **Docker**
    > build docker from Dockerfile
    ```shell 
        $ docker build -t name_of_contaner
    ```
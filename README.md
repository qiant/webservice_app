# webservice_app Readme
A simple Web Service to support upload and query resumes information of candidates using FastAPI, postgres db, and sqlalchemy.orm.

Use docker container postgres. 

Note: the Postgresql docker is required to start the service. The web service, config, and commands are tested on Ubuntu Linux workstation. 
        

## 1. How to start the web service:
 
   - postgres db is required to start the web service. The db service is provided through docker container by running the following commands.
   
    
    $ docker pull postgres
    $ docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
    
    
   - To verify the postgres db container is running:
   
    
    $ docker ps
   
    CONTAINER ID   IMAGE                                             COMMAND                  CREATED          STATUS          PORTS      NAMES
    de12d1a150b4   postgres                                          "docker-entrypoint.s…"   4 hours ago      Up 4 hours      5432/tcp   postgres
   

   - Start the fastAPI resume web service through pull docker container from repo
   
    $ docker pull qiant/webservice_app:0.0.1-ubuntu-need-postgres
    $ docker run --network host qiant/webservice_app:0.0.1-ubuntu-need-postgres
   

    You should see the following messages:

    $ docker run --network host qiant/webservice_app:0.0.1-ubuntu-need-postgres 
    INFO:     Will watch for changes in these directories: ['/usr/src/app']
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [1] using statreload
    INFO:     Started server process [8]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.


## 2. To upload resume into database using the api: localhost:8080/api/uploadResumeDetails.
   You can run the shell script which uploads five resumes into the system.
     ```
     $ upload_sample_resume.sh 
     ```
   Or upload the resume one by one on command line using curl.


    $ curl -X POST "http://127.0.0.1:8080/api/uploadResumeDetails" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"John Doe\",\"title\":\"Software Engineer\",\"description\":\"develop software for a fintech firm\",\"company\":\"One Famous Co., LLC\",\"id\":1}"

    $ curl -X POST "http://127.0.0.1:8080/api/uploadResumeDetails" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"Tom Doe\",\"title\":\"Senior Software Engineer\",\"description\":\"develop software in IT firm\",\"company\":\"ACME famous Co.\",\"id\":2}"

    $ curl -X POST "http://127.0.0.1:8080/api/uploadResumeDetails" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"Eric Hanks\",\"title\":\"Software Engineer\",\"description\":\"develop software for a fintech firm\",\"company\":\"ACME famous Co.\"}"

    $ curl -X POST "http://127.0.0.1:8080/api/uploadResumeDetails" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"Eric Smith\",\"title\":\"Software Engineer\",\"description\":\"develop software\",\"company\":\"The Topgun Co., LLC\"}"

    $ curl -X POST "http://127.0.0.1:8080/api/uploadResumeDetails" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"Ron Smith\",\"title\":\"Software Engineer\",\"description\":\"develop software in financial firm\",\"company\":\"ACME Co.\"}"


## 3. To query resume by id through API:

    $ curl http://127.0.0.1:8080/api/getResumeById/2
    {"name":"Tom Doe","title":"Software Engineer","description":"develop software for a fintech firm","company":"ACME famous Co.","id":2}


## 4. To query resume by the exact name in database through API:
   ```
   $ curl http://127.0.0.1:8080/api/getResumeByName/John+Doe
   [{"name":"John Doe","title":"Software Engineer","description":"develop software for a fintech firm","company":"The famous Co., LLC","id":1}]
   ```

## 5. To query resume by name that does not exactly match in DB, the first name matched and the last name matched groups are returned.
   ```
   $ curl http://127.0.0.1:8080/api/getResumeByName/Eric+Doe
    [{"name":"Eric Hanks","title":"Software Engineer","description":"develop software for a fintech firm","company":"ACME famous Co.","id":4},
     {"name":"Eric Smith","title":"Software Engineer","description":"develop software","company":"The famous Co., LLC","id":5},
     {"name":"John Doe","title":"Software Engineer","description":"develop software for a fintech firm","company":"The famous Co., LLC","id":1},
     {"name":"Tom Doe","title":"Software Engineer","description":"develop software for a fintech firm","company":"ACME famous Co.","id":2}]
   ```


## 6. The source code and configure files of the web service app are
```   
── webservice_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    ├── schemas.py
    ├── sql_app.db   <--- if using sqlite db
    ├── readme.txt
    ├── requirements.txt
    ├── upload_sample_resumes.sh
    └── Dockerfile
```

  - To build docker image on local system, in the directory where Dockerfile is  
   ```
   $ docker build -t fastapi_resume_service_require_postgres 
   ```

  - To test the web app without building docker image, all the following packets should be installed 
   ```
   $ cd webservice_app/
   $ pip install "fastapi[all]"
   $ pip install "uvicorn[standard]"
   $ pip install SQLAlchemy
   $ pip install psycopg2-binary
   $ uvicorn main:app --port 8080 --reload
   ```

## 7. Use Redis for cache
   ```
   $ pip install redis
   ```

   Redis: Remote Dictionary Service
   https://realpython.com/python-redis/
  -  install redis
   ```
   $ redisurl="http://download.redis.io/redis-stable.tar.gz"
   $ curl -s -o redis-stable.tar.gz $redisurl
   $ sudo su root
   $ mkdir -p /usr/local/lib/
   $ chmod a+w /usr/local/lib/
   $ tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
   $ rm redis-stable.tar.gz
   $ cd /usr/local/lib/redis-stable/
   $ make && make install
   ```

  - configure redis
   ```
   $ sudo su root
   $ mkdir -p /etc/redis/
   $ touch /etc/redis/6379.conf
   $ sudo vi /etc/redis/6379.conf
   ```
  
   ```
   # /etc/redis/6379.conf

   port              6379
   daemonize         yes
   save              60 1
   bind              127.0.0.1
   tcp-keepalive     300
   dbfilename        dump.rdb
   dir               ./
   rdbcompression    yes
   ```
  - start redis server

   ```
   $ redis-server /etc/redis/6379.conf
   ```
   
  - Install redis-py

   ```
   $ python -m venv .venv
   $ source .venv/bin/activate
   $ pip install redis
   ```


## 8. Test RabbitMQ and Celery worker
  Start RabbitMQ and worker using docker-compose
  ```
   $ docker-compose up
  ```
  

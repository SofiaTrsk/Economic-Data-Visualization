# How to run code
 
To access the Airflow UI and trigger the DAG, the steps below are to be followed.



1. Install docker and docker compose
   1. If you are using linux or any other unix OS run this commands, for Windows install Docker Desktop
``` 
    $ sudo apt-get update
    $ sudo apt install docker*
    $ sudo apt-get install docker-compose-plugin
```
2. After having cloned the repo, navigate to the airflow folder which contains the docker-compose.yaml file
3. Initialize the database (make sure the Docker daemon is already running)
```
    $ docker-compose up airflow-init
```
4. Create the container
```
    $ docker-compose up
```
5. After finishing trigger this command
```
    $docker-compose down -v
```


## Airflow UI
Unpause and trigger the DAG with the specified name. To trigger for a specific date, trigger the DAG with config and input date.


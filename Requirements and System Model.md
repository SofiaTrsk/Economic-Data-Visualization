## Introduction
This project will gather data from the Finnhub API about economic variables, and create dashboards which will be updated daily, automatically. The focus will be on creating a stable infrastructure which can be used not only on it's own, but in other appications as well.
This data will be collected and overriden every day, and it will be automatically cleaned and structured to be also used in other cases.
## Glossary 
* Data Pipeline - A method where raw data is ingested, transformed and stored to be later used for analysis.
* Airflow - an open-source workflow management platform for data engineering pipelines.
* Docker - a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. 
* Docker container - a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries and settings.
* a subsidiary of Amazon that provides on-demand cloud computing platforms and APIs to individuals, companies, and governments, on a metered, pay-as-you-go basis
* AWS S3 - Amazon S3 or Amazon Simple Storage Service is a service offered by Amazon Web Services that provides object storage through a web service interface.
* Raw data - data that has not been processed for use
* API - Application Programming Interface, a set of rules and protocols that allow different software programs to talk to each other and share data or functionality.
* Data Ingestion -  the process of importing large, assorted data files from multiple sources into a single, cloud-based storage medium
* DAG - ed Acyclic Graph, is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies
* Tasks - the basic unit of execution in Airflow
* Task groups - used to organize tasks in the Airflow UI DAG graph view. 
## User Requirements 
This project will supply the user with data that is cleaned, and updated automatically every day. This data will be saved in a scalable storage, where the user can access and use it in any way they need.
It will also display to the user different dashboards for the variable that they need, which they can use in any way that they need. 

*	The files will need to be saved in csv format. There should not be any empty rows or cells. 
*	Data should be updated every day.
*	Data should be collected for: Crypto Candles for the last 5 years.


## System Architecture
* ### Environment
The whole process will be orchestrated with Airflow, which will be set up using a docker container. The AWS services to be used will be a scalable storage such as AWS S3.
* ### Infrastructure 
The storage that is used is AWS S3. Here the data will be split in different folders. The raw data as we get it from the APi, and the transformed data (cleaned and structured), which is the data ready for analysis and visualization.
This data might also be saved into a database, however it is not a neccessary step for this project to work. The aim of this project is to display a stable infrastructure where we can process our data.
This now cleaned data will be used to create dashboards with google dashboards
* ### Codebase
This is the structure of the pipeline. There will be one DAG, which is the ingestion dag. This dag will be responsible for ingesting, cleaning and storing the data, and it will have a task for each of these processes.
Since we will be processing many different variables in parallel, we will be using task groups (a task group will belong to one variable, and it will contain the process described above).
## System Model
![image](https://user-images.githubusercontent.com/128420260/235433898-16577074-281f-4604-b278-3ddf1074f1e1.png)

* The extract task, which will get data from the API in json format, convert it to csv, and store it in S3 storage, will be the first task. This is the API's raw, unfiltered data, which will subsequently be processed by the next task. This smaller process taking place inside the first extract task, is in itself an ETL process. 
*	The raw data that is saved as csv files in S3 will be cleaned and turned into valid csv files with no redundant or empty rows as part of the transformation operation. Rows for certain time stamps that are vacant will be filled under particular conditions. Now, in our storage unit, these files will be kept in a different directory. The clean, usable data in this directory, transformed data, will be available for usage.
*	Last but not least, the load phase will use the previously stated technique to import all of these files that were cleaned throughout the transformation process into the s3 bucket. The system will contact the user with information about any errors it encounters as an extra precaution to guarantee that the procedure proceeds without monitoring.



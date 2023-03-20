# Weather-Data-Visualization
## Project Description 
The projects main goal will be to display visualizations utilising data from OpenWeatherMaps API. This will be achieved by creating an ETL Pipeline which extracts this data, saves it into AWS S3, a scalable storage infrastructure,cleans and transforms it, and finally displays dashboards based on this data. As a data orchestration tool, I will be using Airflow, and to better manage this infrastructure, Docker. Terraform will also be used to create AWS resources.
## Objectives 
The objective of the project is to create an infrastructure which supplies and updates data regulary and automatically, which later can be used for analysis and visualization. This infrastructure can work on it's on just as well as it can be part of a larger application. 
## Limitations
Since AWS Free Tier will be used for this project, it has it's limitations on the amount of data and usage of the services. This should not be a problem if the pipline is not left running for long periods of time, or if the amount of data collected doesn't exceed the limit of 5GB.
### Team composition
I will be using this project for my Graduation Project, as such I will be working alone

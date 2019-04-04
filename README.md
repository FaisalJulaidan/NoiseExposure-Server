###### Note: this README file is dedicated for the Server side of the project for further details about the other sides of the project i.e. Mobile Application, and Web Application, please check their repositories. You will need to install/setup all the three repositories for the project to work properly (e.g. retrive data from the database, login, etc.)

## Motivation

Cardiff Council’s ultimate goal is to make Cardiff a better place to live, work and visit. Additionally, Cardiff Council are facing the need to reduce costs with the annual budget being reduced every year, while still maintaining a high level of service which is expected of them. Despite budget cuts, there is no desirable income to be gained from achieving the ultimate goal.
One way Cardiff Council hopes to achieve this, is through making Cardiff a smart city by the use of smart devices to collect data to better assist policy making.

In order to accomplish a smart city status, there is a strong emphasis on pollution in the Capital such as noise.
This is a major but also a usually overlooked issue facing the city, which can have an adverse effect on the health and productivity of residents. 
Cardiff Council want to be able to have detailed noise data that will allow them to understand trends and correlations as well as to get the public involved to solve these three core problems:

- Lack of detailed noise pollution data in the city to assist in policy and decision making
- Pure cost of monitoring noise levels is expensive
- Lack of awareness among Cardiff residents of the dangers of noise pollution

We believe that the best way to solve the problems above, is to create an Advanced Functionality Mobile and Web Application.
Our solution is a Mobile Application for the general public that will collect detailed noise level data based on the user’s location. This data would be aggregated together to be displayed on a Website in various visual forms such as tables and maps. This will educate and bring awareness to the user on how dangerous high noise levels can be to health and the environment.


## Tech/framework used

**Built with**

* Backend - Flask (python3)
* Database - MySQL
* Object Relational Mapping - SQLAlchemy
* JWT Authentication - Flask-JWT-Extended
* Enum parsing - Marshmallow-Enum

## Features

- [x] Token based authentication (JWT)
- [x] Routing
- [x] Fetch and add data following RESTful architecture



## Project Installation
*Note: you will need to have python version 3 and above*  

##### 1. Clone the project

```bash
git clone git@gitlab.cs.cf.ac.uk:c1628682/nea_server.git
```

##### 2. Install Pipenv run
```bash
pip install --user --upgrade pipenv
```

##### 3. Install modules required
```bash
pipenv install
```

##### 4. Change IP adress on line 230 in app.py to your device's IP address
```bash
app.run(host='Your IP Adress', port=5000) # run the app on specific ip address.
# app.run(host='192.168.43.20', port=5000)
```

##### 4. Run Python Flask Server
```
pipenv run python app.py
```


## MySQL Database Setup

The database has already been setup and hosted on
https://www.freemysqlhosting.net

In order to connect to your MySQL database, please modify the /database/database_credentials.csv to your database detials following the following format


```
username,password,host,port,database_name
```




## Status Code

The kind of responses you might recieve are
- 200 - OK
- 400 - Bad Request
- 500 - Internal Server Error
- 401 - Unauthorized
- 201 - Created (Resource created)



## Contributors
Faisal, Ieuan, Joey, and Matthew 🎉


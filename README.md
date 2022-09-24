# BuffAlert

**BuffAlert allows users to receive free email alerts when a stock product crosses a certain price level.** 
It works using [cron](https://edouardproust.dev/blog/python-deploy-a-cron-job-on-heroku_8) for the automation part and [iexcloud API](https://iexcloud.io/docs/) for the quotation. Each user need to subscribe to a iexcloud account and get an personal API to avoid exceeding Free plan's requests limit (all the steps to do so are explained to the user). At the moment, BuffAlert works with US stocks only, but will be deployed soon with commodities, currencies (forex) and crypto-currencies as well.

![BuffAlert preview](static/img/screenshot.png)

## Requirements

- flask
- flask-session
- flask-sqlalchemy
- mysql-connector-python
- requests
- apscheduler
- werkzeug
- python-dotenv
- datetime
- calendar

## Deployment

1. Rename `..env` into `.env` and fill the file with your credentials
2. Install dependencies
```bash
pipenv install
```
3. Create database
```bash
python3 -c 'from cli.db import create'
```
4. Create tables
```bash
python3 -c 'from models import db; db.create_all()'
```
5. Run the app
```bash
flask run
```
6. Launch alerts cronjob
```bash
python3 -c 'from cli.cron import check_alerts'
```

Create a user (credentials: test@test.com / test)
```bash
python3 -c 'from models import User; User.create("test@test.com", "test")'
```

### Navigate into database localy: 

**With CLI:**
- Run the following commands:
```bash
mysql -u <username> -p
mysql> SHOW DATABASES; # Get list of databases
mysql> USE buffalert <...>; # Complete the statement with any action you need
mysql> DROP DATABASE buffalert # Delete database
# ...
```
[MySQL commands list](https://www.interviewbit.com/blog/mysql-commands/)

**With PhpMyAdmin:**
- [Install PhpMyAdmin](https://www.linuxshelltips.com/install-phpmyadmin-in-linux/)
- Navigate to `http://localhost/phpmyadmin/`: your database should be in the list.

## Tips

- On dev environement on Linux, access the local database files in: `admin:///var/lib/mysql/{db_name}` folder

## Links
- (FLask-SQLAlchemy - Models definition)[https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/]
- (FLask-SQLAlchemy - Db Queries syntax)[https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries]
- (Theme StartBootstrap)[https://startbootstrap.github.io/startbootstrap-new-age/]
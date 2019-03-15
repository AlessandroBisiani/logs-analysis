# Logs Analysis
reporter.py performs a simple analysis of the information contained in the news database and prints it to standard output, per the Udacity Full Stack Web Developer project specifications.


## Use
Once these steps are complete, you can import the module or run it with `python3 reporter.py` from within the VM.
#### You will need the following:
Download everything and install Vagrant and VirtualBox 5.1.
1. Vagrant: [download](https://www.vagrantup.com/downloads.html)
2. VirtualBox 5.1 for your system: [download](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and install
3. A clone of the VM for this project: [the repo](https://github.com/udacity/fullstack-nanodegree-vm). Fork the repository, then clone it to a local directory.
4. The database data: [download](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

#### Setup
1. Once everything is downloaded and Vagrant and VirtualBox are installed, `cd` to your clone of the VM (#3 above). If you forked and cloned it, the directory should be _.../FSND-Virtual-Machine/_.
2. `cd` to vagrant and type `vagrant up` to start the virtual machine. The first time you do this it will download the necessary files and may take a few minutes.
3. Once the VM has started use `vagrant ssh` to interact with it via the command line. You can stop the VM with vagrant halt, or log out of the session with `Ctrl-d`
4. `cd` to the _/vagrant/_ directory. This directory is shared with _.../FSND-Virtual-Machine/vagrant/_ on your local machine.
5. Unzip the database data file you downloaded (previous section #4) and place the contents in _/vagrant/_ on your local machine.
6. To load the data for this project, execute `psql -d news- newsdata.sql` from within _/vagrant/_ on your VM.


### The API provides:
* `connect(db_name='news')`
Connect to a named database and return `connection_object, cursor`
* `top_three_articles(cursor)`
Returns a _string_, answering: __What are the most popular three articles of all time?__
* `top_authors(cursor)`
Returns a _string_, answering: __Who are the most popular article authors of all time?__
* `problem_days(cursor)`
Returns a _string_, answering: __On which days did more than 1% of requests lead to errors?__


## Output
It answers the following, interspersed by delimiters as shown below:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

#### For example:
<pre>
Top articles by views: 
    "Candidate is jerk, alleges rival - 338647 views"
    "Bears love berries, alleges bear - 253801 views"
    "Bad things gone, say good people - 170098 views"
\======================================================================
Top authors by article views: 
    Ursula La Multa - 507594 views
    Rudolf von Treppenwitz - 423457 views
    Anonymous Contributor - 170098 views
    Markoff Chaney - 84557 views
\======================================================================
Days when over 1% of requests lead to errors: 
    17 of July 2016 - 2.26% of 55907 were errors
\======================================================================
</pre>

## Design
Each function takes a cursor, performs a query, and returns a string with the formatted result. A top level check for whether the module is being run as the main module calls all three functions and prints the formatted results. 

##### The SQL: 
1. A simple join and select, by concatenating the content of _articles.slug_ and "/articles/", in order to match that to _log.path_.
2. Create a view to join log and articles and count how many views are attributed to each author. \
Join that table and authors in order to associate author names and ids.
3. Create two views - _daily_logs_ and _error_logs_ - to count and group the logs by day, and select and count the logs by day where the status code is 4xx or 5xx. \
Finally, join those views and select the day, the value equal to 1% of daily logs, and the number of daily 4xx and 5xx logs. Only select where the number of error statuses returned is larger than 1% of the total number of logs.

## Views
<pre>
create view views_by_id
as select author, count(*) as hits 
    from articles, log 
    where path = ('/article/' || slug) 
    group by author 
    limit 10


create view daily_logs 
as select time::date as day, count(*) as daily_total 
    from log 
    group by day


create view error_logs
as select time::date as day, count(*) as daily_errors 
    from log 
    where status like '4%' or status like '5%' 
    group by day
</pre>
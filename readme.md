# Logs Analysis
reporter.py performs a simple analysis of the information contained in the news database and prints it to standard output, per the Udacity Full Stack Web Developer project specifications.


## Use
Run the script with `python reporter.py`


## Output
It answers the following, interspersed by blank lines:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

#### For example:

>"Candidate is jerk, alleges rival" - 338647 views \
>"Bears love berries, alleges bear" - 253801 views \
>"Bad things gone, say good people" - 170098 views 
>
>Ursula La Multa - 507594 views\
>Rudolf von Treppenwitz - 423457 views\
>Anonymous Contributor - 170098 views\
>Markoff Chaney - 84557 views
>
>016-07-17 - 2% errors

## Design

Each query is performed by a function. The function creates a connection and cursor, immediately uses them, closes the connection, and iterates over the results to print.

##### The SQL: 
1. A simple join and select, by concatenating the content of _articles.slug_ and '/articles/', in order to match that to _log.path_.
2. Join log and articles and count how many views are attributed to each author. \
Join that table and authors in order to associate author names and ids.
3. Select, count, and group the logs by day.\
Also select and count the logs by day where the status code is 4xx or 5xx. \
Select the day, the value equal to 1% of daily logs, and the number of daily 4xx and 5xx logs, and join those two tables. Only select where the number of error statuses returned is larger than 1% of the total number of logs.

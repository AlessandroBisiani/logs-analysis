#! /usr/bin/env python3

import psycopg2


def connect(db_name='news'):
    try:
        db = psycopg2.connect(dbname="{}".format(db_name))
        cursor = db.cursor()
        return db, cursor
    except psycopg2.DatabaseError as e:
        print('Error connecting to the database: {}'.format(e.pgerror))


# 1. What are the most popular three articles of all time?
# Return a string with the top three articles by views each on a new line
def top_three_articles():
    top_articles = 'No articles found'
    db, cursor = connect('news')
    try:
        cursor.execute("""select title, count(*) as hits
            from articles, log
            where path = ('/article/' || slug)
            group by title
            order by hits desc
            limit 3
            """)
        article_views = cursor.fetchall()
        db.close()
        # If no articles were found, return
        if len(article_views) <= 0:
            return article_views

    except psycopg2.Error as e:
        print('Fetching top articles by views: \r\n{}'.format(e.pgerror))

    # If the query returns any articles, return the results.
    else:
        top_articles = 'Top articles by views: \r\n'
        for result in article_views:
            top_articles += '    "{0} - {1} views"\r\n'.format(result[0],
                                                               result[1])
        return top_articles


# 2. Who are the most popular article authors of all time?
# Return a string with each author and their number of views on a new line.
def top_authors():
    top_auth = 'No authors found.'
    db, cursor = connect('news')
    try:
        cursor.execute("""
            select name, hits
            from authors, views_by_id as views_by_id
            where id = author
            group by name, hits
            order by hits desc""")

        authors = cursor.fetchall()
        db.close()
        # If no authors were found, return
        if len(authors) <= 0:
            return top_auth

    except psycopg2.Error as e:
        print('Fetching authors by popularity: \r\n{}'.format(e.pgerror))

    # If the query returns any authors, return the results.
    else:
        top_auth = 'Top authors by article views: \r\n'
        for auth in authors:
            top_auth += '    {} - {} views\r\n'.format(auth[0], auth[1])
        return top_auth


# 3. On which days did more than 1% of requests lead to errors?
# Return a string with the day and percentage of errors.
def problem_days():
    days = 'None found'
    try:
        db, cursor = connect('news')

        logs = """select daily.day,
            daily_total::integer/100,
            daily_errors::integer,
            daily_total
            from daily_logs as daily, error_logs as errors
            where (daily_total::integer/100.0) <
                    daily_errors::integer
                    and daily.day = errors.day
            order by daily.day
            """

        cursor.execute(logs)
        report = cursor.fetchall()
        db.close()
        # If no days were found, return
        if len(report) <= 0:
            return days

    except psycopg2.Error as e:
        print('Fetching summary of days with >1% error statuses: \r\n{}'
              .format(e.pgerror))

    # If the query returns any days, return the results.
    else:
        days = 'Days when over 1% of requests lead to errors: \r\n'
        for date in report:
            percentage_error = round((date[2]/date[1]), 2)
            days += '    {0} - {1}% of {2} were errors\r\n'.format(
                                                            date[0],
                                                            percentage_error,
                                                            date[3])
        return days


if __name__ == '__main__':
    print('\r\n{0}{3}\r\n{1}{3}\r\n{2}{3}\r\n'.format(top_three_articles(),
                                                      top_authors(),
                                                      problem_days(),
                                                      ('='*70)))

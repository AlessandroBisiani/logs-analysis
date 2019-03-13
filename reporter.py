import psycopg2


# 1. What are the most popular three articles of all time?
def top_three_articles():
        db = psycopg2.connect("dbname=news")
        cursor = db.cursor()
        cursor.execute("""select title, count(*) as hits
                from articles, log
                where path = ('/article/' || slug)
                group by title
                order by hits desc
                limit 3
                """)
        # having log.path in (select ('/article/' || slug) from articles)
        article_views = cursor.fetchall()
        db.close()

        for result in article_views:
                print '"' + result[0] + '"', '-', result[1], 'views'


# 2. Who are the most popular article authors of all time?
def top_authors():
        db = psycopg2.connect("dbname=news")
        cursor = db.cursor()

        views_by_id = """select author, count(*) as hits
                from articles, log
                where path = ('/article/' || slug)
                group by author
                limit 10
                """

        cursor.execute("""
                select name, hits
                from authors, ({}) as views_by_id
                where id = author
                group by name, hits
                order by hits desc
                """.format(views_by_id))

        authors = cursor.fetchall()
        db.close()

        for auth in authors:
                print auth[0], '-', auth[1], 'views'


# 3. On which days did more than 1% of requests lead to errors?
def problem_days():
        days = 'None found'
        db = psycopg2.connect("dbname=news")
        cursor = db.cursor()

        daily_logs = """select time::date as day, count(*) as daily_total
                        from log
                        group by day
                        """
        error_logs = """select time::date as day, count(*) as daily_errors
                        from log
                        where status like '4%' or status like '5%'
                        group by day
                        """
        logs = """select daily.day,
                        daily_total::integer/100,
                        daily_errors::integer
                        from ({}) as daily, ({}) as errors
                        where (daily_total::integer/100) <
                                daily_errors::integer
                                and daily.day = errors.day
                        order by daily.day
                        """.format(daily_logs, error_logs)

        cursor.execute(logs)
        report = cursor.fetchall()
        db.close()

        for date in report:
                print str(date[0]) + ' - ' + str(date[2]/date[1]) + '% errors'


print
top_three_articles()
print
top_authors()
print
problem_days()
print
print

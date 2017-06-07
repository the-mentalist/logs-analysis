import psycopg2
conn = psycopg2.connect(database='news')
cursor = conn.cursor()

#
# Query 1
#

# query extracts article's unique slug from path column of log table
# result is joined with article table to extract title
cursor.execute(
	"select articles.title, logs.count from articles, " +
	"(select replace(path,'/article/', ''), count(*) " +
	"from log " +
	"where status like '200%' " +
	"group by path " +
	"offset 1) as logs " +
	"where articles.slug=logs.replace " +
	"order by logs.count desc limit 3;"
)

results = cursor.fetchall()
print
print "Most popular three article"
for row in results:
	print row[0], " - ", int(row[1]), " views"

#
# Query 2
#

# drop view if already exists
cursor.execute(
	'drop view articlecount;'
)

# this view consists of articles unique name, authors id, and number of views
cursor.execute(
	"create view articlecount as " +
	"select logs.replace as path,logs.count,articles.author from articles, " +
	"(select replace(path,'/article/', ''), count(*) " +
	"from log " +
	"where status like '200%' " +
	"group by path " +
	"offset 1) as logs " +
	"where articles.slug=logs.replace " +
	"order by logs.count desc;"
)

cursor.execute(
	"select name,sum(count) from articlecount,authors where authors.id=author group by name;"
)

results = cursor.fetchall()
print
print "Most popular article authors"
for row in results:
	print row[0], " - ", int(row[1]), " views"

#
# Query 3
#

# here first query returns total request per day and second returns errors per day
# both are joined to get percentage error
cursor.execute(
	"select to_char(total.date,'Mon DD, YYYY'), round(ecount*100.0/tcount,2) as percentage_error from " +
	"(select date(time), count(status) as tcount from log group by date(time)) as total left join " +
	"(select date(time), count(status) as ecount from log where status not like '%OK' group by date(time)) as error " +
	"on total.date=error.date " +
	"where  round(ecount*100.0/tcount,2)>1.00;"
)

results = cursor.fetchall()
print
print "Day having more than 1% errors"
for row in results:
	print row[0], " - ", float(row[1]), "% errors"

conn.close()

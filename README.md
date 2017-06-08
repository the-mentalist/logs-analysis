This module is in reference to Logs Analysis Project of Udacity's Full Stack Web Developer Nanodegree.

Before running, please make sure that
	psql should be installed
	news database exists
		it is not pre-installed with vagrant
		if doesn't exists, run ' psql -d news -f newsdata.sql '

Files:
	analyse.py - consist of Python2 code which connects to news database and extracts required responses.
	response.png - screenshot of result of analyse.py

Note: analyse.py also involves views
	following sql statement is used for creation of view used:
		create view articlecount as
    	select logs.replace as path,logs.count,articles.author from articles,
    	(select replace(path,'/article/', ''), count(*)
    	from log
    	where status like '200%'
    	group by path
    	offset 1) as logs
    	where articles.slug=logs.replace
    	order by logs.count desc;

How to Run:
	Enter the project directory - analyse.py is placed in project folder, so enter the path where code is fetched
	type 'python analyse.py'

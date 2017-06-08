This module is in reference to Logs Analysis Project of Udacity's Full Stack Web Developer Nanodegree.

Before running, please make sure that news database exists and psql should be installed.

Files:
	analyse.py - consist of Python2 code which connects to news database and extracts required responses.
	response.png - screenshot of result of analyse.py

Note: analyse.py also involves views, since creation and deletion is already handled in this file so there is no requirement of external creation of any view
	for reference only, following sql statement is used for creation of view used:
		create view articlecount as
		select l.replace as path,l.count,a.author from articles as a,
		(select replace(path,'/article/', ''), count(*)
		from log
		where status like '200%'
		group by path
		offset 1) as l
		where a.slug=l.replace
		order by l.count desc;

How to Run:
	Enter the project directory
	type 'python analyse.py'

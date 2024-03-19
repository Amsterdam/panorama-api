SQL needed to set up the panorama postgresql database.

A dump of the postgresql on cloudvps was obtained.
This dump turned out to be too big to import at once,
so the create statements for tables and indexes were split out of the dump.
Irrelevant or incorrect parts of the create statements 
are commented out in the sql file.

Also the ownership structure on Azure is different. On Azure
a `panorama_owner` user is owner of the data.


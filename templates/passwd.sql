use {{ icat_name }};

create table IF NOT EXISTS PASSWD (UserName VARCHAR(20), encodedPassword VARCHAR(20));

LOAD DATA LOCAL INFILE '{{ download_dir }}PASSWD.text' INTO TABLE PASSWD
FIELDS TERMINATED BY ',';

SELECT * FROM PASSWD;


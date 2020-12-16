drop table application_user
drop table complain



 create table application_user(
 username VARCHAR(50) not null,
 email VARCHAR(50) not null,
 phone number not null,
 pass VARCHAR(50) not null,
 user_id varchar(30) not null,
 PRIMARY KEY (user_id) 
 );

 
 create table application_manager(
 username VARCHAR(50) not null,
 email VARCHAR(50) not null,
 phone number not null,
 pass VARCHAR(50) not null,
 app_id varchar(30) not null,
 PRIMARY KEY (app_id)
 );
 
create table complain(
 complain_id VARCHAR(50) not null,
 status VARCHAR(50) not null,
 complain_type varchar(30) not null,
 complain_details varchar (500),
 user_id varchar(30) not null,
 app_id varchar(30),
 address varchar(50)
 FOREIGN KEY ( user_id ) REFERENCES application_user (user_id),
 FOREIGN KEY ( app_id ) REFERENCES application_manager (app_id),
 primary key(complain_id,user_id)
 );



select * from application_user 

Insert into application_user
values('Adil','adilasi1999@hotmail.com',123456789111,'Dfb456','1234')

Select count(*) from application_user where phone = 123456789111


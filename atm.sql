-- create database atm;
-- use atm;
create table user(name varchar(25) not null,user_id int NOT NULL AUTO_INCREMENT primary key,pin int unique,number_of_transactions int default 0,limit_of_transactions int default 5,balance int default 0);
CREATE EVENT auto_reset ON SCHEDULE EVERY 120 SECOND DO UPDATE user SET limit_of_transactions = 5;
create table admin(admin_id varchar(20) primary key,password varchar(20) unique,name varchar(25));
create table transaction(transaction_id int NOT NULL AUTO_INCREMENT primary key,t_user_id int,user_name varchar(25),withdrawn_or_deposited bool,amount int,trans_pin int,foreign key(t_user_id) references user(user_id) on delete set null on update cascade);
create table atm(atmamount int default 0,two_k int default 0,half_k int default 0,hundreds int default 0,two_hundreds int default 0);
insert into atm values(0,0,0,0,0);hello
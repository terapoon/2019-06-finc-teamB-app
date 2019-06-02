drop database test;
create database test;
ALTER DATABASE test default character set utf8;
use test;

create table users (
  `id` int AUTO_INCREMENT,
  `email` varchar(64) not null unique,
  `hashed_password` varchar(64) not null,
  `gender` int not null,
  `year` int,
  `month` int,
  `day` int,
  `available_year` int,
  `available_month` int,
  `available_date` int,
  `available_area` int,
  `available_slot` int,
  `profile_img` varchar(64) not null,
  `hobby` varchar(64),
  `name` varchar(64),
  `introduce` text,
  `steps` int,
  `weight` int,
  `bmi` int,
  `bodyfat` int,
  `visfat` int,
  `muscle` int,
  `bodyage` int,
  `goal_weight` int,
  `goal_steps` int,
  `goal_sleep-hour` int,
  `goal_sleep_minute` int,
  `gym` int,
  `intensiveness` int,
  PRIMARY KEY (id)
);

create table likes (
  `id` int AUTO_INCREMENT,
  `user_id_from` int not null,
  `user_id_to` int not null,
  `type` enum('like', 'dislike') not null,
  PRIMARY KEY (id)
);

create table matches (
  `id` int AUTO_INCREMENT,
  `user_id_male` int not null,
  `user_id_female` int not null,
  `year` int not null,
  `month` int not null,
  `date` int not null,
  `slot` int not null,
  `area` int not null,
  PRIMARY KEY (id)
);

create table user_costs (
  `user_id_male` int,
  `user_id_female` int,
  `edge_cost` float
);

create table areas (
  `id` int AUTO_INCREMENT,
  `name` varchar(64),
  PRIMARY KEY (id)
);

create table slots (
  `id` int AUTO_INCREMENT,
  `name` varchar(64),
  PRIMARY KEY (id)
);

insert into areas (`name`) values ('世田谷区');
insert into areas (`name`) values ('大田区');
insert into areas (`name`) values ('目黒区');
insert into slots (`name`) values ('6:00');
insert into slots (`name`) values ('7:00');
insert into slots (`name`) values ('8:00');

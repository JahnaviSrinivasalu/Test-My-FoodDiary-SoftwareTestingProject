create table main_table(food_name varchar2(20) primary key, carbo number(10) not null,
                        protein number(10) not null, fat number(10) not null);



create table diet_table(food_name varchar2(20), carbo number(10) not null,protein number(10) not null,
                        fat number(10) not null,_date  date, day number(10), month number(10), year number(10));

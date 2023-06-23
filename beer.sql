drop table if exists beer;

create table beer
(
    id         serial
        primary key,
    name       text  not null,
    region     text not null,
    type       text  not null,
    style      text  not null,
    strength   float not null,
    price_disc int   not null,
    price      int   not null,
    volume     float not null
);

select count(*) from beer;

select * from beer;


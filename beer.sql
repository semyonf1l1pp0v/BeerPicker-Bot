drop table if exists beer;

create table public.beer
(
    id       serial
        primary key,
    name     text             not null,
    type     integer          not null,
    style    text             not null,
    strength double precision not null,
    volume   double precision not null,
    cost     integer          not null,
    region   text             not null
);

alter table public.beer
    owner to postgres;



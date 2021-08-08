create schema content;
create extension if not exists "uuid-ossp";

create table if not exists content.film_work
(
    id            uuid primary key default uuid_generate_v4(),
    title         text not null,
    description   text,
    creation_date date,
    certificate   text,
    file_path     text,
    rating        float,
    type          text not null,
    created_at    timestamp with time zone,
    updated_at    timestamp with time zone
);

create table if not exists content.genre
(
    id          uuid primary key default uuid_generate_v4(),
    name        text not null,
    description text,
    created_at  timestamp with time zone,
    updated_at  timestamp with time zone
);

create table if not exists content.person
(
    id         uuid primary key default uuid_generate_v4(),
    full_name  text not null,
    birth_date date,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

create table if not exists content.genre_film_work
(
    id           uuid primary key default uuid_generate_v4(),
    film_work_id uuid references content.film_work,
    genre_id     uuid references content.genre,
    created_at   timestamp with time zone
);
create unique index film_work_genre_idx on content.genre_film_work (film_work_id, genre_id);

create table if not exists content.person_film_work
(
    id           uuid primary key default uuid_generate_v4(),
    film_work_id uuid references content.film_work,
    person_id    uuid references content.person,
    role         text not null,
    created_at   timestamp with time zone
);
create unique index film_work_person_role_idx on content.person_film_work (film_work_id, person_id, role);


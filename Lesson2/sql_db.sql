create table if not exists 'Mainmenu' (
id integer primary key autoincrement,
title text not null,
url text not null
);

create table if not exists posts(
id integer primary key autoincrement,
site text not null,
author text,
title text not null,
description text not null,
url text not null,
urlToImage text not null,
time integer not null
);


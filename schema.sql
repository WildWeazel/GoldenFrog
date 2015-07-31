drop table if exists vpn;
create table vpn (
  id integer primary key autoincrement,
  name text not null,
  latitude real not null,
  longitude real not null
);
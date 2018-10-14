Archerank2
==========

For the evaluation of archery tournaments.

motivation
----------

I got a sqlite file from Archerank, but I did not receive the program itself.
Would like to create a program with which the data can be entered and evaluated, and should create winners deeds as a pdf.
But data from Archerank2 should not use for Archerank, because I have no software to test it and I would like it not.
Archerank2 should be a software with new ideas, modern design and free use (GPL). 
Help is very welcome.

database
--------

- CREATE TABLE ages ( age integer NOT NULL PRIMARY KEY, short text NOT NULL, name text NOT NULL, sep integer DEFAULT 1, adult integer DEFAULT 1, pos integer DEFAULT 0 )

- CREATE TABLE bows ( bow integer NOT NULL PRIMARY KEY, short text NOT NULL, name text NOT NULL, pos integer DEFAULT 0 )

- CREATE TABLE settings ( name text NOT NULL PRIMARY KEY, value text NOT NULL )

- CREATE TABLE users ( nr integer NOT NULL PRIMARY KEY, lastname text DEFAULT '', name text DEFAULT '', club text DEFAULT '', score integer DEFAULT 0, kills integer DEFAULT 0, age integer NOT NULL, bow integer NOT NULL, part integer DEFAULT 1, rate integer DEFAULT 1, other text DEFAULT '' )

- CREATE INDEX usersPart ON users (part,rate,age,score,kills,bow)

- CREATE VIEW adults AS SELECT nr, lastname, a.name as name, club, score, kills, a.age as age, a.bow as bow, part, rate, other, ages.name AS age_name, ages.short AS age_short, ages.sep as age_sep, bows.name AS bow_name, bows.short AS bow_short, ages.pos AS age_pos, bows.pos AS bow_pos, CASE ages.sep WHEN 0 THEN 0 ELSE bows.pos END AS bow_sort, (SELECT COUNT(*)+1 from users as b WHERE b.rate = 1 AND b.part = 1 AND ( a.score < b.score OR ( a.score = b.score AND a.kills < b.kills ) ) AND b.age IN (SELECT age from ages WHERE adult>0)) as place FROM users as a LEFT JOIN ages USING ( age ) LEFT JOIN bows ON ( a.bow = bows.bow) WHERE ages.adult > 0

- CREATE VIEW results AS SELECT nr, lastname, a.name as name, club, score, kills, a.age as age, a.bow as bow, part, rate, other, ages.name AS age_name, ages.short AS age_short, bows.name AS bow_name, bows.short AS bow_short, ages.sep as age_sep, ages.pos AS age_pos, bows.pos AS bow_pos, CASE ages.sep WHEN 0 THEN 0 ELSE bows.pos END AS bow_sort, (SELECT COUNT(*)+1 from users as b WHERE b.rate = 1 AND b.part = 1 AND ( a.score < b.score OR ( a.score = b.score AND a.kills < b.kills ) ) AND a.age = b.age AND ( a.bow = b.bow OR ages.sep = 0)) AS place FROM users as a LEFT JOIN ages USING ( age ) LEFT JOIN bows ON ( a.bow = bows.bow)

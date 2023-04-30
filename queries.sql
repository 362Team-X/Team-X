--Anime search by name
--1--
SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM Anime WHERE eng_title ILIKE '%naruto%' OR japanese_title ILIKE '%naruto' AND source = 'Original';
-- Get anime/manga with an id
--2--
SELECT * FROM Anime WHERE ID = 2000;
--Get top 10 anime/manga
--3--
SELECT  Anime.ID,eng_title,japanese_title,episodes,aired_from,aired_to,score,num_scored_by FROM Anime  WHERE source = 'Manga' ORDER BY score DESC LIMIT 10;
--yearly specials 
--4--
WITH temp AS (
    SELECT id,eng_title,japanese_title,episodes,EXTRACT(YEAR FROM aired_from) As year_from,COUNT(*) AS num_watched
    FROM Completed,Anime WHERE Anime.id = Completed.animeid AND Anime.source = 'Manga'
    GROUP BY id,eng_title,japanese_title,episodes,year_from),
    temp2 AS(
    SELECT id,eng_title,japanese_title,episodes,year_from,num_watched,rank() over(partition by year_from ORDER BY num_watched DESC) AS row_num FROM temp ) 
    SELECT id,eng_title,japanese_title,episodes,year_from FROM temp2 WHERE row_num = 1 ORDER BY year_from DESC;

--most favourited
--5--
WITH temp AS(
SELECT animeid,COUNT(*) as num_users FROM Favourites WHERE Source =  'Original' GROUP BY animeid ORDER BY num_users DESC LIMIT 10)
SELECT  ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM temp,anime WHERE animeid = id ;
--stats
--6--
SELECT * FROM Stats WHERE name = '0';
--friends
--7--
SELECT name1 FROM friends WHERE name2 = 'friendname'
UNION 
SELECT name2 FROM friends WHERE name1 = 'friendname';
--Search for a user
--8--
SELECT * FROM users WHERE name = '0';
--9, 10, 11, 12--
-- Display animes completed , favourites , planning , watching
WITH temp AS (
    SELECT animeid,score FROM completed WHERE name ='0' 
)
SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to,anime.score FROM anime, temp WHERE animeid=ID;

WITH temp AS (
    SELECT animeid FROM planning WHERE name ='0' 
)
SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime, temp WHERE animeid=ID;

WITH temp AS (
    SELECT animeid FROM watching WHERE name ='0' 
)
SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime, temp WHERE animeid=ID;


WITH temp AS (
    SELECT animeid FROM Favourites WHERE name ='-Mahiru-' 
)
SELECT ID,eng_title,episodes,aired_from,aired_to FROM anime, temp WHERE animeid=ID;

--Display Anime by genres
--13--
SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime WHERE 'Action' = ANY(genres) LIMIT 20;

--Recomendations
--14--
WITH temp AS(
    SELECT genre FROM Genre_count WHERE name = '0' ORDER BY count DESC LIMIT 2
)
SELECT DISTINCT ID,eng_title,japanese_title,episodes,aired_from,aired_to,score FROM temp,anime WHERE genre = ANY(genres) AND source = 'Manga' ORDER BY score DESC LIMIT 10;

--insert anime 
--15--
INSERT INTO Anime(ID, aired_from, aired_to, duration, episodes, genres, premiered, certification, source, synopsis, eng_title, japanese_title, type, studio_id, score, num_scored_by)
  VALUES (932487242, '2023-04-17', NULL, '24 min', 12, '{Action, Adventure}', 'Spring 2023', 'PG-13', 'Original', 'A new anime series', 'New Series', 'japanese', 'TV', 1, 8.0, 1000);


BEGIN TRANSACTION;

-- insert new row into Completed table
--16--
INSERT INTO Completed(name, animeid,score)
VALUES ('Username', 932487242, 9);

--genre_count updation is pending
 WITH genres AS (
   SELECT UNNEST(genres) AS genre
   FROM Anime
   WHERE ID = 932487242
 ),
 existing_counts AS (
   SELECT name, genre, count
   FROM Genre_count
   WHERE name = 'Username'
 )
 INSERT INTO Genre_count (name, genre, count)
 SELECT 'Username', genre, COALESCE(count, 0) + 1
 FROM genres
 LEFT JOIN existing_counts USING (name, genre);

 update corresponding row in Stats table
UPDATE Stats
SET num_completed = num_completed + 1,
    episodes_watched = episodes_watched + (SELECT episodes FROM Anime WHERE ID = 123)
WHERE name = 'Username';

UPDATE Anime
SET num_scored_by =num_scored_by +1,
    score = ((SELECT score FROM Anime WHERE id = 123)*(num_scored_by-1)*(1.0) + 9 *(1.0))/(num_scored_by)
WHERE ID = 123;



END TRANSACTION;

-- insert new row into planning table
--17--

BEGIN TRANSACTION;

INSERT INTO planning(name, animeid)
VALUES ('Username', 123);
UPDATE Stats
SET num_planning = num_planning + 1
WHERE name = 'Username';

END TRANSACTION;


--18--
BEGIN TRANSACTION;

-- insert new row into watching table
INSERT INTO watching(name, animeid)
VALUES ('username2', 123);

-- update corresponding row in Stats table
UPDATE Stats
SET num_watching = num_watching + 1
WHERE name = 'Username';

END TRANSACTION;


--19--

-- insert new row into Favourites table
INSERT INTO Favourites(name, animeid)
VALUES ('Username', 123);

--20--
--adding a user to user table
BEGIN TRANSACTION;
INSERT INTO Users (name, gender, birthdate, location, joindate, inbox) 
VALUES ('vignesh', 'Male', '1990-01-01', 'New York', '2021-04-17', '{}');
INSERT INTO Stats(name,num_completed,episodes_watched,num_watching,num_planning)
VALUES('vignesh',0,0,0,0);
END TRANSACTION;

--adding a friend
--21--
UPDATE Users
SET inbox = array_append(inbox,'username2') WHERE name = 'Username';

--Accept a friend request
--21--
BEGIN TRANSACTION;
INSERT INTO Friends(name1,name2)
VALUES('username2','Username') ;
UPDATE Users
SET inbox = array_remove(inbox,'username2') WHERE name = 'Username';
END TRANSACTION;
--Reject a friend request
--22--
UPDATE Users
SET inbox = array_remove(inbox,'username2') WHERE name = 'Username';



WITH genres AS (SELECT unnest(genres) as genre FROM Anime WHERE ID = 123), existing_genres AS (UPDATE Genre_count SET count = count + 1 WHERE genre IN (SELECT genre FROM genres) AND name = 'vignesh' RETURNING genre) INSERT INTO Genre_count (name, genre, count) SELECT 'vignesh', genre, 1 FROM genres WHERE genre NOT IN (SELECT genre FROM existing_genres);



UPDATE Genre_count SET count = count - 1 WHERE genre = ANY(SELECT unnest(genres) FROM Anime WHERE ID = 123) AND name = 'vignesh';





 








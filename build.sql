BEGIN TRANSACTION;

DROP TABLE IF EXISTS Studio;
CREATE TABLE Studio(
    studio_id int NOT NULL,
    name varchar(50),
    PRIMARY KEY(studio_id)
);

DROP TABLE IF EXISTS Anime;
CREATE TABLE Anime(
    ID int NOT NULL,
    aired_from DATE,
    aired_to DATE,
    duration varchar(50),
    episodes int,
    genres varchar(50) [],
    premiered varchar(50),
    certification varchar(75),
    source varchar(20),
    synopsis text,
    eng_title text,
    japanese_title text,
    type varchar(50),
    studio_id int,
    score FLOAT,
    num_scored_by int,
    PRIMARY KEY(ID),
    CONSTRAINT fk_studioid
    FOREIGN KEY(studio_id)
    REFERENCES Studio(studio_id)
);



DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
    name varchar(50),
    gender varchar(20),
    birthdate Date,
    location varchar(50),
    joindate Date,
    inbox name[],
	password varchar(50) DEFAULT '1234',
    PRIMARY KEY(name)
);

DROP TABLE IF EXISTS Planning;
CREATE TABLE Planning(
    name varchar(50),
    animeid int,
    source varchar(50),
    CONSTRAINT fk_animeid1
    FOREIGN KEY(animeid)
    REFERENCES Anime(ID),
    CONSTRAINT fk_name1
    FOREIGN KEY(name)
    REFERENCES Users(name)
);

DROP TABLE IF EXISTS Favourites;
CREATE TABLE Favourites(
    name varchar(50),
    animeid int,
    source varchar(50),
    CONSTRAINT fk_animeid2
    FOREIGN KEY(animeid)
    REFERENCES Anime(ID),
    CONSTRAINT fk_name2
    FOREIGN KEY(name)
    REFERENCES Users(name)
);

DROP TABLE IF EXISTS Watching;
CREATE TABLE Watching(
    name varchar(50),
    animeid int,
    source varchar(50),
    CONSTRAINT fk_animeid3
    FOREIGN KEY(animeid)
    REFERENCES Anime(ID),
    CONSTRAINT fk_name3
    FOREIGN KEY (name)
    REFERENCES Users(name) 
);


DROP TABLE IF EXISTS Completed;
CREATE TABLE Completed(
    name varchar(50),
    animeid int,
    source varchar(50),
    score int,
    CONSTRAINT fk_animeid1
    FOREIGN KEY(animeid)
    REFERENCES Anime(ID),
    CONSTRAINT fk_name1
    FOREIGN KEY(name)
    REFERENCES Users(name)
);

DROP TABLE IF EXISTS Genre_count;
CREATE TABLE Genre_count(
    name varchar(50),
    genre varchar(50),
    count int,
    PRIMARY KEY(genre,name),
    CONSTRAINT fk_genrename
    FOREIGN KEY(name)
    REFERENCES Users(name)
);

DROP TABLE IF EXISTS Stats;
CREATE TABLE Stats(
    name varchar(50),
    num_completed int,
    episodes_watched int,
    num_watching int,
    num_planning int,
    CONSTRAINT fk_Usersname
    FOREIGN KEY(name)
    REFERENCES Users(name)
);

DROP TABLE IF EXISTS Friends;
CREATE TABLE Friends(
    name1 varchar(50),
    name2 varchar(50),
    CONSTRAINT fk_user1
    FOREIGN KEY(name1)
    REFERENCES Users(name),
    CONSTRAINT fk_user2
    FOREIGN KEY(name2)
    REFERENCES Users(name)
);

CREATE INDEX idx_anime_title_source
ON Anime (eng_title, japanese_title, source);

CREATE INDEX idx_anime_aired_from
ON Anime (aired_from);

CREATE INDEX idx_favourites_animeid
ON Favourites (animeid);

CREATE INDEX idx_friends_name	
ON Friends (name1, name2);

CREATE INDEX idx_completed_animeid
ON Completed (animeid);

CREATE INDEX idx_planning_animeid
ON Planning (animeid);

CREATE INDEX idx_watching_animeid
ON Watching (animeid);

END TRANSACTION;

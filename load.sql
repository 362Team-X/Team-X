BEGIN TRANSACTION;
COPY Studio FROM '/home/vignesh/Desktop/DBMS_Project/Database/studio_new.csv' WITH CSV HEADER DELIMITER AS ',';
COPY anime FROM '/home/vignesh/Desktop/DBMS_Project/Database/anime_new.csv' WITH CSV HEADER DELIMITER AS ',';
COPY users(name,gender,birthdate,location,joindate,inbox) FROM '/home/vignesh/Desktop/DBMS_Project/Database/Users.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Favourites FROM '/home/vignesh/Desktop/DBMS_Project/Database/Favourites.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Completed FROM '/home/vignesh/Desktop/DBMS_Project/Database/Completed.csv' WITH CSV HEADER DELIMITER AS ',';
COPY Planning FROM '/home/vignesh/Desktop/DBMS_Project/Database/Planning.csv' WITH CSV HEADER DELIMITER AS ',';
COPY genre_count FROM '/home/vignesh/Desktop/DBMS_Project/Database/Genre_count.csv' WITH CSV HEADER DELIMITER AS ',';
COPY stats FROM '/home/vignesh/Desktop/DBMS_Project/Database/stats.csv' WITH CSV HEADER DELIMITER AS ',';

--Triggers
CREATE FUNCTION update_stats_planning() RETURNS TRIGGER LANGUAGE plpgsql AS $update_stats_planning$
BEGIN
    -- Increment num_planning column for the user in the Stats table after inserting a record in the Planning table
	RAISE NOTICE 'update_stats_planning triggered';
    IF TG_OP = 'INSERT' THEN
        UPDATE Stats
        SET num_planning = num_planning + 1
        WHERE name = NEW.name;
    -- Decrement num_planning column for the user in the Stats table after deleting a record in the Planning table
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE Stats
        SET num_planning = num_planning - 1
        WHERE name = OLD.name;
    END IF;
    RETURN NULL;
END;
$update_stats_planning$;


CREATE TRIGGER update_stats_planning
AFTER INSERT OR DELETE ON Planning
FOR EACH ROW
EXECUTE PROCEDURE update_stats_planning();

CREATE FUNCTION update_stats_completed() RETURNS TRIGGER LANGUAGE plpgsql AS $update_stats_completed$
BEGIN
    -- Increment num_completed column for the user in the Stats table after inserting a record in the completed table
	RAISE NOTICE 'update_stats_completed triggered';
	
    IF TG_OP = 'INSERT' THEN
        UPDATE Stats
        SET num_completed = num_completed + 1,episodes_watched = episodes_watched + (SELECT episodes FROM Anime WHERE ID = NEW.animeid)
        WHERE name = NEW.name;
    -- Decrement num_completed column for the user in the Stats table after deleting a record in the completed table
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE Stats
        SET num_completed = num_completed - 1,episodes_watched = episodes_watched - (SELECT episodes FROM Anime WHERE ID = NEW.animeid)
        WHERE name = OLD.name;
    END IF;
    RETURN NULL;
END;
$update_stats_completed$ ;


CREATE TRIGGER update_stats_completed
AFTER INSERT OR DELETE ON completed
FOR EACH ROW
EXECUTE PROCEDURE update_stats_completed();

CREATE FUNCTION update_stats_watching() RETURNS TRIGGER LANGUAGE plpgsql AS $update_stats_watching$
BEGIN
    -- Increment num_watching column for the user in the Stats table after inserting a record in the watching table
	RAISE NOTICE 'update_stats_watching triggered';
    IF TG_OP = 'INSERT' THEN
        UPDATE Stats
        SET num_watching = num_watching + 1
        WHERE name = NEW.name;
    -- Decrement num_watching column for the user in the Stats table after deleting a record in the watching table
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE Stats
        SET num_watching = num_watching - 1
        WHERE name = OLD.name;
    END IF;
    RETURN NULL;
END;
$update_stats_watching$ ;


CREATE TRIGGER update_stats_watching
AFTER INSERT OR DELETE ON watching
FOR EACH ROW
EXECUTE PROCEDURE update_stats_watching();


END TRANSACTION;

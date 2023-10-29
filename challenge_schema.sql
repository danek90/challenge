-- seasons X
DROP TABLE IF exists seasons CASCADE;
CREATE TABLE seasons (
"season_id" INT NOT NULL UNIQUE
, "season_name" VARCHAR(256) NOT NULL UNIQUE
, PRIMARY KEY ("season_id")
);

-- dailies X
DROP TABLE IF exists dailies CASCADE;
CREATE TABLE dailies (
"daily_id" VARCHAR(256) NOT NULL UNIQUE
, "season_id" INT NOT NULL
, "daily_in_season" INT NOT NULL
, "daily_name" VARCHAR(256) NOT NULL
, "team_format" VARCHAR(256) NOT NULL
, PRIMARY KEY ("daily_id")
, FOREIGN KEY ("season_id") REFERENCES seasons("season_id")
);

-- eliminations X
DROP TABLE IF exists eliminations CASCADE;
CREATE TABLE eliminations (
"elim_id" VARCHAR(256) NOT NULL UNIQUE
, "season_id" INT NOT NULL
, "elim_in_season" INT NOT NULL
, "elim_name" VARCHAR(256) NOT NULL
, "team_format" VARCHAR(256) NOT NULL
, "gender_format" VARCHAR(256) NOT NULL
, PRIMARY KEY ("elim_id")
, FOREIGN KEY ("season_id") REFERENCES seasons("season_id")
);

-- finals X
DROP TABLE IF exists finals CASCADE;
CREATE TABLE finals (
"final_id" VARCHAR(256) NOT NULL UNIQUE
, "season_id" INT NOT NULL
, "final_name" VARCHAR(256) NOT NULL
, "checkpoints" VARCHAR(256) NOT NULL
, PRIMARY KEY ("final_id")
, FOREIGN KEY ("season_id") REFERENCES seasons("season_id")
);


DROP TABLE IF exists episodes CASCADE;
CREATE TABLE episodes (
"ep_id" INT NOT NULL UNIQUE
, "season_id" INT NOT NULL
, "ep_in_season" INT NOT NULL
, "ep_name" VARCHAR(256) NOT NULL
, "air_date" DATE
, "us_viewers_millions" NUMERIC(2)
, PRIMARY KEY ("ep_id")
, FOREIGN KEY ("season_id") REFERENCES seasons("season_id")
);

-- challengers XX
DROP TABLE IF exists challengers CASCADE;
CREATE TABLE challengers (
"ch_id" INT NOT NULL UNIQUE
, "ch_name" VARCHAR(256) NOT NULL
, "legal_name" VARCHAR(256) NOT NULL
, "first_name" VARCHAR(256) NOT NULL
, "last_name" VARCHAR(256) NOT NULL
, "gender" VARCHAR(256) NOT NULL
, "birth" date
, "death" date
, "hometown" VARCHAR(256)
, PRIMARY KEY ("ch_id")
);

-- teams x x
DROP TABLE IF exists teams CASCADE;
CREATE TABLE teams (
"team_id" VARCHAR(256) NOT NULL UNIQUE
, "season_id" INT NOT NULL
, "team_name" VARCHAR(256)
, "leader_id" INT
, "leader_selects" BOOLEAN
, PRIMARY KEY ("team_id")
, FOREIGN KEY ("leader_id") REFERENCES challengers("ch_id")
, FOREIGN KEY ("season_id") REFERENCES seasons("season_id")
);

-- team_ch X X
DROP TABLE IF exists ch_teams CASCADE;
CREATE TABLE ch_teams (
"season_id" INT NOT NULL
, "team_id" VARCHAR(256) NOT NULL
, "ch_id" INT NOT null
, primary key ("season_id", "team_id", "ch_id")
, FOREIGN KEY ("team_id") REFERENCES teams("team_id")
, FOREIGN KEY ("ch_id") REFERENCES challengers("ch_id")
, FOREIGN KEY ("season_id") REFERENCES seasons("season_id")
);

DROP TABLE IF exists elim_history CASCADE;
CREATE TABLE elim_history (
"elim_id" VARCHAR(256) NOT NULL
, "team_id" VARCHAR(256) NOT NULL
, "ch_id" INT NOT NULL
, "elim_partner_id" INT
, "opponent_id"	INT
, "opponent_partner_id" INT
, "elim_result" VARCHAR(256) NOT NULL
, "elim_heat" INT NOT NULL
, "method_id" INT NOT NULL
, PRIMARY KEY ("elim_id", "team_id", "ch_id","opponent_id")
, FOREIGN KEY ("ch_id") REFERENCES challengers("ch_id")
, FOREIGN KEY ("opponent_id") REFERENCES challengers("ch_id")
, FOREIGN KEY ("opponent_partner_id") REFERENCES challengers("ch_id")
, FOREIGN KEY ("team_id") REFERENCES teams("team_id")
);

DROP TABLE IF exists elim_method CASCADE;
CREATE TABLE elim_method (
"method_id" INT NOT NULL
, "method_description" VARCHAR(256) NOT NULL
, "method_class_id" INT NOT NULL
, "method_class" VARCHAR(256) NOT NULL
, "vote_type" VARCHAR(256)
, "sent_to_elim" BOOLEAN
, "voting_group" VARCHAR(256)
, "selection_group" VARCHAR(256)
, PRIMARY KEY ("method_id")
);

-- daily_history
DROP TABLE IF exists daily_history CASCADE;
CREATE TABLE daily_history (
"daily_id" VARCHAR(256) NOT NULL
, "team_id" VARCHAR(256) NOT NULL
, "ch_id" INT NOT NULL
, "daily_team_result" VARCHAR(256) NOT NULL
, "within_team_result" VARCHAR(256)
, PRIMARY KEY ("daily_id", "team_id", "ch_id")
, FOREIGN KEY ("ch_id") REFERENCES challengers("ch_id")
, FOREIGN KEY ("team_id") REFERENCES teams("team_id")
, FOREIGN KEY ("daily_id") REFERENCES dailies("daily_id")
);

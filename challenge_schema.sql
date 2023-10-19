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
"daily_id" INT NOT NULL UNIQUE
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
"elim_id" INT NOT NULL UNIQUE
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
"final_id" INT NOT NULL UNIQUE
, "season_id" INT NOT NULL
, "final_name" VARCHAR(256) NOT NULL
, "checkpoints" VARCHAR(256) NOT NULL
, PRIMARY KEY ("final_id")
, FOREIGN KEY ("season_id") REFERENCES seasons("season_id")
);


-- challengers X
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

-- team_ch X
DROP TABLE IF exists teams_challengers CASCADE;
CREATE TABLE teams_challengers (
"team_ch_index" INT NOT NULL UNIQUE
, "season_id" INT NOT NULL
, "team_id" INT NOT NULL
, "team_name" VARCHAR(256) NOT NULL
, "ch_id" INT NOT NULL
, "ch_name" VARCHAR(256) NOT NULL
, PRIMARY KEY ("team_ch_index")
, FOREIGN KEY ("ch_id") REFERENCES challengers("ch_id")
, FOREIGN KEY ("season_id") REFERENCES seasons("ch_id")
);

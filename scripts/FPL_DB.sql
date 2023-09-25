

DROP TABLE IF EXISTS `player_performance`,`player`,`position`,`team`;

CREATE TABLE `team` (
  `id` integer PRIMARY KEY,
  `name` varchar(255) UNIQUE NOT NULL,
  `strength` integer
);

CREATE TABLE `player` (
  `id` integer PRIMARY KEY,
  `first_name` varchar(255) NOT NULL,
  `second_name` varchar(255) NOT NULL,
  `team_id` integer NOT NULL,
  `position_id` integer NOT NULL,
  `cost` float
);

CREATE TABLE `player_performance` (
  `player_id` integer NOT NULL,
  `form` float,
  `total_points` integer NOT NULL,
  `bonus_points` integer,
  `points_per_game` float,
  `selected_by_percent` float NOT NULL,
  `threat` float,
  `minutes_played` integer,
  `goals_scored` integer,
  `assists` integer,
  `clean_sheets` integer,
  `goals_conceded` integer,
  `yellow_cards` integer,
  `red_cards` integer,
  `games_started` integer
);

CREATE TABLE `position` (
  `id` integer PRIMARY KEY,
  `position_name` varchar(255) UNIQUE NOT NULL,
  `position_count` integer
);

ALTER TABLE `player` ADD FOREIGN KEY (`team_id`) REFERENCES `team` (`id`);

ALTER TABLE `player` ADD FOREIGN KEY (`position_id`) REFERENCES `position` (`id`);

ALTER TABLE `player_performance` ADD FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);

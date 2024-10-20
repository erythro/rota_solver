-- --------------------------------------------------------
-- Host:                         C:\Users\sammy\Documents\CCE\data.db
-- Server version:               3.39.4
-- Server OS:                    
-- HeidiSQL Version:             12.5.0.6677
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for data
CREATE DATABASE IF NOT EXISTS "data";
;

-- Dumping structure for table data.event
CREATE TABLE IF NOT EXISTS "event"(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING);

-- Dumping data for table data.event: 2 rows
DELETE FROM "event";
/*!40000 ALTER TABLE "event" DISABLE KEYS */;
INSERT INTO "event" ("id", "name") VALUES
	(1, '20th Oct'),
	(2, '27th Oct');
/*!40000 ALTER TABLE "event" ENABLE KEYS */;

-- Dumping structure for table data.migration
CREATE TABLE IF NOT EXISTS migration (name STRING PRIMARY KEY, ran_at DATETIME);

-- Dumping data for table data.migration: -1 rows
DELETE FROM "migration";
/*!40000 ALTER TABLE "migration" DISABLE KEYS */;
INSERT INTO "migration" ("name", "ran_at") VALUES
	('initialMigration', '1729442603.24845'),
	('createPersonTable', '1729443020.47316'),
	('createRoleTable', '1729443368.01938'),
	('createEventTable', '1729450143.17272'),
	('createPersonRoleTable', '1729459072.98631'),
	('createSlotTable', '1729459072.98885'),
	('createSolutionTable', '1729460517.36297');
/*!40000 ALTER TABLE "migration" ENABLE KEYS */;

-- Dumping structure for table data.person
CREATE TABLE IF NOT EXISTS person(id INTEGER PRIMARY KEY AUTOINCREMENT, firstName STRING, lastName STRING);

-- Dumping data for table data.person: 2 rows
DELETE FROM "person";
/*!40000 ALTER TABLE "person" DISABLE KEYS */;
INSERT INTO "person" ("id", "firstName", "lastName") VALUES
	(1, 'Foo', 'Bar'),
	(2, 'Baz', 'Bar');
/*!40000 ALTER TABLE "person" ENABLE KEYS */;

-- Dumping structure for table data.person_role
CREATE TABLE IF NOT EXISTS person_role(person_id INTEGER, role_id INTEGER);

-- Dumping data for table data.person_role: -1 rows
DELETE FROM "person_role";
/*!40000 ALTER TABLE "person_role" DISABLE KEYS */;
INSERT INTO "person_role" ("person_id", "role_id") VALUES
	(1, 1),
	(2, 1);
/*!40000 ALTER TABLE "person_role" ENABLE KEYS */;

-- Dumping structure for table data.role
CREATE TABLE IF NOT EXISTS role(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING);

-- Dumping data for table data.role: -1 rows
DELETE FROM "role";
/*!40000 ALTER TABLE "role" DISABLE KEYS */;
INSERT INTO "role" ("id", "name") VALUES
	(1, 'Test Role');
/*!40000 ALTER TABLE "role" ENABLE KEYS */;

-- Dumping structure for table data.slot
CREATE TABLE IF NOT EXISTS "slot"(id INTEGER PRIMARY KEY AUTOINCREMENT, event_id INTEGER, role_id INTEGER);

-- Dumping data for table data.slot: -1 rows
DELETE FROM "slot";
/*!40000 ALTER TABLE "slot" DISABLE KEYS */;
INSERT INTO "slot" ("id", "event_id", "role_id") VALUES
	(1, 1, 1),
	(2, 2, 1);
/*!40000 ALTER TABLE "slot" ENABLE KEYS */;

-- Dumping structure for table data.solution
CREATE TABLE IF NOT EXISTS solution(event_id INTEGER, slot_id INTEGER, person_id INTEGER);

-- Dumping data for table data.solution: 4 rows
DELETE FROM "solution";
/*!40000 ALTER TABLE "solution" DISABLE KEYS */;
INSERT INTO "solution" ("event_id", "slot_id", "person_id") VALUES
	(1, 1, 2),
	(1, 2, 1),
	(2, 1, 2),
	(2, 2, 1);
/*!40000 ALTER TABLE "solution" ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

CREATE TABLE "tasks" (task_id TEXT PRIMARY KEY, status INTEGER NOT NULL DEFAULT '0', unix_time INTEGER);
CREATE TABLE "task_scheduler" (pc TEXT PRIMARY KEY, status INTEGER NOT NULL DEFAULT '0');
INSERT INTO task_scheduler (pc) VALUES ('eeklo'), ('beveren'), ('damme'), ('halle'), ('brugge');
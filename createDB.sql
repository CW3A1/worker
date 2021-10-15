CREATE TABLE "tasks" (task_id TEXT PRIMARY KEY, status INTEGER NOT NULL DEFAULT '0');
CREATE TABLE "task_scheduling" (pc TEXT PRIMARY KEY, status INTEGER NOT NULL DEFAULT '1');
INSERT INTO task_scheduling (pc) VALUES ('eeklo'), ('beveren'), ('damme'), ('halle'), ('brugge');
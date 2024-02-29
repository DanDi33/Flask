CREATE TABLE IF NOT EXISTS `Professions`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `profession` TEXT NOT NULL
);
    
CREATE TABLE IF NOT EXISTS `FIO`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `lastName` TEXT NOT NULL,
    `firstName` TEXT,
    `patronymic` TEXT
);

create table IF NOT EXISTS Types(
	`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `type` TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS `Companies`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `companyName` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `Workers`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `companyId` INTEGER NOT NULL,
    `fioId` INTEGER NOT NULL,
    `professionId` INTEGER NOT NULL,
    FOREIGN KEY(`companyId`) REFERENCES `Companies`(`id`),
    FOREIGN KEY(`professionId`) REFERENCES `Professions`(`id`),
    FOREIGN KEY(`fioId`) REFERENCES `FIO`(`id`)
);

CREATE TABLE IF NOT EXISTS `Phones`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `typeId` INTEGER NOT NULL,
    `number` TEXT NOT NULL unique
);

create table IF NOT EXISTS WorkPhones(
	`id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `workerId` INTEGER NOT NULL,
    `phoneId` INTEGER NOT NULL,
    FOREIGN KEY(workerId) REFERENCES Workers(id),
    FOREIGN KEY(phoneId) REFERENCES Phones(id)
    );
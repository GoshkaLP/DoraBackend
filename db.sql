CREATE TABLE Users (
	id SERIAL,
	email VARCHAR(40) UNIQUE NOT NULL,
	password VARCHAR(40) NOT NULL,
	verified boolean DEFAULT FALSE,

	date_of_creation TIMESTAMP NOT NULL DEFAULT NOW(),
	deleted boolean DEFAULT FALSE,
	PRIMARY KEY (id)
);

CREATE TABLE Users_Codes (
	id SERIAL,
	email VARCHAR(40) NOT NULL,
	code INT NOT NULL,
	type INT NOT NULL,

	date_of_creation TIMESTAMP NOT NULL DEFAULT NOW(),
	deleted boolean DEFAULT FALSE,
	PRIMARY KEY (id),

	CONSTRAINT users_codes_email_fkey
	FOREIGN KEY (email) REFERENCES Users (email)
	MATCH SIMPLE ON UPDATE RESTRICT ON DELETE CASCADE
);

CREATE TABLE Users_Tokens_Salt (
    id SERIAL,
    user_id INT NOT NULL,
    salt VARCHAR(7),

    date_of_creation TIMESTAMP NOT NULL DEFAULT NOW(),
	deleted boolean DEFAULT FALSE,
	PRIMARY KEY (id),

	CONSTRAINT users_tokens_salt_user_id_fkey
	FOREIGN KEY (user_id) REFERENCES Users (id)
	MATCH SIMPLE ON UPDATE RESTRICT ON DELETE CASCADE
);


CREATE TABLE Warranties_Categories (
	id SERIAL,
	name VARCHAR(40) UNIQUE NOT NULL,
	type_warranty_period VARCHAR(1),
	warranty_period INT NOT NULL,

	date_of_creation TIMESTAMP NOT NULL DEFAULT NOW(),
	deleted boolean DEFAULT FALSE,

	CHECK (type_warranty_period in ( 'Y', 'M', 'D' )),
	PRIMARY KEY (id)
);


INSERT INTO Warranties_Categories
	(name, type_warranty_period, warranty_period)
VALUES
	('Товары для дома', 'M', 3),
	('Бытовая техника', 'M', 6),
	('Товары для авто', 'Y', 1),
	('Одежда и обувь', 'D', 30),
	('Другие товары', 'D', 14);


CREATE TABLE Users_Warranties (
	id SERIAL,
	user_id INT NOT NULL,
	name VARCHAR(40) NOT NULL,
	shop_name VARCHAR(50) NOT NULL,
	category_id INT NOT NULL,
	date_of_purchase TIMESTAMP NOT NULL,
	type_warranty_period VARCHAR(1),
	warranty_period INT NOT NULL,

	archived boolean DEFAULT FALSE,

	date_of_creation TIMESTAMP NOT NULL DEFAULT NOW(),
	deleted boolean DEFAULT FALSE,

	CHECK (type_warranty_period in ( 'Y', 'M', 'D' )),
	PRIMARY KEY (id),

	CONSTRAINT users_warranties_user_id_fkey
	FOREIGN KEY (user_id) REFERENCES Users (id)
	MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,

	CONSTRAINT users_warranties_category_id_fkey
	FOREIGN KEY (category_id) REFERENCES Warranties_Categories (id)
	ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE Warranties_Files (
	id SERIAL,
	warranty_id INT NOT NULL,
	path_to_file VARCHAR(255) NOT NULL,

	CONSTRAINT warranties_files_warranty_id_fkey
	FOREIGN KEY (warranty_id) REFERENCES Users_Warranties (id)
	MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,

	date_of_creation TIMESTAMP NOT NULL DEFAULT NOW(),
	deleted boolean DEFAULT FALSE,
	PRIMARY KEY (id)
);

CREATE TABLE Warranties_Cases (
	id SERIAL,
	warranty_id INT NOT NULL,
	expertise boolean NOT NULL DEFAULT FALSE,
	date_end_expertise TIMESTAMP,
	money_returned boolean DEFAULT FALSE,
	item_replaced boolean DEFAULT FALSE,

	CONSTRAINT warranties_cases_warranty_id_fkey
	FOREIGN KEY (warranty_id) REFERENCES Users_Warranties (id)
	MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,

	date_of_creation TIMESTAMP NOT NULL DEFAULT NOW(),
	deleted boolean DEFAULT FALSE,
	PRIMARY KEY (id, warranty_id)
);
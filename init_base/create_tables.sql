CREATE TABLE repositories (
	id_rep INT GENERATED ALWAYS AS IDENTITY,
	name_rep VARCHAR(50) NOT NULL,
	stars INT NOT NULL,
	description TEXT NOT NULL,
	data_ DATE DEFAULT CURRENT_DATE,
	PRIMARY KEY (id_rep)
);

CREATE TABLE keywords (
	id_rep INT NOT NULL,
	tech VARCHAR(50) NOT NULL,
	score NUMERIC(5, 4) NOT NULL,
	PRIMARY KEY (id_rep, tech),
	FOREIGN KEY (id_rep) REFERENCES repositories(id_rep)
);

CREATE TABLE top_tech (
	tech VARCHAR(50) NOT NULL,
	total_score NUMERIC(5, 4) NOT NULL,
	start_data DATE NOT NULL
);
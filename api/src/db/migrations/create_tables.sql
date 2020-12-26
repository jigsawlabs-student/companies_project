DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS sectors;
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS financials;

CREATE TABLE IF NOT EXISTS companies (
  id serial PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  ticker VARCHAR(255) UNIQUE,
  sub_industry_id SMALLINT,
  year_founded SMALLINT,
  number_of_employees INTEGER,
  HQs_state VARCHAR(255),
  country VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS sub_sectors (
  id serial PRIMARY KEY,
  sub_industry_GICS VARCHAR(255),
  sector_GICS VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS quarterly_reports (
  id serial PRIMARY KEY,
  date DATE,
  company_id INTEGER,
  revenue BIGINT,
  cost BIGINT,
  net_income BIGINT,
  earnings_per_share FLOAT
);

CREATE TABLE IF NOT EXISTS prices (
  id serial PRIMARY KEY,
  date DATE,
  company_id INTEGER,
  closing_price FLOAT
);

CREATE TABLE IF NOT EXISTS price_earnings_ratio(
  id serial PRIMARY KEY,
  company_id INTEGER,
  date DATE,
  price_earnings_ratio FLOAT
);


-- MySQL Script generated by MySQL Workbench
-- Wed Mar  3 15:14:06 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

-- -----------------------------------------------------
-- Schema HUWebshop
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema HUWebshop
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table HUWebshop.Products
-- -----------------------------------------------------
DROP TABLE IF EXISTS Products CASCADE ;

create type genders as enum ('Vrouw', 'Man', 'Unisex', 'Gezin', 'B2B', 'Kinderen', 'Senior', 'Baby', 'onbekend');
CREATE TABLE IF NOT EXISTS Products (
  idProducts VARCHAR(255) NOT NULL,
  name VARCHAR(255) NULL,
  brand VARCHAR(255) NULL,
  category VARCHAR(255) NULL,
  deeplink VARCHAR(255) NULL,
  doelgroep VARCHAR(255) NULL,
  fastmover BOOLEAN NULL,
  target genders NULL,
  herhaalaankopen BOOLEAN NULL,
  price DECIMAL NULL,
  PRIMARY KEY (idProducts))
;


-- -----------------------------------------------------
-- Table HUWebshop.Visitors
-- -----------------------------------------------------
DROP TABLE IF EXISTS  Visitors CASCADE ;

CREATE TABLE IF NOT EXISTS Visitors (
  idVisitors SERIAL NOT NULL,
  previously_recommended VARCHAR(255) NULL,
  latest_visit timestamp NULL,
  PRIMARY KEY (idVisitors))
;

-- -----------------------------------------------------
-- Table HUWebshop.Sessions
-- -----------------------------------------------------
DROP TABLE IF EXISTS Sessions CASCADE ;

CREATE TABLE IF NOT EXISTS Sessions (
  idSessions SERIAL NOT NULL,
  identifier VARCHAR NULL,
  sessie_start TIMESTAMP NULL,
  sessie_end TIMESTAMP NULL,
  PRIMARY KEY (idSessions))
;


-- -----------------------------------------------------
-- Table HUWebshop.Buids
-- -----------------------------------------------------
DROP TABLE IF EXISTS Buids CASCADE ;

CREATE TABLE IF NOT EXISTS Buids (
  buids VARCHAR(255) NOT NULL,
  Visitors_idVisitors SERIAL NOT NULL,
  Sessions_idSessions SERIAL NOT NULL,
  PRIMARY KEY (buids),
  CONSTRAINT fk_Buids_Visitors
    FOREIGN KEY (Visitors_idVisitors)
    REFERENCES Visitors (idVisitors),
  CONSTRAINT fk_Buids_Sessions
    FOREIGN KEY (Sessions_idSessions)
    REFERENCES Sessions (idSessions))
;

-- -----------------------------------------------------
-- Table `HUWebshop`.`events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS  events CASCADE ;

CREATE TABLE IF NOT EXISTS events (
  Products_idProducts VARCHAR(255) NOT NULL,
  Sessions_idSessions SERIAL NOT NULL,
  Event VARCHAR(255) NULL,
  CONSTRAINT fk_events_Products1
    FOREIGN KEY (Products_idProducts)
    REFERENCES Products (idProducts),
  CONSTRAINT fk_events_Sessions1
    FOREIGN KEY (Sessions_idSessions)
    REFERENCES Sessions (idSessions))
;


-- -----------------------------------------------------
-- Table `HUWebshop`.`order`
-- -----------------------------------------------------
DROP TABLE IF EXISTS orders CASCADE ;

CREATE TABLE IF NOT EXISTS orders (
  Products_idProducts VARCHAR(255) NOT NULL,
  Sessions_idSessions SERIAL NOT NULL,
  Amount INT NOT NULL,
  CONSTRAINT fk_orders_Products1
    FOREIGN KEY (Products_idProducts)
    REFERENCES Products (idProducts),
  CONSTRAINT fk_orders_Sessions1
    FOREIGN KEY (Sessions_idSessions)
    REFERENCES Sessions (idSessions))
;


-- -----------------------------------------------------
-- Table `HUWebshop`.`viewed_before`
-- -----------------------------------------------------
DROP TABLE IF EXISTS viewed_before CASCADE ;

CREATE TABLE IF NOT EXISTS viewed_before (
  Visitors_idVisitors SERIAL NOT NULL,
  Products_idProducts VARCHAR(255) NOT NULL,
  Timedate timestamp NULL,
  CONSTRAINT fk_viewed_before_Products1
    FOREIGN KEY (Products_idProducts)
    REFERENCES Products (idProducts),
  CONSTRAINT fk_viewed_before_Visitors1
    FOREIGN KEY (Visitors_idVisitors)
    REFERENCES Visitors (idVisitors))
;


-- -----------------------------------------------------
-- Table `HUWebshop`.`Category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS Category CASCADE ;

CREATE TABLE IF NOT EXISTS Category (
  idCategory BIGINT NOT NULL,
  Products_idProducts VARCHAR(255) NOT NULL,
  _name VARCHAR(255) NULL,
  PRIMARY KEY (idCategory),
  CONSTRAINT fk_Category_Products1
    FOREIGN KEY (Products_idProducts)
    REFERENCES Products (idProducts))
;


-- -----------------------------------------------------
-- Table `HUWebshop`.`Subcategory`
-- -----------------------------------------------------
DROP TABLE IF EXISTS  Subcategory CASCADE;

CREATE TABLE IF NOT EXISTS Subcategory (
  idSubcategory BIGINT NOT NULL,
  Category_idCategory BIGINT NOT NULL,
  name VARCHAR(255) NULL,
  leveldepth INT NULL,
  PRIMARY KEY (idSubcategory),
  CONSTRAINT fk_Subcategory_Category1
    FOREIGN KEY (Category_idCategory)
    REFERENCES Category (idCategory))
;


-- -----------------------------------------------------
-- Table `HUWebshop`.`Similars`
-- -----------------------------------------------------
DROP TABLE IF EXISTS  Similars CASCADE;

CREATE TABLE IF NOT EXISTS Similars (
  Visitors_idVisitors SERIAL NOT NULL,
  Products_idProducts VARCHAR(255) NOT NULL,
  CONSTRAINT fk_Similars_Visitors1
    FOREIGN KEY (Visitors_idVisitors)
    REFERENCES Visitors (idVisitors),
  CONSTRAINT fk_Similars_Products1
    FOREIGN KEY (Products_idProducts)
    REFERENCES Products (idProducts))
;


-- -----------------------------------------------------
-- Table `HUWebshop`.`Has_sale`
-- -----------------------------------------------------
DROP TABLE IF EXISTS  Has_sale CASCADE;

create type TypeSales as enum ('Korting', '1Plus1');
CREATE TABLE IF NOT EXISTS Has_sale (
  Sessions_idSessions SERIAL NOT NULL,
  Products_idProducts VARCHAR(255) NOT NULL,
  TypeSale TypeSales NULL,
  AmountKorting INT NULL,
  CONSTRAINT fk_Has_sale_Sessions1
    FOREIGN KEY (Sessions_idSessions)
    REFERENCES Sessions (idSessions),
  CONSTRAINT fk_Has_sale_Products1
    FOREIGN KEY (Products_idProducts)
    REFERENCES Products (idProducts))
;


-- -----------------------------------------------------
-- Table `HUWebshop`.`Properties`
-- -----------------------------------------------------
DROP TABLE IF EXISTS  Properties CASCADE ;

CREATE TABLE IF NOT EXISTS Properties (
  Products_idProducts VARCHAR(255) NOT NULL,
  Properties VARCHAR(255) NOT NULL,
  CONSTRAINT fk_Properties_Products1
    FOREIGN KEY (Products_idProducts)
    REFERENCES Products (idProducts))
;

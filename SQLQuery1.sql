
-- Create Database
CREATE DATABASE FlaskAuthDB;
GO

-- Use the Database
USE FlaskAuthDB;
GO

-- Create Users Table
CREATE TABLE Users (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(100) UNIQUE NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    PasswordHash NVARCHAR(255) NOT NULL
);
GO

DROP TABLE Users; 
SELECT * FROM Users; 

INSERT INTO Users (Username, Email, PasswordHash) 
VALUES ('Bhuwan', 'bhuwanshrestha187@gmail.com', 'Leoaayan@24');


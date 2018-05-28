 CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
 GRANT ALL PRIVILEGES ON * . * TO 'admin'@'localhost';
 FLUSH PRIVILEGES;

 CREATE DATABASE law;

 USE law;

 CREATE TABLE cases (
   id INT NOT NULL AUTO_INCREMENT,
   name    VARCHAR(255),
   ask     VARCHAR(20),
   sex     VARCHAR(10),
   address VARCHAR(255),
   social  VARCHAR(30),
   job     VARCHAR(20),
   about   VARCHAR(10000),
   PRIMARY KEY (id)
);


 CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
 GRANT ALL PRIVILEGES ON * . * TO 'admin'@'localhost';
 FLUSH PRIVILEGES;

 CREATE DATABASE law CHARACTER SET utf8;

 USE law;

 CREATE TABLE cases (
   id      INT NOT NULL UNIQUE AUTO_INCREMENT,
   name    VARCHAR(255) NOT NULL,
   name1   VARCHAR(255),
   date    DATE NOT NULL,
   ask     VARCHAR(20) NOT NULL,
   birth   DATE,
   sex     VARCHAR(10),
   address VARCHAR(255),
   phone   VARCHAR(20),
   email   VARCHAR(100),
   social  VARCHAR(30),
   job     VARCHAR(20),
   media   VARCHAR(20),
   queue   VARCHAR(25),
   law     VARCHAR(30),
   about   LONGTEXT,
   help    VARCHAR(30),
   student VARCHAR(500),
   open    DATE,
   close   DATE,
   stage   VARCHAR(30),
   present VARCHAR(5),
   result  MEDIUMTEXT,
   appeal  VARCHAR(30),
   client  VARCHAR(30),
   info    MEDIUMTEXT,
   comment LONGTEXT,
   PRIMARY KEY (id)
);


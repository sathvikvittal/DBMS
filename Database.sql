DROP DATABASE IF EXISTS E_COMMERCE;
CREATE DATABASE E_COMMERCE;
USE E_COMMERCE;

DROP TABLE IF EXISTS USER;
CREATE TABLE USER(USER_ID VARCHAR(50) PRIMARY KEY,
FIRSTNAME VARCHAR(30),
MIDDLENAME VARCHAR(30),
LASTNAME VARCHAR(30),
GENDER ENUM("MALE","FEMALE"),
PASSWD VARCHAR(40),
EMAIL VARCHAR(40),
PHONENO INT,
ADDR VARCHAR(100)
);

DROP TABLE IF EXISTS SELLER;
CREATE TABLE SELLER(SELLER_ID VARCHAR(50) PRIMARY KEY,
FIRSTNAME VARCHAR(30),
MIDDLENAME VARCHAR(30),
LASTNAME VARCHAR(30),
PASSWD VARCHAR(40),
EMAIL VARCHAR(40),
SHOP_NAME VARCHAR(50));

DROP TABLE IF EXISTS PRODUCT;
CREATE TABLE PRODUCT(PRODUCT_ID VARCHAR(50) PRIMARY KEY,
SELLER_ID VARCHAR(50),
PRODUCT_NAME VARCHAR(50),
QTY INT,
PRICE INT,
DETAILS VARCHAR(300),
CATEGORY VARCHAR(50)
);

DROP TABLE IF EXISTS REVIEW;
CREATE TABLE REVIEW(REVIEW_ID VARCHAR(50) PRIMARY KEY,
PRODUCT_ID VARCHAR(50),
USER_ID VARCHAR(50),
RATING INT,
COMMENT VARCHAR(50));

DROP TABLE IF EXISTS ORDERS;
CREATE TABLE ORDERS(ORDER_ID VARCHAR(50) PRIMARY KEY,
PRODUCT_ID VARCHAR(50),
USER_ID VARCHAR(50),
ADDR VARCHAR(300),
PAYMENT_MODE VARCHAR(50),
QTY INT
);

DROP TABLE IF EXISTS SHOPPING_CART;
CREATE TABLE SHOPPING_CART(USER_ID VARCHAR(50),
PRODUCT_ID VARCHAR(50),
QTY INT,
PRIMARY KEY(USER_ID,PRODUCT_ID)
);


ALTER TABLE PRODUCT ADD CONSTRAINT FOREIGN KEY(SELLER_ID) REFERENCES SELLER(SELLER_ID);

ALTER TABLE REVIEW ADD CONSTRAINT FOREIGN KEY(PRODUCT_ID) REFERENCES PRODUCT(PRODUCT_ID);
ALTER TABLE REVIEW ADD CONSTRAINT FOREIGN KEY(USER_ID) REFERENCES USER(USER_ID);

ALTER TABLE ORDERS ADD CONSTRAINT FOREIGN KEY(PRODUCT_ID) REFERENCES PRODUCT(PRODUCT_ID);
ALTER TABLE ORDERS ADD CONSTRAINT FOREIGN KEY(USER_ID) REFERENCES USER(USER_ID);

ALTER TABLE SHOPPING_CART ADD CONSTRAINT FOREIGN KEY(PRODUCT_ID) REFERENCES PRODUCT(PRODUCT_ID);
ALTER TABLE SHOPPING_CART ADD CONSTRAINT FOREIGN KEY(USER_ID) REFERENCES USER(USER_ID);

INSERT INTO USER VALUES
    ("USER_1","ABC","D","EF","MALE","ABC","ABC@gmail.com","424780588","JP NAGAR, BANGALORE"),
    ("USER_2","XYZ","D","LKJ","FEMALE","XYZ","XYZ@gmail.com","85452286","JAYANAGAR, BANGALORE"),
    ("USER_3","NOOB","D","LONG","MALE","NOOB","NOOB@gmail.com","98755125","VIJAYANAGAR, BANGALORE");

INSERT INTO SELLER VALUES
('SELLER_1','MAHESH','SINGH','DALLE','DALLE','DALLE@dalle.com','DALLE ELECTRONICS'),
('SELLER_2','JAMES','RAVINDRA','NAYAK','SELLER_2','JAMES@gmail.com','JAMES STORES');

INSERT INTO PRODUCT VALUES
('P1','SELLER_1','Samsung 4K Ultra HD Smart TV','45','165000','55-inch LED display, 4K resolution, Smart TV functionality with built-in apps, HDR support, multiple HDMI and USB ports.','Television'),
('P2','SELLER_1','Apple MacBook Pro','20','67000','13.3-inch Retina display, Intel Core i5 processor, 8GB RAM, 256GB SSD storage, macOS operating system.','Laptop'),
('P3','SELLER_1','Sony Noise-Canceling Headphones','14','32000','Over-ear design, industry-leading noise-canceling technology, Bluetooth connectivity, long battery life, touch controls.','Headphones'),
('P4','SELLER_2','Dyson V11 Absolute Cordless Vacuum','5','14000','Powerful suction, intelligent cleaning modes, LCD screen display, cordless design, multiple attachments for different surfaces.','Vacuum Cleaner'),
('P5','SELLER_2','Canon EOS Rebel T7i DSLR Camera','10','57000','24.2-megapixel APS-C sensor, DIGIC 7 image processor, 45-point autofocus system, vari-angle touchscreen, Full HD video recording.','Camera');

INSERT INTO REVIEW VALUES
('R1','P1','USER_1','4','Very Noice'),
('R2','P1','USER_3','1','Not fitting through Door'),
('R3','P3','USER_2','4','Good Quality Headphones'),
('R4','P2','USER_2','1','My ironbox is cooler than this');


DELIMITER //

CREATE TRIGGER valid_order
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE product_quantity INT;

    -- Get the quantity from the product table for the corresponding product_id
    SELECT QTY INTO product_quantity
    FROM product
    WHERE product_id = NEW.product_id;

    -- Check if the order quantity is greater than the available quantity in the product table
    IF NEW.qty > product_quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Order quantity exceeds available quantity in product table';
    END IF;
END //

DELIMITER ;
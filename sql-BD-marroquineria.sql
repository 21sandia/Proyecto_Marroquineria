CREATE TABLE status(
id_status serial PRIMARY KEY,
name varchar(30)
);

CREATE TABLE rol(
id_rol serial PRIMARY KEY,
name varchar(30)
);
/*
CREATE drop TABLE people (
id_people int PRIMARY KEY,
fk_id_rol int,
fk_id_status int,
name varchar(30),
last_name varchar(30),
document int,
date_birth date,
phone varchar(10),
address varchar(30),
email varchar(50),
password varchar(50)	
);
ALTER TABLE people
ADD CONSTRAINT FK_rol_people
FOREIGN KEY (fk_id_rol)
REFERENCES rol(id_rol);

ALTER TABLE people
ADD CONSTRAINT FK_status_people
FOREIGN KEY (fk_id_status)
REFERENCES status(id_status);
*/
CREATE TABLE category (
id_category serial PRIMARY KEY,
name varchar(30)
);

CREATE TABLE type_prod (
id_type_prod serial PRIMARY KEY,
fk_id_category int,
name varchar(30)
);

ALTER TABLE type_prod
ADD CONSTRAINT FK_category_type_prod
FOREIGN KEY (fk_id_category)
REFERENCES category(id_category);

CREATE TABLE product(
id_product serial PRIMARY KEY,
fk_id_status int,
fk_id_type_prod int,
name varchar(30),
image varchar(500),
reference varchar(60),
price numeric(10,2)
);

ALTER TABLE product
ADD CONSTRAINT FK_status_product
FOREIGN KEY (fk_id_status)
REFERENCES status(id_status);

ALTER TABLE product
ADD CONSTRAINT FK_type_prod_product
FOREIGN KEY (fk_id_type_prod)
REFERENCES type_prod(id_type_prod);

CREATE TABLE detail_prod(
id_detail_prod serial PRIMARY KEY,
fk_id_product int,
registration_date date,
color varchar(30),
size_p varchar(50),
material varchar(40),
quantity int
);

ALTER TABLE detail_prod
ADD CONSTRAINT FK_product_detail_prod
FOREIGN KEY (fk_id_product)
REFERENCES product(id_product);

CREATE TABLE sale(
id_sale serial PRIMARY KEY,
fk_id_product int,
date_sale date,
quantity int,
total numeric(10,2)
);

ALTER TABLE sale
ADD CONSTRAINT FK_product_sale
FOREIGN KEY (fk_id_product)
REFERENCES product(id_product);

CREATE TABLE detail_sale (
id_detail_sale serial PRIMARY KEY,
fk_id_sale int,
customer_name varchar(50),
quantity int,
price_unit NUMERIC(10, 2),
total NUMERIC(10, 2)
);

ALTER TABLE detail_sale
ADD CONSTRAINT FK_sale_detail_sale
FOREIGN KEY (fk_id_sale)
REFERENCES sale(id_sale);
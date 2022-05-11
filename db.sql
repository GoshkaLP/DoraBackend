CREATE TABLE "Users" (
  "id" SERIAL PRIMARY KEY,
  "email" varchar(50) NOT NULL,
  "password" varchar(100) NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "UsersTokensSalt" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "salt" varchar(7) NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "Roles" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(50) NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "UsersRoles" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "role_id" int NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "Manufacturers" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(50) NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "UsersManufacturers" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "manufacturer_id" int NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "UsersServiceCenter" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "service_center_id" int NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "ProductTypes" (
  "id" SERIAL PRIMARY KEY,
  "manufacturer_id" int NOT NULL,
  "name" varchar(50) NOT NULL,
  "warranty_period" int NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "ProductModel" (
  "id" SERIAL PRIMARY KEY,
  "manufacturer_id" int NOT NULL,
  "name" varchar(50) NOT NULL,
  "product_type_id" int NOT NULL,
  "photo" bytea NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "ProductUnit" (
  "id" SERIAL PRIMARY KEY,
  "model_id" int NOT NULL,
  "serial_number" varchar(50) NOT NULL,
  "salt" varchar(10) NOT NULL,
  "assigned" boolean NOT NULL DEFAULT false,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "ServiceCenter" (
  "id" SERIAL PRIMARY KEY,
  "manufacturer_id" int NOT NULL,
  "name" varchar(50) NOT NULL,
  "latitude" decimal NOT NULL,
  "longitude" decimal NOT NULL,
  "address" varchar(50) NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "WarrantyClaim" (
  "id" SERIAL PRIMARY KEY,
  "unit_id" int NOT NULL,
  "service_center_id" int NOT NULL,
  "problem" varchar(255) NOT NULL,
  "status" varchar(255) NOT NULL DEFAULT 'Создана',
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "CustomersProductUnit" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "unit_id" int NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

CREATE TABLE "WarrantyProductUnit" (
  "id" SERIAL PRIMARY KEY,
  "unit_id" int NOT NULL,
  "end_date" timestamp NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  "deleted" boolean DEFAULT false
);

ALTER TABLE "UsersTokensSalt" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "UsersRoles" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "UsersRoles" ADD FOREIGN KEY ("role_id") REFERENCES "Roles" ("id");

ALTER TABLE "UsersManufacturers" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "UsersManufacturers" ADD FOREIGN KEY ("manufacturer_id") REFERENCES "Manufacturers" ("id");

ALTER TABLE "UsersServiceCenter" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "UsersServiceCenter" ADD FOREIGN KEY ("service_center_id") REFERENCES "ServiceCenter" ("id");

ALTER TABLE "ProductModel" ADD FOREIGN KEY ("manufacturer_id") REFERENCES "Manufacturers" ("id");

ALTER TABLE "ProductModel" ADD FOREIGN KEY ("product_type_id") REFERENCES "ProductTypes" ("id");

ALTER TABLE "ProductTypes" ADD FOREIGN KEY ("manufacturer_id") REFERENCES "Manufacturers" ("id");

ALTER TABLE "ProductUnit" ADD FOREIGN KEY ("model_id") REFERENCES "ProductModel" ("id");

ALTER TABLE "ServiceCenter" ADD FOREIGN KEY ("manufacturer_id") REFERENCES "Manufacturers" ("id");

ALTER TABLE "WarrantyClaim" ADD FOREIGN KEY ("unit_id") REFERENCES "ProductUnit" ("id");

ALTER TABLE "WarrantyClaim" ADD FOREIGN KEY ("service_center_id") REFERENCES "ServiceCenter" ("id");

ALTER TABLE "CustomersProductUnit" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "CustomersProductUnit" ADD FOREIGN KEY ("unit_id") REFERENCES "ProductUnit" ("id");

ALTER TABLE "WarrantyProductUnit" ADD FOREIGN KEY ("unit_id") REFERENCES "ProductUnit" ("id");


INSERT INTO "Roles" ("name") VALUES ('customer');

INSERT INTO "Roles" ("name") VALUES ('admin');

INSERT INTO "Roles" ("name") VALUES ('manufacturer');

INSERT INTO "Roles" ("name") VALUES ('service');

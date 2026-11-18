CREATE TABLE "Catalog_attribute" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "slug" varchar(100) NOT NULL UNIQUE);

CREATE TABLE "Catalog_brand" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "slug" varchar(200) NOT NULL UNIQUE, "description" text NOT NULL, "logo" varchar(100) NOT NULL, "is_active" boolean NOT NULL, "created_at" datetime NOT NULL);

CREATE TABLE "Catalog_attributevalue" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "value" varchar(100) NOT NULL, "attribute_id" bigint NOT NULL REFERENCES "Catalog_attribute" ("id"));

CREATE TABLE "Catalog_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "slug" varchar(200) NOT NULL UNIQUE, "description" text NOT NULL, "is_active" boolean NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "parent_id" bigint NULL REFERENCES "Catalog_category" ("id"));

CREATE TABLE "Catalog_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(250) NOT NULL UNIQUE, "slug" varchar(200) NOT NULL UNIQUE, "description" text NOT NULL, "base_price" decimal NOT NULL, "discount_price" decimal NOT NULL, "is_active" boolean NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "brand_id" bigint NULL REFERENCES "Catalog_brand" ("id"), "category_id" bigint NULL REFERENCES "Catalog_category" ("id"));

CREATE TABLE "Catalog_productimage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(100) NOT NULL, "display_order" integer NOT NULL CHECK ("display_order" >= 0), "created_at" datetime NOT NULL, "product_id" bigint NOT NULL REFERENCES "Catalog_product" ("id"));

CREATE TABLE "Catalog_productimage_variant" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "productimage_id" bigint NOT NULL REFERENCES "Catalog_productimage" ("id"), "productvariant_id" bigint NOT NULL REFERENCES "Catalog_productvariant" ("id"));

CREATE TABLE "Catalog_variantattributevalue" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "attribute_id" bigint NOT NULL REFERENCES "Catalog_attribute" ("id"), "attribute_value_id" bigint NOT NULL REFERENCES "Catalog_attributevalue" ("id"), "variant_id" bigint NOT NULL REFERENCES "Catalog_productvariant" ("id"), CONSTRAINT "unique_variant_attribute" UNIQUE ("variant_id", "attribute_id"));

CREATE TABLE "user_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "user_user" ("id"), "group_id" integer NOT NULL REFERENCES "auth_group" ("id"));

CREATE TABLE "user_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "user_user" ("id"), "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"));

CREATE TABLE "cart_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" bigint NOT NULL UNIQUE REFERENCES "user_user" ("id"));

CREATE TABLE "cart_cartitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "price" decimal NOT NULL, "quantity" integer NOT NULL CHECK ("quantity" >= 0), "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "cart_id" bigint NOT NULL REFERENCES "cart_cart" ("id"), "product_variant_id" bigint NOT NULL REFERENCES "Catalog_productvariant" ("id"));

CREATE TABLE "token_blacklist_blacklistedtoken" ("blacklisted_at" datetime NOT NULL, "token_id" bigint NOT NULL UNIQUE REFERENCES "token_blacklist_outstandingtoken" ("id"), "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT);

CREATE TABLE "token_blacklist_outstandingtoken" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" text NOT NULL, "created_at" datetime NULL, "expires_at" datetime NOT NULL, "jti" varchar(255) NOT NULL UNIQUE, "user_id" bigint NULL REFERENCES "user_user" ("id"));

CREATE TABLE "user_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "phone" varchar(15) NOT NULL, "city" varchar(100) NOT NULL, "state" varchar(100) NOT NULL, "postal_code" varchar(20) NOT NULL, "country" varchar(100) NOT NULL, "is_default" boolean NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" bigint NOT NULL REFERENCES "user_user" ("id"), "address" text NOT NULL);

CREATE TABLE "Catalog_productvariant" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "price" decimal NOT NULL, "is_active" boolean NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "product_id" bigint NULL REFERENCES "Catalog_product" ("id"), "stock_quantity" integer NOT NULL CHECK ("stock_quantity" >= 0), "name" varchar(250) NULL);

CREATE TABLE "user_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" boolean NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "is_staff" boolean NOT NULL, "is_active" boolean NOT NULL, "date_joined" datetime NOT NULL, "email" varchar(254) NOT NULL UNIQUE, "phone" varchar(15) NULL);


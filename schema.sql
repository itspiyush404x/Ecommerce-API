#--------------------------
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);

CREATE TABLE "Catalog_attribute" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "slug" varchar(100) NOT NULL UNIQUE);

CREATE TABLE "Catalog_brand" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "slug" varchar(200) NOT NULL UNIQUE, "description" text NOT NULL, "logo" varchar(100) NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL);

CREATE TABLE "Catalog_attributevalue" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "value" varchar(100) NOT NULL, "attribute_id" bigint NOT NULL REFERENCES "Catalog_attribute" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Catalog_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "slug" varchar(200) NOT NULL UNIQUE, "description" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "parent_id" bigint NULL REFERENCES "Catalog_category" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Catalog_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(250) NOT NULL UNIQUE, "slug" varchar(200) NOT NULL UNIQUE, "description" text NOT NULL, "base_price" decimal NOT NULL, "discount_price" decimal NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "brand_id" bigint NULL REFERENCES "Catalog_brand" ("id") DEFERRABLE INITIALLY DEFERRED, "category_id" bigint NULL REFERENCES "Catalog_category" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Catalog_productimage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(100) NOT NULL, "display_order" integer unsigned NOT NULL CHECK ("display_order" >= 0), "created_at" datetime NOT NULL, "product_id" bigint NOT NULL REFERENCES "Catalog_product" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Catalog_productimage_variant" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "productimage_id" bigint NOT NULL REFERENCES "Catalog_productimage" ("id") DEFERRABLE INITIALLY DEFERRED, "productvariant_id" bigint NOT NULL REFERENCES "Catalog_productvariant" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Catalog_variantattributevalue" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "attribute_id" bigint NOT NULL REFERENCES "Catalog_attribute" ("id") DEFERRABLE INITIALLY DEFERRED, "attribute_value_id" bigint NOT NULL REFERENCES "Catalog_attributevalue" ("id") DEFERRABLE INITIALLY DEFERRED, "variant_id" bigint NOT NULL REFERENCES "Catalog_productvariant" ("id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique_variant_attribute" UNIQUE ("variant_id", "attribute_id"));

CREATE INDEX "Catalog_attributevalue_attribute_id_fb777380" ON "Catalog_attributevalue" ("attribute_id");

CREATE INDEX "Catalog_category_parent_id_9bb0704c" ON "Catalog_category" ("parent_id");

CREATE INDEX "Catalog_product_brand_id_d6116e2d" ON "Catalog_product" ("brand_id");

CREATE INDEX "Catalog_product_category_id_0383929c" ON "Catalog_product" ("category_id");

CREATE INDEX "Catalog_productimage_product_id_81def7c7" ON "Catalog_productimage" ("product_id");

CREATE UNIQUE INDEX "Catalog_productimage_variant_productimage_id_productvariant_id_6c66334c_uniq" ON "Catalog_productimage_variant" ("productimage_id", "productvariant_id");

CREATE INDEX "Catalog_productimage_variant_productimage_id_a3d2b37b" ON "Catalog_productimage_variant" ("productimage_id");

CREATE INDEX "Catalog_productimage_variant_productvariant_id_559b7268" ON "Catalog_productimage_variant" ("productvariant_id");

CREATE INDEX "Catalog_variantattributevalue_attribute_id_32a1e4c8" ON "Catalog_variantattributevalue" ("attribute_id");

CREATE INDEX "Catalog_variantattributevalue_attribute_value_id_e50b1385" ON "Catalog_variantattributevalue" ("attribute_value_id");

CREATE INDEX "Catalog_variantattributevalue_variant_id_dd368116" ON "Catalog_variantattributevalue" ("variant_id");

CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);

CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");

CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");

CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");

CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");

CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);

CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");

CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");

CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);

CREATE TABLE "user_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "user_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "user_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "user_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE UNIQUE INDEX "user_user_groups_user_id_group_id_bb60391f_uniq" ON "user_user_groups" ("user_id", "group_id");

CREATE INDEX "user_user_groups_user_id_13f9a20d" ON "user_user_groups" ("user_id");

CREATE INDEX "user_user_groups_group_id_c57f13c0" ON "user_user_groups" ("group_id");

CREATE UNIQUE INDEX "user_user_user_permissions_user_id_permission_id_64f4d5b8_uniq" ON "user_user_user_permissions" ("user_id", "permission_id");

CREATE INDEX "user_user_user_permissions_user_id_31782f58" ON "user_user_user_permissions" ("user_id");

CREATE INDEX "user_user_user_permissions_permission_id_ce49d4de" ON "user_user_user_permissions" ("permission_id");

CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "user_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);

CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");

CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");

CREATE TABLE "cart_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" bigint NOT NULL UNIQUE REFERENCES "user_user" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "cart_cartitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "price" decimal NOT NULL, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "cart_id" bigint NOT NULL REFERENCES "cart_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "product_variant_id" bigint NOT NULL REFERENCES "Catalog_productvariant" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "cart_cartitem_cart_id_370ad265" ON "cart_cartitem" ("cart_id");

CREATE INDEX "cart_cartitem_product_variant_id_adf3444f" ON "cart_cartitem" ("product_variant_id");

CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");

CREATE TABLE "token_blacklist_blacklistedtoken" ("blacklisted_at" datetime NOT NULL, "token_id" bigint NOT NULL UNIQUE REFERENCES "token_blacklist_outstandingtoken" ("id") DEFERRABLE INITIALLY DEFERRED, "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT);

CREATE TABLE "token_blacklist_outstandingtoken" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" text NOT NULL, "created_at" datetime NULL, "expires_at" datetime NOT NULL, "jti" varchar(255) NOT NULL UNIQUE, "user_id" bigint NULL REFERENCES "user_user" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "token_blacklist_outstandingtoken_user_id_83bc629a" ON "token_blacklist_outstandingtoken" ("user_id");

CREATE TABLE "user_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "phone" varchar(15) NOT NULL, "city" varchar(100) NOT NULL, "state" varchar(100) NOT NULL, "postal_code" varchar(20) NOT NULL, "country" varchar(100) NOT NULL, "is_default" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" bigint NOT NULL REFERENCES "user_user" ("id") DEFERRABLE INITIALLY DEFERRED, "address" text NOT NULL);

CREATE INDEX "user_address_user_id_64deb2c7" ON "user_address" ("user_id");

CREATE TABLE "Catalog_productvariant" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "price" decimal NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "product_id" bigint NULL REFERENCES "Catalog_product" ("id") DEFERRABLE INITIALLY DEFERRED, "stock_quantity" integer unsigned NOT NULL CHECK ("stock_quantity" >= 0), "name" varchar(250) NULL);

CREATE INDEX "Catalog_productvariant_product_id_1f4c7774" ON "Catalog_productvariant" ("product_id");

CREATE TABLE "user_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "email" varchar(254) NOT NULL UNIQUE, "phone" varchar(15) NULL);


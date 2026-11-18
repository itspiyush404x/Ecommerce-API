import re
import sqlite3

# Django's own tables you don't need in your diagram
SKIP = ("django_", "auth_group", "auth_permission", "sqlite_")

conn = sqlite3.connect("db.sqlite3")
rows = conn.execute(
    "SELECT name, sql FROM sqlite_master "
    "WHERE type='table' AND sql IS NOT NULL"
).fetchall()

with open("schema_clean.sql", "w") as f:
    for name, sql in rows:
        if name.startswith(SKIP):
            continue
        sql = re.sub(r"\bbool\b", "boolean", sql)
        sql = re.sub(r"\s+unsigned", "", sql, flags=re.I)
        sql = sql.replace(" DEFERRABLE INITIALLY DEFERRED", "")
        f.write(sql + ";\n\n")

print("Done: schema_clean.sql created")
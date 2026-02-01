#!/usr/bin/env python3
import sys
import sqlite3
from pathlib import Path


def main():
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("../backend/db.sqlite3")
    if not db_path.exists():
        raise SystemExit(f"DB not found: {db_path}")

    con = sqlite3.connect(db_path)
    try:
        cur = con.cursor()

        # Show current FK target (should be auth_user -> we will replace with mentor)
        fk = cur.execute("PRAGMA foreign_key_list('django_admin_log')").fetchall()
        if not fk:
            raise SystemExit("django_admin_log has no foreign keys? Aborting.")
        print("Current django_admin_log FKs:", fk)

        if not any(row[2] == "auth_user" and row[3] == "user_id" for row in fk):
            print("django_admin_log.user_id does not reference auth_user; nothing to do.")
            return

        # We cannot reliably migrate old log rows because auth_user.id (int) != mentor.id (char(32))
        old_count = cur.execute("SELECT COUNT(*) FROM django_admin_log").fetchone()[0]
        if old_count:
            print(f"NOTE: deleting {old_count} existing admin log rows (cannot map to mentor ids).")

        cur.execute("PRAGMA foreign_keys=OFF")
        cur.execute("BEGIN")

        # Create replacement table with correct FK to mentor(id)
        cur.execute("""
            CREATE TABLE django_admin_log__new (
              id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              object_id text NULL,
              object_repr varchar(200) NOT NULL,
              action_flag smallint unsigned NOT NULL CHECK (action_flag >= 0),
              change_message text NOT NULL,
              content_type_id integer NULL
                REFERENCES django_content_type (id) DEFERRABLE INITIALLY DEFERRED,
              user_id char(32) NOT NULL
                REFERENCES mentor (id) DEFERRABLE INITIALLY DEFERRED,
              action_time datetime NOT NULL
            )
        """)

        # Keep none of the old rows (see note above)
        # Drop old table and replace
        cur.execute("DROP TABLE django_admin_log")
        cur.execute("ALTER TABLE django_admin_log__new RENAME TO django_admin_log")

        # Recreate helpful indexes (names don’t matter for correctness)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_django_admin_log_content_type_id ON django_admin_log (content_type_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_django_admin_log_user_id ON django_admin_log (user_id)")

        cur.execute("COMMIT")
        cur.execute("PRAGMA foreign_keys=ON")

        # Verify new FK
        fk2 = cur.execute("PRAGMA foreign_key_list('django_admin_log')").fetchall()
        print("New django_admin_log FKs:", fk2)
        print("Done.")
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


if __name__ == "__main__":
    main()
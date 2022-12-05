#!/bin/sh
# Migrate the database first
mongo <<EOF
use db_oncourse_trails;
db.createUser(
  {
    user: "trail_oncourse",
    pwd: "PwDoncourseSatu1Dua3",
    roles: [{ role: "readWrite", db: "db_oncourse_trails" },]
  },
);
use db_oncourse_django_message;
db.createUser(
  {
    user: "django_messages_oncourse",
    pwd: "PwDoncourseSatu1Dua3",
    roles: [{ role: "readWrite", db: "db_oncourse_django_messages" },]
  },
);

EOF
    

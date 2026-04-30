from app.database import SessionLocal, Base, engine
from app.models.models import User

Base.metadata.create_all(bind=engine)

db = SessionLocal()
users = db.query(User).all()
print(f"Found {len(users)} users")
for u in users:
    print(u.email, u.is_admin)
if users:
    users[0].is_admin = True
    db.commit()
    print("First user made admin")
db.close()

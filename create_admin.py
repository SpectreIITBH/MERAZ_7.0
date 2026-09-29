"""Create/promote an admin user. Run once to seed the first admin."""
import sys
sys.path.insert(0, ".")
import database, models
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=database.engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = database.SessionLocal()

# Check if admin already exists
admin = db.query(models.User).filter(models.User.username == "admin").first()
if admin:
    admin.is_admin = True
    db.commit()
    print(f"User 'admin' promoted to admin (team: {admin.team.name})")
else:
    # Create admin team + user
    team = db.query(models.Team).filter(models.Team.name == "ORGANIZERS").first()
    if not team:
        team = models.Team(name="ORGANIZERS")
        db.add(team)
        db.commit()
        db.refresh(team)
    
    hashed = pwd_context.hash("admin123")
    user = models.User(username="admin", hashed_password=hashed, team_id=team.id, is_admin=True)
    db.add(user)
    db.commit()
    print("Created admin user: admin / admin123 (team: ORGANIZERS)")

db.close()

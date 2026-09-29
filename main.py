from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
import jwt
import datetime
import os

import database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="NIGHTJAR API")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "nightjar_super_secret" 

def get_current_user(request: Request, db: Session = Depends(database.get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token.replace("Bearer ", ""), SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            return None
        user = db.query(models.User).filter(models.User.username == username).first()
        return user
    except jwt.PyJWTError:
        return None

def require_admin(request: Request, db: Session = Depends(database.get_db)):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# ─── Page Routes ───────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, user: models.User = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/hub")
    with open("login.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/hub", response_class=HTMLResponse)
async def read_hub(request: Request, user: models.User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/")
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/admin", response_class=HTMLResponse)
async def read_admin(request: Request, user: models.User = Depends(get_current_user)):
    if not user or not user.is_admin:
        return RedirectResponse(url="/")
    with open("admin.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/scoreboard", response_class=HTMLResponse)
async def read_scoreboard():
    with open("scoreboard.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# ─── Auth API ──────────────────────────────────────────────────

@app.post("/api/register")
async def register(
    response: Response,
    team_name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    team = db.query(models.Team).filter(models.Team.name == team_name).first()
    if not team:
        team = models.Team(name=team_name)
        db.add(team)
        db.commit()
        db.refresh(team)
    
    hashed_password = pwd_context.hash(password)
    user = models.User(username=username, hashed_password=hashed_password, team_id=team.id)
    db.add(user)
    db.commit()
    
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    token = jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return {"message": "Registered successfully"}

@app.post("/api/login")
async def login(
    response: Response,
    team_name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if user.team.name != team_name:
        raise HTTPException(status_code=400, detail="Incorrect team name for this user")

    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    token = jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return {"message": "Login successful", "is_admin": user.is_admin}

@app.post("/api/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

# ─── Game API ──────────────────────────────────────────────────

@app.post("/api/submit_flag")
async def submit_flag(room_id: int, flag: str, user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if flag == "TEST_FLAG":
        return {"success": True, "message": "Correct! Room unlocked."}
    return {"success": False, "message": "Incorrect flag. Try again."}

@app.get("/api/me")
async def get_me(user: models.User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {
        "username": user.username,
        "is_admin": user.is_admin,
        "team": user.team.name if user.team else None
    }

# ─── Scoreboard API (public) ──────────────────────────────────

@app.get("/api/scoreboard")
async def get_scoreboard(db: Session = Depends(database.get_db)):
    teams = db.query(models.Team).order_by(models.Team.score.desc(), models.Team.created_at.asc()).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "score": t.score,
            "current_room": t.current_room,
            "members": len(t.users),
            "created_at": t.created_at.isoformat() if t.created_at else None
        }
        for t in teams
    ]

# ─── Admin API (protected) ────────────────────────────────────

@app.get("/api/admin/teams")
async def admin_get_teams(admin: models.User = Depends(require_admin), db: Session = Depends(database.get_db)):
    teams = db.query(models.Team).order_by(models.Team.created_at.asc()).all()
    result = []
    for t in teams:
        members = [{"id": u.id, "username": u.username, "is_admin": u.is_admin} for u in t.users]
        subs = db.query(models.FlagSubmission).filter(models.FlagSubmission.team_id == t.id).count()
        correct = db.query(models.FlagSubmission).filter(
            models.FlagSubmission.team_id == t.id,
            models.FlagSubmission.is_correct == True
        ).count()
        result.append({
            "id": t.id,
            "name": t.name,
            "score": t.score,
            "current_room": t.current_room,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "members": members,
            "total_submissions": subs,
            "correct_submissions": correct
        })
    return result

@app.put("/api/admin/teams/{team_id}/score")
async def admin_update_score(
    team_id: int,
    score: int = Body(..., embed=True),
    admin: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team.score = score
    db.commit()
    return {"message": f"Score updated to {score}", "team": team.name}

@app.put("/api/admin/teams/{team_id}/room")
async def admin_update_room(
    team_id: int,
    room: int = Body(..., embed=True),
    admin: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team.current_room = room
    db.commit()
    return {"message": f"Room updated to {room}", "team": team.name}

@app.delete("/api/admin/teams/{team_id}")
async def admin_delete_team(
    team_id: int,
    admin: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    # Delete users and submissions first
    db.query(models.FlagSubmission).filter(models.FlagSubmission.team_id == team_id).delete()
    db.query(models.User).filter(models.User.team_id == team_id).delete()
    db.delete(team)
    db.commit()
    return {"message": f"Team '{team.name}' deleted"}

@app.put("/api/admin/users/{user_id}/toggle-admin")
async def admin_toggle_admin(
    user_id: int,
    admin: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot modify your own admin status")
    user.is_admin = not user.is_admin
    db.commit()
    return {"message": f"Admin status for '{user.username}' set to {user.is_admin}"}

@app.delete("/api/admin/users/{user_id}")
async def admin_delete_user(
    user_id: int,
    admin: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    db.delete(user)
    db.commit()
    return {"message": f"User '{user.username}' deleted"}

@app.post("/api/admin/reset-scores")
async def admin_reset_scores(
    admin: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    db.query(models.Team).update({models.Team.score: 0, models.Team.current_room: 1})
    db.query(models.FlagSubmission).delete()
    db.commit()
    return {"message": "All scores and progress reset"}

@app.get("/api/admin/stats")
async def admin_stats(
    admin: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    total_teams = db.query(models.Team).count()
    total_users = db.query(models.User).count()
    total_subs = db.query(models.FlagSubmission).count()
    correct_subs = db.query(models.FlagSubmission).filter(models.FlagSubmission.is_correct == True).count()
    top_team = db.query(models.Team).order_by(models.Team.score.desc()).first()
    return {
        "total_teams": total_teams,
        "total_users": total_users,
        "total_submissions": total_subs,
        "correct_submissions": correct_subs,
        "top_team": {"name": top_team.name, "score": top_team.score} if top_team else None
    }


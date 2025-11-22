from flask import Flask, make_response
from flask_migrate import Migrate
from models import Event, Session, Speaker, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/events")
def get_events():
    events = Event.query.all()
    body = [
        {"id": event.id, "name": event.name, "location": event.location}
        for event in events
    ]
    return make_response(body, 200)


@app.route("/events/<int:id>/sessions")
def get_event_sessions(id):
    event = Event.query.get(id)
    if not event:
        return make_response({"error": "Event not found"}, 404)

    sessions = [
        {
            "id": session.id,
            "title": session.title,
            "start_time": (
                session.start_time.isoformat() if session.start_time else None
            ),
        }
        for session in event.sessions
    ]
    return make_response(sessions, 200)


@app.route("/speakers")
def get_speakers():
    speakers = Speaker.query.all()
    body = [{"id": s.id, "name": s.name} for s in speakers]
    return make_response(body, 200)


@app.route("/speakers/<int:id>")
def get_speaker(id):
    speaker = Speaker.query.get(id)
    if not speaker:
        return make_response({"error": "Speaker not found"}, 404)

    body = {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available",
    }
    return make_response(body, 200)


@app.route("/sessions/<int:id>/speakers")
def get_session_speakers(id):
    session = Session.query.get(id)
    if not session:
        return make_response({"error": "Session not found"}, 404)

    speakers = []
    for sp in session.speakers:
        speakers.append(
            {
                "id": sp.id,
                "name": sp.name,
                "bio_text": sp.bio.bio_text if sp.bio else "No bio available",
            }
        )

    return make_response(speakers, 200)

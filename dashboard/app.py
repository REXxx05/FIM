from flask import Flask, render_template, jsonify
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_events, get_baseline

app = Flask(__name__)


@app.route("/")
def index():
    """Main dashboard page."""
    events = get_events(limit=50)
    baseline = get_baseline()
    stats = {
        "total_files": len(baseline),
        "total_events": len(events),
        "critical": len([e for e in events if e["alert_level"] == "CRITICAL"]),
        "warning": len([e for e in events if e["alert_level"] == "WARNING"]),
    }
    return render_template("index.html", events=events, stats=stats)


@app.route("/api/events")
def api_events():
    """API endpoint — returns events as JSON."""
    events = get_events(limit=50)
    return jsonify(events)


@app.route("/api/stats")
def api_stats():
    """API endpoint — returns stats as JSON."""
    events = get_events(limit=100)
    baseline = get_baseline()
    stats = {
        "total_files": len(baseline),
        "total_events": len(events),
        "critical": len([e for e in events if e["alert_level"] == "CRITICAL"]),
        "warning": len([e for e in events if e["alert_level"] == "WARNING"]),
    }
    return jsonify(stats)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

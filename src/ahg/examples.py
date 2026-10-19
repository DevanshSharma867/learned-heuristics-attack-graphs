"""Hand-built tasks used in tests and in docs/learn."""

from .task import Task


def toy_network() -> Task:
    """Three-host network: internet -> web (DMZ) -> app -> db (crown jewel).

    The db only accepts connections from app, and the cheap way in is the
    db admin's password, which can only be stolen with root on web. So the
    cheap plan needs two things at once (a foothold on app AND the password):
    a conjunctive precondition, which is what makes the problem harder than
    a shortest path.
    """
    facts = ["internet", "user@web", "root@web", "user@app", "root@app", "cred:dbadmin", "root@db"]
    actions = [
        ("exploit_web_rce", ["internet"], ["user@web"], 30),
        ("privesc_web", ["user@web"], ["root@web"], 40),
        ("exploit_app_from_web", ["user@web"], ["user@app"], 50),
        ("dump_creds_web", ["root@web"], ["cred:dbadmin"], 20),
        ("privesc_app", ["user@app"], ["root@app"], 20),
        ("login_db_with_cred", ["user@app", "cred:dbadmin"], ["root@db"], 10),
        ("exploit_db_from_app", ["root@app"], ["root@db"], 90),
    ]
    return Task.from_names(facts, ["internet"], ["root@db"], actions)

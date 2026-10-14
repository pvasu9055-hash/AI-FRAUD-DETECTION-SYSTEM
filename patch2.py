import re

src = open("app.py", encoding="utf-8").read()

NEW_AUTH = '''# ============================================================
# AUTHENTICATION (JWT cookie + email OTP via Resend)
# ============================================================

JWT_COOKIE = "access_token"
PENDING_COOKIE_KEY = "pending_email"


def _now():
    return datetime.utcnow()


def _db_exec(conn, sql_q, params=()):
    """Run a query using ? for SQLite and %s for Postgres."""
    if DATABASE_URL:
        sql_q = sql_q.replace("?", "%s")
    return conn.execute(sql_q, params)


def _set_jwt_cookie(response, user_id, name, email):
    token = auth_utils.create_access_token(user_id, name, email)
    response.set_cookie(
        JWT_COOKIE,
        token,
        max_age=auth_utils.JWT_EXPIRY_HOURS * 3600,
        httponly=True,
        samesite="Lax",
        secure=os.environ.get("COOKIE_SECURE", "0") == "1",
    )
    return response


def _issue_otp(email, purpose, name=None, password_hash=None):
    """Create + email an OTP. Returns (ok, error)."""
    otp = auth_utils.generate_otp()
    expires = _now() + timedelta(minutes=auth_utils.OTP_EXPIRY_MINUTES)
    with get_db() as conn:
        _db_exec(conn, "DELETE FROM otp_codes WHERE email = ? AND purpose = ?", (email, purpose))
        _db_exec(
            conn,
            """INSERT INTO otp_codes
               (email, purpose, otp_hash, name, password_hash, expires_at, attempts, created_at)
               VALUES (?, ?, ?, ?, ?, ?, 0, ?)""",
            (
                email,
                purpose,
                auth_utils.hash_otp(email, otp),
                name,
                password_hash,
                expires.isoformat(timespec="seconds"),
                _now().isoformat(timespec="seconds"),
            ),
        )
    return auth_utils.send_otp_email(email, name, otp, purpose)


@app.route("/register", methods=["GET", "POST"])
def register():
    if getattr(g, "user", None):
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not name or not email or not password:
            flash("Please fill in every field.", "error")
        elif len(password) < 8:
            flash("Use a password with at least 8 characters.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        else:
            with get_db() as conn:
                existing = _db_exec(conn, "SELECT id FROM users WHERE email = ?", (email,)).fetchone()
            if existing:
                flash("An account with that email already exists.", "error")
            else:
                ok, err = _issue_otp(email, "register", name, generate_password_hash(password))
                if ok:
                    session.clear()
                    session[PENDING_COOKIE_KEY] = email
                    session["pending_purpose"] = "register"
                    flash("We emailed you a 6-digit code.", "info")
                    return redirect(url_for("verify_otp"))
                app.logger.error("OTP email failed: %s", err)
                flash("Could not send the verification email. Try again.", "error")

    return render_template("auth.html", mode="register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if getattr(g, "user", None):
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with get_db() as conn:
            user = _db_exec(conn, "SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            ok, err = _issue_otp(email, "login", user["name"])
            if ok:
                session.clear()
                session[PENDING_COOKIE_KEY] = email
                session["pending_purpose"] = "login"
                session["next_url"] = request.args.get("next", "")
                flash("We emailed you a 6-digit code.", "info")
                return redirect(url_for("verify_otp"))
            app.logger.error("OTP email failed: %s", err)
            flash("Could not send the verification email. Try again.", "error")
        else:
            flash("Invalid email or password.", "error")

    return render_template("auth.html", mode="login")


@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    email = session.get(PENDING_COOKIE_KEY)
    purpose = session.get("pending_purpose")
    if not email or purpose not in ("register", "login"):
        return redirect(url_for("login"))

    if request.method == "POST":
        code = request.form.get("otp", "").strip()

        with get_db() as conn:
            row = _db_exec(
                conn,
                "SELECT * FROM otp_codes WHERE email = ? AND purpose = ?",
                (email, purpose),
            ).fetchone()

            if not row:
                flash("No active code. Request a new one.", "error")
            elif _now() > datetime.fromisoformat(row["expires_at"]):
                flash("That code has expired. Request a new one.", "error")
            elif row["attempts"] >= auth_utils.OTP_MAX_ATTEMPTS:
                flash("Too many attempts. Request a new code.", "error")
            elif not auth_utils.verify_otp_hash(email, code, row["otp_hash"]):
                _db_exec(conn, "UPDATE otp_codes SET attempts = attempts + 1 WHERE id = ?", (row["id"],))
                flash("Incorrect code.", "error")
            else:
                # Code is correct.
                if purpose == "register":
                    try:
                        if DATABASE_URL:
                            cur = conn.execute(
                                """INSERT INTO users (name, email, password_hash, created_at)
                                   VALUES (%s, %s, %s, %s) RETURNING id""",
                                (row["name"], email, row["password_hash"],
                                 _now().isoformat(timespec="seconds") + "Z"),
                            )
                            user_id = cur.fetchone()["id"]
                        else:
                            cur = conn.execute(
                                """INSERT INTO users (name, email, password_hash, created_at)
                                   VALUES (?, ?, ?, ?)""",
                                (row["name"], email, row["password_hash"],
                                 _now().isoformat(timespec="seconds") + "Z"),
                            )
                            user_id = cur.lastrowid
                    except (sqlite3.IntegrityError, psycopg.errors.UniqueViolation):
                        flash("An account with that email already exists.", "error")
                        return redirect(url_for("login"))
                    user_name = row["name"]
                else:
                    user = _db_exec(conn, "SELECT * FROM users WHERE email = ?", (email,)).fetchone()
                    user_id, user_name = user["id"], user["name"]

                _db_exec(conn, "DELETE FROM otp_codes WHERE email = ? AND purpose = ?", (email, purpose))

                target = session.get("next_url", "")
                if not target.startswith("/") or target.startswith("//"):
                    target = url_for("home")
                session.clear()
                response = make_response(redirect(target))
                return _set_jwt_cookie(response, user_id, user_name, email)

    return render_template("auth.html", mode="otp", pending_email=email)


@app.route("/resend-otp", methods=["POST"])
def resend_otp():
    email = session.get(PENDING_COOKIE_KEY)
    purpose = session.get("pending_purpose")
    if not email or purpose not in ("register", "login"):
        return redirect(url_for("login"))

    with get_db() as conn:
        row = _db_exec(
            conn,
            "SELECT * FROM otp_codes WHERE email = ? AND purpose = ?",
            (email, purpose),
        ).fetchone()

    if not row:
        return redirect(url_for("login"))

    # Cooldown: one resend per 30 seconds.
    sent_at = datetime.fromisoformat(row["created_at"])
    if (_now() - sent_at).total_seconds() < 30:
        flash("Please wait 30 seconds before requesting another code.", "error")
        return redirect(url_for("verify_otp"))

    ok, err = _issue_otp(email, purpose, row["name"], row["password_hash"])
    flash("A new code was sent." if ok else "Could not send the email. Try again.", "info" if ok else "error")
    if not ok:
        app.logger.error("OTP resend failed: %s", err)
    return redirect(url_for("verify_otp"))


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    response = make_response(redirect(url_for("login")))
    response.delete_cookie(JWT_COOKIE)
    return response

'''

# 1. replace the auth section
start = src.index("# ============================================================\n# AUTHENTICATION")
end = src.index("# ============================================================\n# HOME PAGE")
src = src[:start] + NEW_AUTH + src[end:]

# 2. replace the require_login guard
NEW_GUARD = '''@app.before_request
def require_login():
    g.user = None
    payload = auth_utils.decode_access_token(request.cookies.get(JWT_COOKIE))
    if payload:
        g.user = payload
        session["user_id"] = int(payload["sub"])
        session["user_name"] = payload.get("name")
        session["user_email"] = payload.get("email")

    public_endpoints = {"login", "register", "verify_otp", "resend_otp", "logout", "static", "health"}
    if request.endpoint in public_endpoints or request.endpoint is None:
        return None
    if not g.user:
        session.pop("user_id", None)
        if request.path.startswith("/api/") or request.is_json or request.path in {"/predict", "/demo_predict", "/batch_predict", "/history/clear"}:
            return jsonify({"error": "Authentication required. Please log in."}), 401
        return redirect(url_for("login", next=request.path))
    return None
'''
g_start = src.index("@app.before_request\ndef require_login():")
g_end = src.index("# ============================================================\n# CONFIGURATION")
src = src[:g_start] + NEW_GUARD + "\n" + src[g_end:]

# 3. import g
src = src.replace("redirect, url_for,session, flash", "redirect, url_for, session, flash, g", 1)

open("app.py", "w", encoding="utf-8").write(src)
print("auth section replaced")


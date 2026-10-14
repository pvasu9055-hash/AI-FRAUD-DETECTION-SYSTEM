p = "templates/auth.html"
src = open(p, encoding="utf-8-sig").read()

# 1. heading + subtitle
src = src.replace(
    "{{ 'Create your account' if mode == 'register' else 'Welcome back' }}",
    "{{ 'Create your account' if mode == 'register' else ('Verify your email' if mode == 'otp' else 'Welcome back') }}",
    1,
)
src = src.replace(
    "{{ 'Register to access the fraud analytics dashboard.' if mode == 'register'\n                   else 'Sign in to continue to your fraud analytics dashboard.' }}",
    "{% if mode == 'otp' %}Enter the 6-digit code we sent to {{ pending_email }}.{% elif mode == 'register' %}Register to access the fraud analytics dashboard.{% else %}Sign in to continue to your fraud analytics dashboard.{% endif %}",
    1,
)

# 2. flash messages with categories
src = src.replace(
    "{% with messages = get_flashed_messages() %}\n                {% for message in messages %}\n                    <div class=\"alert\">{{ message }}</div>\n                {% endfor %}\n            {% endwith %}",
    "{% with messages = get_flashed_messages(with_categories=true) %}\n                {% for category, message in messages %}\n                    <div class=\"alert {{ 'info' if category == 'info' else '' }}\">{{ message }}</div>\n                {% endfor %}\n            {% endwith %}",
    1,
)

# 3. info alert style
src = src.replace(
    "        .security {",
    "        .alert.info {\n            border-color: #1e3a8a;\n            background: #172554;\n            color: #bfdbfe;\n        }\n\n        .security {",
    1,
)

# 4. wrap the existing form so OTP mode shows its own form
otp_form = '''{% if mode == 'otp' %}
            <form method="post" action="{{ url_for('verify_otp') }}" autocomplete="off">
                <label for="otp">Verification code</label>
                <input
                    id="otp"
                    name="otp"
                    type="text"
                    inputmode="numeric"
                    pattern="[0-9]{6}"
                    maxlength="6"
                    placeholder="123456"
                    autocomplete="one-time-code"
                    required
                    autofocus
                >
                <button class="submit" type="submit">Verify and continue →</button>
            </form>
            <form method="post" action="{{ url_for('resend_otp') }}">
                <div class="switch">
                    Did not get it?
                    <button type="submit" style="background:none;border:0;padding:0;color:#67e8f9;font-weight:700;cursor:pointer;font-size:12px;">Resend code</button>
                </div>
            </form>
            <div class="switch"><a href="{{ url_for('login') }}">Back to sign in</a></div>
            {% else %}
            <form method="post" autocomplete="on">'''
src = src.replace('<form method="post" autocomplete="on">', otp_form, 1)

# close the else after the original form's switch block
src = src.replace(
    "                {{ 'Sign in' if mode == 'register' else 'Create account' }}\n                </a>\n            </div>",
    "                {{ 'Sign in' if mode == 'register' else 'Create account' }}\n                </a>\n            </div>\n            {% endif %}",
    1,
)

open(p, "w", encoding="utf-8").write(src)
print("auth.html patched")

import re, shutil
src_app = open("app.py", encoding="utf-8").read()
m = re.search(r'@app\.route\(\s*["\']/logout["\']([^)]*)\)', src_app)
post_only = bool(m and "POST" in m.group(1) and "GET" not in m.group(1))
print("logout route:", m.group(0) if m else "NOT FOUND", "| post_only:", post_only)

p = "templates/index.html"
shutil.copy(p, "index_before_logout.html")
src = open(p, encoding="utf-8-sig").read()
if "fs-logout" in src:
    print("already patched")
else:
    css = """
  .fs-user{display:flex;align-items:center;gap:10px;margin-left:16px}
  .fs-name{color:#9fb3c8;font-size:13px}
  .fs-logout{display:inline-block;padding:9px 18px;border-radius:10px;border:1px solid #ef4444;background:linear-gradient(180deg,#ef4444,#b91c1c);color:#fff;font-weight:700;font-size:13px;cursor:pointer;text-decoration:none;box-shadow:0 10px 20px -8px rgba(239,68,68,.6);transition:transform .2s,box-shadow .2s}
  .fs-logout:hover{transform:translateY(-2px);box-shadow:0 16px 26px -8px rgba(239,68,68,.8)}
"""
    if post_only:
        btn = '<form method="post" action="{{ url_for(\'logout\') }}" style="margin:0"><button class="fs-logout" type="submit">Logout</button></form>'
    else:
        btn = '<a class="fs-logout" href="{{ url_for(\'logout\') }}">Logout</a>'
    chip = '<div class="fs-user"><span class="fs-name">{{ session.get(\'name\', \'\') }}</span>' + btn + '</div>'
    if "</style>" in src:
        src = src.replace("</style>", css + "</style>", 1)
    src = src.replace("</header>", chip + "</header>", 1)
    open(p, "w", encoding="utf-8").write(src)
    print("logout button added")

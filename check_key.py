from dotenv import dotenv_values
v = dotenv_values(".env").get("RESEND_API_KEY") or ""
print("starts with re_:", v.startswith("re_"))
print("has quotes:", '"' in v or "'" in v)
print("has spaces:", v != v.strip() or " " in v)
print("length:", len(v))

import jinja2
s = open("templates/auth.html", encoding="utf-8").read()
jinja2.Environment().parse(s)
print("template parses OK")
print("flash categories:", "with_categories=true" in s)
print("info css:", ".alert.info" in s)
print("otp blocks:", s.count("mode == 'otp'"))

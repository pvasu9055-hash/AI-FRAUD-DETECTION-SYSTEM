p = "app.py"
src = open(p, encoding="utf-8").read()
old = "from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for, session, flash"
new = old + ", g"
if old in src and new not in src:
    src = src.replace(old, new, 1)
    open(p, "w", encoding="utf-8").write(src)
    print("g import added")
else:
    print("no change")

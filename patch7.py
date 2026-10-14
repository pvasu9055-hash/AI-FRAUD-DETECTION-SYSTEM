import shutil
p = "templates/index.html"
src = open(p, encoding="utf-8-sig").read()
if "/* DASH-3D */" in src:
    print("already patched")
else:
    shutil.copy(p, "index_before_3d.html")
    css = """
  /* DASH-3D */
  body{background:radial-gradient(1200px 700px at 10% -10%,#1e3a8a 0%,transparent 60%),radial-gradient(1000px 700px at 100% 0%,#0e7490 0%,transparent 55%),radial-gradient(900px 600px at 50% 120%,#6d28d9 0%,transparent 55%),#050816 !important;background-attachment:fixed !important}
  header{background:linear-gradient(135deg,rgba(37,99,235,.35),rgba(6,182,212,.18)) !important;backdrop-filter:blur(14px);border:1px solid rgba(103,232,249,.25) !important;border-radius:18px;box-shadow:0 25px 50px -20px rgba(0,0,0,.8),0 0 40px rgba(34,211,238,.15)}
  header .logo{background:linear-gradient(135deg,#2563eb,#22d3ee) !important;color:#fff;box-shadow:0 14px 30px rgba(37,99,235,.65);animation:d3float 4s ease-in-out infinite}
  header h1{background:linear-gradient(90deg,#fff,#67e8f9,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent !important}
  .live{text-shadow:0 0 12px currentColor;animation:d3pulse 2s ease-in-out infinite}
  .card,.stat{background:linear-gradient(145deg,rgba(30,41,89,.62),rgba(8,15,40,.72)) !important;backdrop-filter:blur(14px);border:1px solid rgba(125,211,252,.22) !important;border-radius:18px !important;box-shadow:0 30px 50px -25px rgba(0,0,0,.85),inset 0 1px 0 rgba(255,255,255,.12),0 0 30px rgba(59,130,246,.10);transition:transform .15s ease-out,box-shadow .25s;will-change:transform;transform-style:preserve-3d}
  .card:hover,.stat:hover{box-shadow:0 40px 60px -25px rgba(0,0,0,.9),inset 0 1px 0 rgba(255,255,255,.2),0 0 45px rgba(34,211,238,.28)}
  .stat{border-top:3px solid #38bdf8 !important}
  .stat.red{border-top-color:#f43f5e !important;box-shadow:0 30px 50px -25px rgba(0,0,0,.85),0 0 40px rgba(244,63,94,.22)}
  .stat.green{border-top-color:#22c55e !important;box-shadow:0 30px 50px -25px rgba(0,0,0,.85),0 0 40px rgba(34,197,94,.22)}
  .stat.yellow{border-top-color:#facc15 !important;box-shadow:0 30px 50px -25px rgba(0,0,0,.85),0 0 40px rgba(250,204,21,.2)}
  .stat .value{background:linear-gradient(90deg,#fff,#67e8f9);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:0 8px 24px rgba(34,211,238,.35)}
  .stat.red .value{background:linear-gradient(90deg,#fff,#fb7185);-webkit-background-clip:text;background-clip:text}
  .stat.green .value{background:linear-gradient(90deg,#fff,#4ade80);-webkit-background-clip:text;background-clip:text}
  .stat.yellow .value{background:linear-gradient(90deg,#fff,#fde047);-webkit-background-clip:text;background-clip:text}
  .title{background:linear-gradient(90deg,#67e8f9,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent}
  .btn{background:linear-gradient(180deg,#3b82f6,#1d4ed8) !important;border:1px solid rgba(147,197,253,.5) !important;color:#fff !important;border-radius:12px !important;font-weight:700;box-shadow:0 16px 26px -12px rgba(37,99,235,.9),inset 0 1px 0 rgba(255,255,255,.3);transition:transform .2s,box-shadow .2s}
  .btn.alt{background:linear-gradient(180deg,#8b5cf6,#6d28d9) !important;box-shadow:0 16px 26px -12px rgba(124,58,237,.9),inset 0 1px 0 rgba(255,255,255,.3)}
  .btn:hover{transform:translateY(-3px);box-shadow:0 24px 34px -12px rgba(34,211,238,.7),inset 0 1px 0 rgba(255,255,255,.4)}
  .btn:active{transform:translateY(1px)}
  .tab{border-radius:10px !important;transition:transform .2s,box-shadow .2s}
  .tab:hover{transform:translateY(-2px)}
  .tab.active{background:linear-gradient(180deg,#22d3ee,#0891b2) !important;color:#04121f !important;box-shadow:0 12px 22px -10px rgba(34,211,238,.8)}
  @keyframes d3float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
  @keyframes d3pulse{50%{opacity:.55}}
  .fx{position:fixed;inset:0;z-index:-1;pointer-events:none;overflow:hidden;perspective:900px}
  .orb{position:absolute;border-radius:50%;filter:blur(70px);opacity:.30;animation:d3drift 16s ease-in-out infinite alternate}
  @keyframes d3drift{to{transform:translate(70px,-50px) scale(1.25)}}
  .cube{position:absolute;width:var(--s);height:var(--s);transform-style:preserve-3d;animation:d3spin var(--d) linear infinite}
  .cube i{position:absolute;inset:0;border:1px solid rgba(103,232,249,.5);background:rgba(34,211,238,.06);box-shadow:inset 0 0 18px rgba(34,211,238,.2)}
  .cube i:nth-child(1){transform:translateZ(calc(var(--s)/2))}
  .cube i:nth-child(2){transform:rotateY(180deg) translateZ(calc(var(--s)/2))}
  .cube i:nth-child(3){transform:rotateY(90deg) translateZ(calc(var(--s)/2))}
  .cube i:nth-child(4){transform:rotateY(-90deg) translateZ(calc(var(--s)/2))}
  .cube i:nth-child(5){transform:rotateX(90deg) translateZ(calc(var(--s)/2))}
  .cube i:nth-child(6){transform:rotateX(-90deg) translateZ(calc(var(--s)/2))}
  @keyframes d3spin{from{transform:rotateX(0) rotateY(0)}to{transform:rotateX(360deg) rotateY(360deg)}}
  @media (prefers-reduced-motion:reduce){.cube,.orb,.live,header .logo{animation:none}}
  @media (max-width:900px){.cube{display:none}}
"""
    faces = "<i></i>" * 6
    cubes = [("70px","22s","4%","60%"),("46px","16s","92%","18%"),("100px","32s","84%","70%"),("34px","12s","14%","8%"),("58px","20s","50%","88%")]
    cube_html = "".join('<div class="cube" style="--s:%s;--d:%s;left:%s;top:%s">%s</div>' % (s, d, l, t, faces) for s, d, l, t in cubes)
    html = """
<div class="fx">
  <div class="orb" style="width:420px;height:420px;left:-100px;top:8%;background:#2563eb"></div>
  <div class="orb" style="width:360px;height:360px;right:-80px;top:40%;background:#06b6d4;animation-delay:-6s"></div>
  <div class="orb" style="width:340px;height:340px;left:35%;bottom:-120px;background:#7c3aed;animation-delay:-10s"></div>
  """ + cube_html + """
</div>
<script>
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var els = document.querySelectorAll('.card, .stat');
  els.forEach(function (el) {
    el.addEventListener('mousemove', function (e) {
      var r = el.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5;
      var y = (e.clientY - r.top) / r.height - 0.5;
      el.style.transform = 'perspective(900px) rotateY(' + (x * 7) + 'deg) rotateX(' + (-y * 7) + 'deg) translateZ(8px)';
    });
    el.addEventListener('mouseleave', function () { el.style.transform = ''; });
  });
  var cubes = document.querySelectorAll('.cube');
  document.addEventListener('mousemove', function (e) {
    var x = e.clientX / window.innerWidth - 0.5;
    var y = e.clientY / window.innerHeight - 0.5;
    cubes.forEach(function (c, i) { c.style.translate = (x * (i + 1) * 16) + 'px ' + (y * (i + 1) * 16) + 'px'; });
  });
})();
</script>
"""
    src = src.replace("</style>", css + "</style>", 1)
    src = src.replace("</body>", html + "</body>", 1)
    open(p, "w", encoding="utf-8").write(src)
    print("dashboard 3D added")

p = "templates/auth.html"
src = open(p, encoding="utf-8-sig").read()

css = """
        /* 3D-FX */
        .shell { transform-style: preserve-3d; transition: transform .15s ease-out; will-change: transform; box-shadow: 0 40px 80px -20px rgba(0,0,0,.7), 0 0 60px rgba(34,211,238,.12); }
        .mark { box-shadow: 0 12px 30px rgba(37,99,235,.55); animation: fsfloat 4s ease-in-out infinite; }
        .feature { transition: transform .25s; }
        .feature:hover { transform: translateX(8px); }
        .formside input { transition: transform .2s, box-shadow .2s; }
        .formside input:focus { transform: translateY(-2px); box-shadow: 0 14px 30px -10px rgba(34,211,238,.45); }
        .submit { box-shadow: 0 18px 30px -12px rgba(37,99,235,.7); transition: transform .2s, box-shadow .2s; }
        .submit:hover { transform: translateY(-3px); box-shadow: 0 26px 40px -12px rgba(34,211,238,.6); }
        .submit:active { transform: translateY(1px); }
        @keyframes fsfloat { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
        .fx { position: fixed; inset: 0; z-index: -1; pointer-events: none; overflow: hidden; perspective: 900px; }
        .orb { position: absolute; border-radius: 50%; filter: blur(60px); opacity: .35; animation: fsdrift 14s ease-in-out infinite alternate; }
        @keyframes fsdrift { to { transform: translate(60px,-40px) scale(1.2); } }
        .cube { position: absolute; width: var(--s); height: var(--s); transform-style: preserve-3d; animation: fsspin var(--d) linear infinite; }
        .cube i { position: absolute; inset: 0; border: 1px solid rgba(103,232,249,.5); background: rgba(34,211,238,.06); box-shadow: inset 0 0 18px rgba(34,211,238,.18); }
        .cube i:nth-child(1) { transform: translateZ(calc(var(--s) / 2)); }
        .cube i:nth-child(2) { transform: rotateY(180deg) translateZ(calc(var(--s) / 2)); }
        .cube i:nth-child(3) { transform: rotateY(90deg) translateZ(calc(var(--s) / 2)); }
        .cube i:nth-child(4) { transform: rotateY(-90deg) translateZ(calc(var(--s) / 2)); }
        .cube i:nth-child(5) { transform: rotateX(90deg) translateZ(calc(var(--s) / 2)); }
        .cube i:nth-child(6) { transform: rotateX(-90deg) translateZ(calc(var(--s) / 2)); }
        @keyframes fsspin { from { transform: rotateX(0deg) rotateY(0deg); } to { transform: rotateX(360deg) rotateY(360deg); } }
        @media (prefers-reduced-motion: reduce) { .cube, .orb, .mark { animation: none; } }
        @media (max-width: 900px) { .shell { transform: none !important; } .cube { display: none; } }
"""

faces = "<i></i><i></i><i></i><i></i><i></i><i></i>"
html = """
<div class="fx">
  <div class="orb" style="width:380px;height:380px;left:-80px;top:10%;background:#2563eb"></div>
  <div class="orb" style="width:320px;height:320px;right:-60px;bottom:5%;background:#06b6d4;animation-delay:-6s"></div>
  <div class="cube" style="--s:70px;--d:22s;left:6%;top:68%">""" + faces + """</div>
  <div class="cube" style="--s:46px;--d:16s;left:90%;top:14%">""" + faces + """</div>
  <div class="cube" style="--s:90px;--d:30s;left:82%;top:72%">""" + faces + """</div>
  <div class="cube" style="--s:34px;--d:12s;left:12%;top:10%">""" + faces + """</div>
</div>
<script>
(function () {
  var s = document.querySelector('.shell');
  if (!s || window.innerWidth < 900 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var cubes = document.querySelectorAll('.cube');
  document.addEventListener('mousemove', function (e) {
    var x = e.clientX / window.innerWidth - 0.5;
    var y = e.clientY / window.innerHeight - 0.5;
    s.style.transform = 'perspective(1400px) rotateY(' + (x * 8) + 'deg) rotateX(' + (-y * 8) + 'deg)';
    cubes.forEach(function (c, i) { c.style.translate = (x * (i + 1) * 14) + 'px ' + (y * (i + 1) * 14) + 'px'; });
  });
  document.addEventListener('mouseleave', function () { s.style.transform = ''; });
})();
</script>
"""

if "/* 3D-FX */" in src:
    print("already patched")
else:
    src = src.replace("</style>", css + "    </style>", 1)
    src = src.replace("</body>", html + "</body>", 1)
    open(p, "w", encoding="utf-8").write(src)
    print("3D UI added")

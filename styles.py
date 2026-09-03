"""Premium SDR visual system inspired by the Research Agent workspace."""

HEADER_HTML = """
<div class="ambient ambient-one"></div>
<div class="ambient ambient-two"></div>

<nav class="topbar">
  <div class="brand-lockup">
    <div class="brand-mark"><span></span><span></span><span></span></div>
    <div><strong>KAUSHIK / SDR</strong><small>OUTREACH INTELLIGENCE WORKSPACE</small></div>
  </div>
  <div class="topbar-actions">
    <span class="system-chip"><i></i> SYSTEM ONLINE</span>
    <span class="version-chip">V4.0</span>
  </div>
</nav>

<section class="hero">
  <div class="hero-copy">
    <div class="eyebrow"><span>✦</span> MULTI-MODEL SALES OUTREACH</div>
    <h1>Outreach that<br><em>earns a reply.</em></h1>
    <p>Three specialist SDR agents draft competing emails. A Groq-powered sales manager
    evaluates the candidates, selects the strongest message, and keeps a human review gate before sending.</p>
    <div class="hero-tags">
      <span>Gemini 3.5 Flash-Lite</span>
      <span>Groq · GPT-OSS 20B</span>
      <span>Human-reviewed sending</span>
    </div>
  </div>
  <div class="pipeline-visual">
    <div class="radar-ring ring-one"></div>
    <div class="radar-ring ring-two"></div>
    <div class="core-node"><b>SDR</b><small>ORCHESTRATOR</small></div>
    <div class="satellite node-pro"><i>01</i><span>PRO</span></div>
    <div class="satellite node-consult"><i>02</i><span>CONSULT</span></div>
    <div class="satellite node-manager"><i>03</i><span>SELECT</span></div>
  </div>
</section>

<section class="capability-strip">
  <article><strong>3</strong><span>Specialist SDR agents</span></article>
  <article><strong>2</strong><span>Live model providers</span></article>
  <article><strong>1</strong><span>Manager-selected winner</span></article>
  <article><strong>SMTP</strong><span>Human-approved delivery</span></article>
</section>
"""

CSS = r"""
:root {
  --bg: #050711;
  --surface: rgba(13, 17, 32, 0.84);
  --surface-solid: #0d1120;
  --surface-2: #11172a;
  --surface-3: #090d19;
  --line: rgba(143, 163, 203, 0.16);
  --line-bright: rgba(134, 114, 255, 0.42);
  --text: #edf1ff;
  --text-soft: #c7cfea;
  --muted: #8f9bb8;
  --violet: #8875ff;
  --violet-2: #5b45e8;
  --cyan: #46e6d7;
  --blue: #6aa8ff;
  --orange: #ffad72;
  --green: #6ee7a2;
  --red: #ff8c93;
  --glow: 0 0 70px rgba(102, 77, 255, 0.17);
}
* { box-sizing: border-box; }
html { background: var(--bg); }
body, .gradio-container {
  color: var(--text) !important;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}
body {
  background:
    linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px),
    radial-gradient(circle at 50% -10%, #18134b 0, transparent 42%),
    var(--bg) !important;
  background-size: 54px 54px, 54px 54px, auto, auto !important;
}
.gradio-container {
  max-width: 1440px !important;
  margin: 0 auto !important;
  padding: 0 38px 36px !important;
  background: transparent !important;
}
footer { display: none !important; }
.ambient {
  position: fixed; width: 360px; height: 360px; border-radius: 50%;
  filter: blur(110px); pointer-events: none; opacity: .17; z-index: 0;
}
.ambient-one { background: #704cff; top: 18%; left: -190px; }
.ambient-two { background: #13d8cc; right: -230px; top: 56%; }
.topbar {
  min-height: 78px; display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid var(--line); position: relative; z-index: 2;
}
.brand-lockup { display:flex; gap:12px; align-items:center; }
.brand-lockup strong { display:block; font-size:12px; letter-spacing:.16em; color:var(--text); }
.brand-lockup small { display:block; color:var(--muted); font-size:8px; letter-spacing:.21em; margin-top:3px; }
.brand-mark {
  width:34px; height:34px; border:1px solid var(--line-bright); border-radius:9px;
  display:grid; grid-template-columns:repeat(3,4px); gap:3px; place-content:center;
  background:linear-gradient(145deg,rgba(134,114,255,.22),rgba(70,230,215,.06));
  box-shadow:0 0 25px rgba(113,87,255,.18);
}
.brand-mark span { height:15px; border-radius:5px; background:var(--violet); }
.brand-mark span:nth-child(2) { height:22px; margin-top:-4px; background:var(--cyan); }
.brand-mark span:nth-child(3) { height:10px; margin-top:5px; }
.topbar-actions { display:flex; gap:9px; align-items:center; }
.system-chip,.version-chip {
  border:1px solid var(--line); border-radius:999px; padding:7px 11px;
  color:var(--muted); font-size:9px; font-weight:800; letter-spacing:.12em;
  background:rgba(10,14,27,.72);
}
.system-chip i { width:6px; height:6px; display:inline-block; border-radius:50%; background:var(--cyan); box-shadow:0 0 12px var(--cyan); margin-right:6px; }
.version-chip { color:var(--violet); }
.hero {
  min-height:410px; display:grid; grid-template-columns:1.15fr .85fr; align-items:center;
  gap:48px; position:relative; z-index:1; padding:48px 32px 36px;
}
.hero-copy { max-width:730px; }
.eyebrow { color:var(--cyan); font-size:10px; font-weight:900; letter-spacing:.19em; margin-bottom:20px; }
.eyebrow span { color:var(--violet); margin-right:7px; }
.hero h1 { margin:0; color:var(--text); font-size:clamp(48px,6.1vw,84px); line-height:.94; letter-spacing:-.066em; font-weight:760; }
.hero h1 em { font-style:normal; background:linear-gradient(110deg,#a99cff 5%,#6f8fff 48%,#4ce6d8 95%); -webkit-background-clip:text; background-clip:text; color:transparent; }
.hero p { color:#a9b3cc; max-width:670px; font-size:16px; line-height:1.7; margin:22px 0 20px; }
.hero-tags { display:flex; flex-wrap:wrap; gap:8px; }
.hero-tags span { color:#aeb9d5; font-size:10px; font-weight:700; letter-spacing:.05em; padding:7px 10px; border:1px solid var(--line); border-radius:7px; background:rgba(14,18,34,.66); }
.pipeline-visual { width:320px; height:320px; justify-self:center; position:relative; display:grid; place-items:center; }
.radar-ring { position:absolute; border:1px solid rgba(134,114,255,.22); border-radius:50%; }
.ring-one { width:205px; height:205px; animation:spin 17s linear infinite; }
.ring-two { width:305px; height:305px; border-style:dashed; animation:spin 28s linear infinite reverse; }
.ring-one::before,.ring-two::after { content:""; position:absolute; width:7px; height:7px; border-radius:50%; background:var(--cyan); box-shadow:0 0 16px var(--cyan); }
.ring-one::before { left:20px; top:35px; }
.ring-two::after { right:43px; bottom:28px; background:var(--violet); box-shadow:0 0 16px var(--violet); }
.core-node { width:118px; height:118px; border-radius:31px; display:grid; place-content:center; text-align:center; background:linear-gradient(145deg,#1a2140,#0b0f1f); border:1px solid var(--line-bright); box-shadow:0 0 70px rgba(112,83,255,.27),inset 0 0 25px rgba(134,114,255,.08); }
.core-node b { font-size:29px; letter-spacing:-.06em; background:linear-gradient(120deg,#fff,#8c7aff); -webkit-background-clip:text; color:transparent; }
.core-node small { color:var(--muted); font-size:7px; letter-spacing:.17em; margin-top:4px; }
.satellite { position:absolute; min-width:90px; padding:9px 11px; display:flex; align-items:center; gap:8px; background:rgba(12,16,31,.92); border:1px solid var(--line); border-radius:10px; box-shadow:0 12px 30px rgba(0,0,0,.28); backdrop-filter:blur(12px); }
.satellite i { font-style:normal; color:var(--cyan); font-size:8px; }
.satellite span { font-size:9px; font-weight:800; letter-spacing:.12em; }
.node-pro { top:31px; left:6px; }
.node-consult { right:-5px; top:116px; }
.node-manager { left:15px; bottom:25px; }
@keyframes spin { to { transform:rotate(360deg); } }
.capability-strip { display:grid; grid-template-columns:repeat(4,1fr); border:1px solid var(--line); background:rgba(9,13,25,.68); border-radius:16px; margin-bottom:26px; backdrop-filter:blur(16px); overflow:hidden; position:relative; z-index:2; }
.capability-strip article { padding:17px 20px; display:flex; align-items:center; gap:12px; border-right:1px solid var(--line); }
.capability-strip article:last-child { border-right:0; }
.capability-strip strong { color:var(--text); font-size:15px; }
.capability-strip span { color:var(--muted); font-size:10px; letter-spacing:.05em; }

#sdr-workspace { position:relative; z-index:2; gap:18px; align-items:flex-start; }
.workspace-panel {
  background:var(--surface) !important; border:1px solid var(--line) !important;
  border-radius:20px !important; padding:24px !important; backdrop-filter:blur(22px);
  box-shadow:0 28px 80px rgba(0,0,0,.25),var(--glow);
}
#brief-panel { position:sticky; top:16px; }
.section-kicker { color:var(--cyan); font-size:9px; font-weight:900; letter-spacing:.18em; }
.section-heading { margin:7px 0 6px; font-size:22px; letter-spacing:-.035em; color:var(--text); }
.section-copy { margin:0 0 18px; color:var(--muted); font-size:11.5px; line-height:1.58; }

.gradio-container label,.gradio-container .label-wrap { color:#aeb8d1 !important; font-size:10px !important; font-weight:800 !important; letter-spacing:.06em !important; }
.gradio-container input,.gradio-container textarea { color:var(--text) !important; background:#090d19 !important; border-color:var(--line) !important; }
.gradio-container input::placeholder,.gradio-container textarea::placeholder { color:#5d6885 !important; }
.gradio-container .wrap,.gradio-container .secondary-wrap { background:#090d19 !important; border-color:var(--line) !important; }
.gradio-container .form { border:0 !important; background:transparent !important; }
#run-sdr { min-height:50px !important; color:#fff !important; font-weight:850 !important; background:linear-gradient(105deg,#674cff,#7d69ff 55%,#437ff5) !important; border:0 !important; border-radius:11px !important; box-shadow:0 13px 28px rgba(96,72,255,.28) !important; transition:transform .2s ease,box-shadow .2s ease !important; }
#run-sdr:hover { transform:translateY(-2px); box-shadow:0 17px 36px rgba(96,72,255,.36) !important; }

.provider-map { display:grid; gap:8px; margin-top:12px; }
.provider-row { display:flex; align-items:center; justify-content:space-between; gap:10px; padding:9px 10px; border:1px solid var(--line); border-radius:10px; background:rgba(8,12,24,.65); }
.provider-row span { color:var(--muted); font-size:10px; }
.provider-row b { color:var(--text-soft); font-size:10px; }

#candidate-output { background:transparent !important; border:0 !important; padding:0 !important; }
.draft-stack { display:grid; gap:14px; }
.draft-card { position:relative; overflow:hidden; background:linear-gradient(145deg,rgba(17,23,42,.96),rgba(10,14,28,.97)); border:1px solid var(--line); border-radius:16px; padding:18px 19px 19px; box-shadow:0 18px 46px rgba(0,0,0,.18); }
.draft-card::before { content:""; position:absolute; inset:0 auto 0 0; width:3px; background:linear-gradient(var(--violet),var(--cyan)); opacity:.65; }
.winner-card { border-color:rgba(70,230,215,.48); box-shadow:0 0 0 1px rgba(70,230,215,.08),0 20px 52px rgba(37,194,181,.09); }
.winner-card::before { width:4px; background:linear-gradient(var(--cyan),var(--violet)); opacity:1; }
.draft-head { display:flex; justify-content:space-between; gap:10px; align-items:flex-start; margin-bottom:14px; }
.agent-name { color:var(--text); font-size:15px; font-weight:850; letter-spacing:-.01em; }
.agent-meta { margin-top:6px; display:flex; gap:6px; flex-wrap:wrap; }
.badge { display:inline-flex; align-items:center; border:1px solid var(--line); border-radius:999px; padding:4px 8px; font-size:8px; font-weight:850; letter-spacing:.09em; text-transform:uppercase; background:rgba(13,18,34,.8); color:var(--muted); }
.badge-gemini { color:#b9c9ff; border-color:rgba(106,168,255,.31); background:rgba(61,98,170,.13); }
.badge-groq { color:#ffd0ad; border-color:rgba(255,173,114,.31); background:rgba(151,84,38,.13); }
.badge-winner { color:#9bf3e7; border-color:rgba(70,230,215,.36); background:rgba(30,139,129,.14); }
.badge-safe { color:#b9c5dd; border-color:rgba(143,163,203,.24); }
.subject-label,.manager-label { color:#74819e; font-size:8px; letter-spacing:.18em; font-weight:900; }
.subject-text { color:#f4f6ff; font-size:14px; font-weight:780; margin:5px 0 12px; line-height:1.45; }
.email-body { border-top:1px solid var(--line); padding-top:13px; color:#c4cde3; font-size:12.5px; line-height:1.72; white-space:normal; }

.manager-card { background:linear-gradient(145deg,#151b33,#0a0e1c); color:var(--text); border:1px solid var(--line-bright); border-radius:16px; padding:19px; box-shadow:0 20px 55px rgba(72,52,190,.16); }
.manager-eyebrow { color:var(--cyan); font-size:8px; letter-spacing:.19em; font-weight:900; }
.manager-title { color:var(--text); font-size:20px; font-weight:800; letter-spacing:-.03em; margin:6px 0 10px; }
.manager-badges { display:flex; gap:6px; flex-wrap:wrap; }
.manager-rule { border-top:1px solid var(--line); margin:16px 0; }
.manager-label { color:#7885a3; }
.manager-copy { color:#bac4db; font-size:12px; line-height:1.65; margin-top:7px; }

.review-box { margin-top:16px; padding-top:16px; border-top:1px solid var(--line); }
.review-heading { color:var(--text); font-size:13px; font-weight:800; margin-bottom:3px; }
.review-copy { color:var(--muted); font-size:10.5px; line-height:1.55; margin-bottom:12px; }
#send-email { min-height:46px !important; background:linear-gradient(105deg,#177e76,#21a396) !important; color:#fff !important; font-weight:850 !important; border:0 !important; border-radius:11px !important; box-shadow:0 12px 26px rgba(22,139,128,.20) !important; }
#email-status textarea { min-height:74px !important; }

.activity { border-radius:12px; padding:11px 13px; font-size:10.5px; border:1px solid rgba(70,230,215,.20); background:rgba(24,101,95,.10); color:#a7ded8; display:flex; align-items:center; gap:8px; margin-top:14px; }
.activity-error { background:rgba(152,51,62,.13); border-color:rgba(255,140,147,.25); color:#ffb1b6; }
.activity-safe { background:rgba(110,121,153,.10); border-color:var(--line); color:#aab4cb; }
.pulse { width:7px; height:7px; border-radius:50%; background:currentColor; opacity:.9; flex:0 0 auto; box-shadow:0 0 10px currentColor; }

.status-strip { display:flex; flex-wrap:wrap; gap:8px; margin:0 0 18px; }
.status-chip { border:1px solid var(--line); border-radius:999px; padding:7px 10px; background:rgba(10,14,27,.72); color:var(--muted); font-size:8px; font-weight:850; letter-spacing:.1em; }
.status-chip.live { color:#9bf3e7; border-color:rgba(70,230,215,.25); }
.status-chip.gemini { color:#b9c9ff; border-color:rgba(106,168,255,.25); }
.status-chip.groq { color:#ffd0ad; border-color:rgba(255,173,114,.25); }
.status-chip.send { color:#d7d0ff; border-color:rgba(136,117,255,.25); }

@media (max-width:1100px) {
  .gradio-container { padding:0 20px 28px !important; }
  .hero { grid-template-columns:1fr; padding:42px 12px 30px; }
  .pipeline-visual { display:none; }
  .capability-strip { grid-template-columns:repeat(2,1fr); }
  .capability-strip article:nth-child(2) { border-right:0; }
  #brief-panel { position:relative; top:auto; }
}
@media (max-width:700px) {
  .gradio-container { padding:0 12px 20px !important; }
  .topbar { min-height:66px; }
  .topbar-actions { display:none; }
  .hero { min-height:auto; padding:32px 4px 24px; }
  .hero h1 { font-size:46px; }
  .hero p { font-size:14px; }
  .capability-strip { grid-template-columns:1fr 1fr; }
  .capability-strip article { padding:13px 12px; }
  .workspace-panel { padding:17px !important; }
}
"""

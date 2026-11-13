// Well Run IT site script: menu, sortable tables, news, IT health check, visit counter.
(() => {
  const SB_URL = "https://mefvxxoytleyfjbwtxix.supabase.co";   // Supabase project "valve-partners" (shared by Eric's sites)
  const SB_KEY = "sb_publishable_Ex6vMImvvkTdQsFYprve7g_awiuqxEs";   // public key: used only to count visits

  // mobile menu
  const btn = document.querySelector(".burger"), nav = document.getElementById("nav");
  if (btn && nav) {
    btn.addEventListener("click", () => { const open = nav.classList.toggle("open"); btn.setAttribute("aria-expanded", open); });
    addEventListener("keydown", (e) => { if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.focus(); } });
  }


  // sortable tables: click a column heading to sort, click again to reverse
  document.querySelectorAll("table.sortable").forEach((t) => {
    const heads = [...t.querySelectorAll("thead th")], body = t.tBodies[0];
    const orig = [...body.rows];
    heads.forEach((th, col) => {
      const b = th.querySelector("button"); if (!b) return;
      b.addEventListener("click", () => {
        const dir = th.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
        heads.forEach((h) => h.removeAttribute("aria-sort")); th.setAttribute("aria-sort", dir);
        const key = (r) => r.cells[col].textContent.trim().toLowerCase();
        orig.slice().sort((x, y) => key(x).localeCompare(key(y), undefined, { numeric: true }) * (dir === "ascending" ? 1 : -1)).forEach((r) => body.appendChild(r));
      });
    });
  });

  // security news and Microsoft 365 status: assets/data/news.json is refreshed hourly by a GitHub Action
  const newsList = document.getElementById("newsList"), m365 = document.querySelector("[data-status]");
  if (newsList || m365) {
    const ago = (iso) => { const m = Math.round((Date.now() - new Date(iso)) / 60000); if (!(m >= 0)) return ""; if (m < 60) return m <= 1 ? "just now" : m + " minutes ago"; const h = Math.round(m / 60); if (h < 24) return h + (h === 1 ? " hour ago" : " hours ago"); const d = Math.round(h / 24); return d + (d === 1 ? " day ago" : " days ago"); };
    fetch("assets/data/news.json?t=" + Math.floor(Date.now() / 600000)).then((r) => r.json()).then((data) => {
      if (newsList) {
        const hours = +newsList.dataset.hours || 0, since = Date.now() - hours * 3600000;
        const items = hours ? (data.items || []).filter((it) => new Date(it.date) >= since) : (data.items || []).slice(0, +newsList.dataset.limit || 6);
        newsList.textContent = "";
        if (!items.length) { const li = document.createElement("li"); li.className = "news-empty"; li.textContent = "Headlines will appear here shortly."; newsList.appendChild(li); }
        items.forEach((it) => {
          const li = document.createElement("li"), a = document.createElement("a"), meta = document.createElement("span");
          a.href = it.link; a.target = "_blank"; a.rel = "noopener"; a.textContent = it.title;
          meta.className = "news-meta"; meta.textContent = it.source + "  \u00b7  " + ago(it.date);
          li.append(meta, a); newsList.appendChild(li);
        });
      }
      document.querySelectorAll("[data-status]").forEach((row) => {
        const d = data[row.dataset.status]; const t = row.querySelector(".sp-t"); if (!t) return;
        const st = (d && d.status) || "Unknown", ok = /^available$/i.test(st), link = st === "Link only", unk = st === "Unknown";
        row.classList.remove("ok", "unk", "warn");
        row.classList.add(ok ? "ok" : (unk || link) ? "unk" : "warn");
        t.textContent = ok ? "No issues reported" : link ? "See their page" : unk ? "Unavailable right now" : st;
        row._d = d || { status: st, notes: [] };
      });
      if (document.getElementById("csView")) cloudStatus(data);
    }).catch(() => { if (newsList) newsList.innerHTML = '<li class="news-empty">Headlines are unavailable right now.</li>'; });
  }

  // Cloud Status page: pick a provider on the left, see it on the right.  Pages that allow it load in a frame;
  // the rest (they block being shown inside other sites) show what their public feed says, plus a button to open them.
  function cloudStatus(data) {
    const rows = [...document.querySelectorAll("#csRows .sp-row")];
    const name = document.getElementById("csName"), state = document.getElementById("csState"), open = document.getElementById("csOpen");
    const frame = document.getElementById("csFrame"), sum = document.getElementById("csSum");
    const up = document.getElementById("csUpdated");
    if (up && data.updated) up.textContent = "Last checked " + new Date(data.updated).toLocaleString("en-US", { hour: "numeric", minute: "2-digit", month: "short", day: "numeric" }) + ".";
    function pick(row, scroll) {
      rows.forEach((r) => r.setAttribute("aria-pressed", r === row ? "true" : "false"));
      const d = row._d || { status: "Unknown", notes: [] }, n = row.dataset.name, link = row.dataset.link;
      name.textContent = n; state.textContent = row.querySelector(".sp-t").textContent;
      state.className = row.classList.contains("ok") ? "ok" : row.classList.contains("warn") ? "warn" : "unk";
      open.href = link; open.hidden = false; open.textContent = "Open " + n + "'s page";
      if (row.dataset.frame === "1") {
        sum.hidden = true; frame.hidden = false;
        if (frame.getAttribute("src") !== link) frame.setAttribute("src", link);
      } else {
        frame.hidden = true; frame.removeAttribute("src"); sum.hidden = false; sum.textContent = "";
        const p = document.createElement("p"); p.className = "cs-why";
        p.textContent = d.status === "Link only" ? n + " doesn't publish a public status feed, and its page can't be shown inside other websites.  Use the button to open it." : n + " doesn't allow its status page to be shown inside other websites, so here's what its public status feed says right now.";
        sum.appendChild(p);
        if (d.status !== "Link only") {
          const h = document.createElement("h3"); h.textContent = /^available$/i.test(d.status) ? "Nothing open right now" : "Open right now"; sum.appendChild(h);
          if ((d.notes || []).length) { const ul = document.createElement("ul"); d.notes.forEach((t) => { const li = document.createElement("li"); li.textContent = t; ul.appendChild(li); }); sum.appendChild(ul); }
          else if (!/^available$/i.test(d.status)) { const q = document.createElement("p"); q.textContent = d.status === "Unknown" ? "We couldn't reach their status feed on the last check." : d.status + ".  Their page has the details."; sum.appendChild(q); }
        }
      }
      try { history.replaceState(null, "", "#" + row.dataset.status); } catch (e) {}
      if (scroll && window.matchMedia("(max-width: 900px)").matches) document.getElementById("csView").scrollIntoView({ behavior: "smooth", block: "start" });
    }
    rows.forEach((r) => r.addEventListener("click", () => pick(r, true)));
    const start = rows.find((r) => "#" + r.dataset.status === location.hash) || rows[0];
    if (start) pick(start, false);
  }

  // news history: the previous two weeks, grouped by day (older than the 48 hours on the main page)
  const hist = document.getElementById("newsHistory");
  if (hist) {
    fetch("assets/data/news-history.json?t=" + Math.floor(Date.now() / 600000)).then((r) => r.json()).then((data) => {
      const cut = Date.now() - 48 * 3600000, days = new Map();
      (data.items || []).filter((it) => new Date(it.date) < cut).forEach((it) => {
        const k = new Date(it.date).toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
        if (!days.has(k)) days.set(k, []); days.get(k).push(it);
      });
      hist.textContent = "";
      if (!days.size) { const p = document.createElement("p"); p.className = "news-empty"; p.textContent = "Older headlines will build up here over the next two weeks."; hist.appendChild(p); return; }
      days.forEach((items, day) => {
        const sec = document.createElement("div"), h = document.createElement("h2"), ol = document.createElement("ol");
        sec.className = "nh-day"; h.textContent = day; ol.className = "news";
        items.forEach((it) => {
          const li = document.createElement("li"), a = document.createElement("a"), meta = document.createElement("span");
          a.href = it.link; a.target = "_blank"; a.rel = "noopener"; a.textContent = it.title;
          meta.className = "news-meta"; meta.textContent = it.source;
          li.append(meta, a); ol.appendChild(li);
        });
        sec.append(h, ol); hist.appendChild(sec);
      });
    }).catch(() => { hist.innerHTML = '<p class="news-empty">Headlines are unavailable right now.</p>'; });
  }

  // IT health check (runs only in the browser; nothing is sent unless the visitor chooses to)
  const qs = document.getElementById("questions");
  if (qs) {
    const answers = {}; const total = qs.querySelectorAll("li").length;
    const num = document.getElementById("gaugeNum"), title = document.getElementById("verdictTitle"), text = document.getElementById("verdictText"), cta = document.getElementById("checkCta");
    qs.addEventListener("click", (e) => {
      const b = e.target.closest("button"); if (!b) return;
      const li = b.closest("li"); li.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", x === b));
      answers[li.dataset.q] = b.dataset.v === "1";
      const done = Object.keys(answers).length, yes = Object.values(answers).filter(Boolean).length;
      num.innerHTML = `${yes}<small> of ${total}</small>`;
      if (done < total) { title.textContent = `${total - done} to go`; text.textContent = "Keep going to see where you stand."; return; }
      const gaps = total - yes;
      title.textContent = gaps === 0 ? "In good shape" : gaps <= 2 ? "A few gaps to close" : "Worth a closer look";
      text.textContent = gaps === 0 ? "Nice work.  A second set of eyes can still confirm it holds up." : `You answered "No" ${gaps} time${gaps > 1 ? "s" : ""}.  Each one is a gap worth closing, and most are quick to fix.`;
      const missed = [...qs.querySelectorAll("li")].filter((li) => answers[li.dataset.q] === false).map((li) => "- " + li.querySelector("p").textContent.trim());
      const msg = `IT health check: ${yes} of ${total}.` + (missed.length ? `\nAnswered "No" to:\n${missed.join("\n")}` : "");
      cta.href = "contact.html?topic=" + encodeURIComponent("A project or assessment") + "&msg=" + encodeURIComponent(msg);
      cta.hidden = false;
    });
  }

  // contact form removed Nov 2026: Bernie (assets/js/bernie.js) handles contact, and nothing is stored in a database.

  // visit counter: one count per page per browser session.  No cookies, no personal data.
  if (!/^(localhost|127\.)/.test(location.hostname)) {
    const path = location.pathname.replace(/index\.html$/, "") || "/";
    let seen = false; try { const k = "wr-hit:" + path; seen = !!sessionStorage.getItem(k); sessionStorage.setItem(k, "1"); } catch (e) {}
    if (!seen) fetch(`${SB_URL}/rest/v1/rpc/count_hit`, { method: "POST", keepalive: true, headers: { apikey: SB_KEY, "Content-Type": "application/json" }, body: JSON.stringify({ p_site: "wellrunit", p_path: path }) }).catch(() => {});
  }
})();

/* services jump bar: highlight the section in view */
(function(){
  var links=[].slice.call(document.querySelectorAll('.jump a[href^="#"]'));
  if(!links.length||!('IntersectionObserver' in window))return;
  var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a;});
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){links.forEach(function(a){a.classList.remove('on');});var a=map[e.target.id];if(a)a.classList.add('on');}
  });},{rootMargin:'-45% 0px -50% 0px'});
  Object.keys(map).forEach(function(id){var s=document.getElementById(id);if(s)io.observe(s);});
})();

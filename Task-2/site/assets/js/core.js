/* HisabCulator core: theme, language (Bangla), navigation and shared helpers */
(function () {
  'use strict';
  var d = document, root = d.documentElement, BN = '০১২৩৪৫৬৭৮৯';

  var LS = {
    get: function (k, f) { try { var v = localStorage.getItem(k); return v === null ? f : v; } catch (e) { return f; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  function mk(tag, cls, text) {
    var el = d.createElement(tag);
    if (cls) el.className = cls;
    if (text !== undefined) el.textContent = text;
    return el;
  }

  var HC = window.HC = {
    $: function (s, r) { return (r || d).querySelector(s); },
    $$: function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); },
    LS: LS,
    mk: mk,
    lang: function () { return root.getAttribute('lang') === 'bn' ? 'bn' : 'en'; },
    L: function (en, bn) { return HC.lang() === 'bn' && bn ? bn : en; },
    /* Bangla digits -> ASCII (so people can type ১২৩) */
    toEn: function (s) { return String(s).replace(/[০-৯]/g, function (c) { return BN.indexOf(c); }); },
    /* ASCII digits -> Bangla, only when Bangla mode is on */
    bnd: function (s) { return HC.lang() === 'bn' ? String(s).replace(/\d/g, function (c) { return BN[c]; }) : String(s); },
    parse: function (v) {
      var s = HC.toEn(v == null ? '' : v).trim().replace(/,/g, '');
      if (s === '' || !/^[-+]?(\d+\.?\d*|\.\d+)$/.test(s)) return NaN;
      return Number(s);
    },
    fmt: function (n, max, min) {
      if (n === null || n === undefined || !isFinite(n)) return '—';
      var a = Math.abs(n);
      if (a !== 0 && (a >= 1e15 || a < 1e-9)) return HC.bnd(n.toExponential(6).replace(/\.?0+e/, 'e'));
      return HC.bnd(n.toLocaleString('en-US', { maximumFractionDigits: max === undefined ? 2 : max, minimumFractionDigits: min || 0 }));
    },
    taka: function (n) { return '৳ ' + HC.fmt(n, 2, 2); },
    /* Render a result box: {label,value,rows:[[k,v]],note} */
    render: function (el, o) {
      el.textContent = '';
      if (!o) return el;
      if (o.value !== undefined) {
        var m = mk('div', 'res-main');
        m.append(mk('span', '', o.label || ''), mk('strong', '', o.value));
        el.append(m);
      }
      if (o.rows && o.rows.length) {
        var dl = mk('dl', 'res-grid');
        o.rows.forEach(function (r) { var dv = mk('div'); dv.append(mk('dt', '', r[0]), mk('dd', '', r[1])); dl.append(dv); });
        el.append(dl);
      }
      if (o.note) el.append(mk('p', 'res-note', o.note));
      return el;
    },
    error: function (el, msg) { el.textContent = ''; if (msg) el.append(mk('p', 'err', msg)); return el; },
    onLang: function (fn) { d.addEventListener('hc:lang', fn); },
    /* Date helpers (UTC based so daylight saving never shifts a day) */
    parseDate: function (s) {
      var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || '');
      if (!m) return null;
      var y = +m[1], mo = +m[2] - 1, da = +m[3], t = new Date(Date.UTC(y, mo, da));
      return t.getUTCMonth() === mo ? { y: y, m: mo, d: da } : null;
    },
    utc: function (o) { return Date.UTC(o.y, o.m, o.d); },
    dayDiff: function (a, b) { return Math.round((HC.utc(b) - HC.utc(a)) / 864e5); },
    ymd: function (a, b) {
      var y = b.y - a.y, m = b.m - a.m, dd = b.d - a.d;
      if (dd < 0) { m--; dd += new Date(Date.UTC(b.y, b.m, 0)).getUTCDate(); }
      if (m < 0) { y--; m += 12; }
      return { y: y, m: m, d: dd };
    },
    fmtDate: function (o, withDay) {
      var opt = { timeZone: 'UTC', day: 'numeric', month: 'long', year: 'numeric' };
      if (withDay) opt.weekday = 'long';
      return new Date(HC.utc(o)).toLocaleDateString(HC.lang() === 'bn' ? 'bn-BD' : 'en-GB', opt);
    },
    today: function () { var t = new Date(); return { y: t.getFullYear(), m: t.getMonth(), d: t.getDate() }; },
    isoDate: function (o) { return o.y + '-' + String(o.m + 1).padStart(2, '0') + '-' + String(o.d).padStart(2, '0'); }
  };

  /* ---------- theme ---------- */
  var themeBtn = HC.$('#theme-toggle');
  function setTheme(t) {
    root.setAttribute('data-theme', t);
    LS.set('hc_theme', t);
    if (themeBtn) themeBtn.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false');
    var meta = HC.$('meta[name=theme-color]');
    if (meta) meta.setAttribute('content', t === 'dark' ? '#0B1120' : '#F8FAFC');
  }
  if (themeBtn) {
    themeBtn.setAttribute('aria-pressed', root.getAttribute('data-theme') === 'dark' ? 'true' : 'false');
    themeBtn.addEventListener('click', function () { setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); });
  }

  /* ---------- language ---------- */
  var digitNodes = [];
  function walkDigits(bn) {
    var skip = /^(SCRIPT|STYLE|TEXTAREA|INPUT|SELECT|OPTION)$/;
    if (!bn) {
      digitNodes.forEach(function (n) { if (n.__en !== undefined && n.parentNode) { n.nodeValue = n.__en; } delete n.__en; });
      digitNodes = [];
      return;
    }
    var w = d.createTreeWalker(d.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentNode;
        if (!p || skip.test(p.nodeName) || (p.closest && p.closest('.nodigit'))) return NodeFilter.FILTER_REJECT;
        return /\d/.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    var n;
    while ((n = w.nextNode())) {
      if (n.__en === undefined) { n.__en = n.nodeValue; digitNodes.push(n); }
      n.nodeValue = n.nodeValue.replace(/\d/g, function (c) { return BN[c]; });
    }
  }
  function applyLang(initial) {
    var bn = HC.lang() === 'bn';
    walkDigits(false);
    HC.$$('[data-bn]').forEach(function (el) {
      if (el.dataset.en === undefined) el.dataset.en = el.textContent;
      el.textContent = bn ? el.dataset.bn : el.dataset.en;
    });
    HC.$$('[data-bn-ph]').forEach(function (el) {
      if (el.dataset.enPh === undefined) el.dataset.enPh = el.getAttribute('placeholder') || '';
      el.setAttribute('placeholder', bn ? el.dataset.bnPh : el.dataset.enPh);
    });
    HC.$$('[data-bn-label]').forEach(function (el) {
      if (el.dataset.enLabel === undefined) el.dataset.enLabel = el.getAttribute('aria-label') || '';
      el.setAttribute('aria-label', bn ? el.dataset.bnLabel : el.dataset.enLabel);
    });
    var lb = HC.$('#lang-toggle');
    if (lb) { lb.textContent = bn ? 'EN' : 'বাংলা'; lb.setAttribute('aria-label', bn ? 'Switch to English' : 'বাংলায় দেখুন'); }
    d.dispatchEvent(new CustomEvent('hc:lang'));
    walkDigits(bn);
  }
  var langBtn = HC.$('#lang-toggle');
  if (langBtn) langBtn.addEventListener('click', function () {
    var next = HC.lang() === 'bn' ? 'en' : 'bn';
    root.setAttribute('lang', next);
    LS.set('hc_lang', next);
    applyLang();
  });
  HC.refreshLang = applyLang;

  /* ---------- navigation ---------- */
  var nav = HC.$('#site-nav'), burger = HC.$('#burger');
  function closeDropdowns(except) {
    HC.$$('.has-dd.open').forEach(function (li) {
      if (li !== except) { li.classList.remove('open'); li.querySelector('.nav-btn').setAttribute('aria-expanded', 'false'); }
    });
  }
  HC.$$('.has-dd > .nav-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var li = btn.parentNode, open = !li.classList.contains('open');
      closeDropdowns(li);
      li.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  d.addEventListener('click', function (e) { if (!e.target.closest('.has-dd')) closeDropdowns(); });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeDropdowns();
      if (nav && nav.classList.contains('open')) { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); burger.focus(); }
    }
  });
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = !nav.classList.contains('open');
      nav.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
    });
  }

  if (root.getAttribute('lang') === 'bn') applyLang(true); else applyLang(true);
})();

/* Generic unit converter (length, weight, temperature). Config is embedded in the page as JSON. */
(function () {
  'use strict';
  var cfgEl = HC.$('#cv-cfg'); if (!cfgEl) return;
  var cfg = JSON.parse(cfgEl.textContent), units = cfg.units;
  var val = HC.$('#cv-val'), from = HC.$('#cv-from'), to = HC.$('#cv-to'), res = HC.$('#cv-res'), all = HC.$('#cv-all');

  function toBase(k, x) {
    if (cfg.type !== 'temp') return x * units.filter(function (u) { return u.k === k; })[0].f;
    return k === 'C' ? x : k === 'F' ? (x - 32) * 5 / 9 : k === 'K' ? x - 273.15 : (x - 491.67) * 5 / 9;
  }
  function fromBase(k, c) {
    if (cfg.type !== 'temp') return c / units.filter(function (u) { return u.k === k; })[0].f;
    return k === 'C' ? c : k === 'F' ? c * 9 / 5 + 32 : k === 'K' ? c + 273.15 : (c + 273.15) * 9 / 5;
  }
  function conv(x, a, b) { return fromBase(b, toBase(a, x)); }
  function name(u) { return HC.L(u.n, u.bn); }
  function num(v) { return HC.fmt(parseFloat(v.toPrecision(10)), 8); }

  function fillOptions() {
    [from, to].forEach(function (sel, i) {
      var keep = sel.value || cfg.def[i];
      sel.textContent = '';
      units.forEach(function (u) { var o = HC.mk('option', '', name(u) + ' (' + u.s + ')'); o.value = u.k; sel.append(o); });
      sel.value = keep;
    });
  }
  function calc() {
    var x = HC.parse(val.value);
    all.textContent = '';
    if (isNaN(x)) { HC.render(res, null); return; }
    var a = from.value, b = to.value, r = conv(x, a, b);
    var ua = units.filter(function (u) { return u.k === a; })[0], ub = units.filter(function (u) { return u.k === b; })[0];
    HC.render(res, { label: HC.fmt(x, 8) + ' ' + ua.s + ' =', value: num(r) + ' ' + ub.s,
      note: cfg.type === 'temp' ? '' : '1 ' + ua.s + ' = ' + num(conv(1, a, b)) + ' ' + ub.s });
    units.forEach(function (u) {
      var tr = HC.mk('tr'); tr.append(HC.mk('td', '', name(u)), HC.mk('td', '', num(conv(x, a, u.k)) + ' ' + u.s));
      all.append(tr);
    });
  }
  HC.$('#cv-swap').addEventListener('click', function () { var t = from.value; from.value = to.value; to.value = t; calc(); });
  [val, from, to].forEach(function (el) { el.addEventListener('input', calc); el.addEventListener('change', calc); });
  HC.onLang(function () { fillOptions(); calc(); });
  fillOptions(); calc();
})();

/* Safe expression evaluator (recursive descent). No eval(), no new Function(). */
(function (g) {
  'use strict';
  var CONST = { pi: Math.PI, e: Math.E };
  var FN = {
    sin: Math.sin, cos: Math.cos, tan: Math.tan, asin: Math.asin, acos: Math.acos, atan: Math.atan,
    ln: Math.log, log: Math.log10, sqrt: Math.sqrt, cbrt: Math.cbrt, abs: Math.abs, exp: Math.exp
  };
  var BNDIG = '০১২৩৪৫৬৭৮৯';

  function fail(code) { var e = new Error(code); e.code = code; throw e; }

  function tokenize(src) {
    var s = String(src)
      .replace(/[০-৯]/g, function (c) { return BNDIG.indexOf(c); })
      .replace(/×|\u00d7/g, '*').replace(/÷/g, '/').replace(/[−–—]/g, '-')
      .replace(/π/g, ' pi ').replace(/√/g, ' sqrt ').replace(/²/g, '^2').replace(/³/g, '^3');
    var t = [], i = 0, c, j;
    while (i < s.length) {
      c = s[i];
      if (/\s/.test(c)) { i++; continue; }
      if (/[0-9.]/.test(c)) {
        j = i; while (j < s.length && /[0-9.]/.test(s[j])) j++;
        var txt = s.slice(i, j);
        if (txt === '.' || txt.split('.').length > 2) fail('syntax');
        t.push({ k: 'n', v: parseFloat(txt) }); i = j; continue;
      }
      if (/[a-zA-Z]/.test(c)) {
        j = i; while (j < s.length && /[a-zA-Z]/.test(s[j])) j++;
        t.push({ k: 'i', v: s.slice(i, j).toLowerCase() }); i = j; continue;
      }
      if ('+-*/^()!%'.indexOf(c) > -1) { t.push({ k: 'o', v: c }); i++; continue; }
      fail('syntax');
    }
    return t;
  }

  function fact(n) {
    if (n < 0 || n !== Math.floor(n) || n > 170) fail('fact');
    var r = 1; for (var i = 2; i <= n; i++) r *= i; return r;
  }

  function evaluate(src, opt) {
    opt = opt || {};
    var deg = opt.angle !== 'rad', T = tokenize(src), p = 0;
    if (!T.length) fail('empty');

    function isOp(v) { return p < T.length && T[p].k === 'o' && T[p].v === v; }
    function startsPrimary() { return p < T.length && (T[p].k === 'n' || T[p].k === 'i' || (T[p].k === 'o' && T[p].v === '(')); }

    function expr() {
      var v = term();
      while (isOp('+') || isOp('-')) {
        var op = T[p++].v, st = p, r = term();
        /* "200 + 10%" means 10% of 200 */
        if (p - st === 2 && T[st].k === 'n' && T[st + 1].v === '%') r = v * r;
        v = op === '+' ? v + r : v - r;
      }
      return v;
    }
    function term() {
      var v = unary();
      for (;;) {
        if (isOp('*')) { p++; v *= unary(); }
        else if (isOp('/')) { p++; var dv = unary(); if (dv === 0) fail('div0'); v /= dv; }
        else if (startsPrimary()) v *= unary();
        else return v;
      }
    }
    function unary() {
      if (isOp('-')) { p++; return -unary(); }
      if (isOp('+')) { p++; return unary(); }
      return power();
    }
    function power() {
      var b = postfix();
      if (isOp('^')) { p++; return Math.pow(b, unary()); }
      return b;
    }
    function postfix() {
      var v = primary();
      while (isOp('!') || isOp('%')) { v = T[p++].v === '!' ? fact(v) : v / 100; }
      return v;
    }
    function primary() {
      var tk = T[p++];
      if (!tk) fail('syntax');
      if (tk.k === 'n') return tk.v;
      if (tk.k === 'o' && tk.v === '(') {
        var v = expr();
        if (isOp(')')) p++; else if (p < T.length) fail('syntax');
        return v;
      }
      if (tk.k === 'i') {
        if (tk.v === 'ans') return opt.ans || 0;
        if (CONST.hasOwnProperty(tk.v)) return CONST[tk.v];
        if (!FN.hasOwnProperty(tk.v)) fail('syntax');
        var a;
        if (isOp('(')) { p++; a = expr(); if (isOp(')')) p++; else if (p < T.length) fail('syntax'); }
        else a = unary();
        return apply(tk.v, a);
      }
      fail('syntax');
    }
    function apply(name, x) {
      if (deg && /^(sin|cos|tan)$/.test(name)) {
        if (name === 'tan' && Math.abs(x % 180) === 90) fail('math');
        x = x * Math.PI / 180;
      }
      var r = FN[name](x);
      if (deg && /^a(sin|cos|tan)$/.test(name)) r = r * 180 / Math.PI;
      return r;
    }

    var res = expr();
    if (p < T.length) fail('syntax');
    if (!isFinite(res) || isNaN(res)) fail('math');
    res = parseFloat(res.toPrecision(12));
    return Object.is(res, -0) ? 0 : res;
  }

  g.MathParse = { evaluate: evaluate };
})(window);

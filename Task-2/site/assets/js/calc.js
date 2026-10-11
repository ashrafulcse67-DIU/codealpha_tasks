/* Basic + scientific calculator UI. Expression text goes through MathParse (no eval). */
(function () {
  'use strict';
  var box = HC.$('[data-calc]'); if (!box) return;
  var sci = box.dataset.calc === 'sci';
  var inp = HC.$('#expr'), out = HC.$('#res'), list = HC.$('#hist-list'), angleBtn = HC.$('#angle');
  var angle = HC.LS.get('hc_angle', 'deg'), ans = 0, fresh = false, hist = [];
  var HK = 'hc_hist_' + box.dataset.calc;
  try { hist = JSON.parse(HC.LS.get(HK, '[]')) || []; } catch (e) { hist = []; }

  function msg(code) {
    return ({
      div0: HC.L('Cannot divide by zero', 'শূন্য দিয়ে ভাগ করা যায় না'),
      math: HC.L('Result is not a valid number', 'ফলাফল বৈধ সংখ্যা নয়'),
      fact: HC.L('Factorial needs a whole number from 0 to 170', 'ফ্যাক্টরিয়ালের জন্য ০ থেকে ১৭০ এর পূর্ণ সংখ্যা দিন'),
      syntax: HC.L('Check the expression', 'এক্সপ্রেশনটি যাচাই করুন')
    })[code] || '';
  }
  function plain(v) { return v.toLocaleString('en-US', { useGrouping: false, maximumFractionDigits: 10 }); }
  function show(text, bad) { out.textContent = text; out.className = bad ? 'bad' : ''; }

  function preview() {
    var s = inp.value.trim();
    if (!s) return show('0');
    try { show(HC.fmt(MathParse.evaluate(s, { angle: angle, ans: ans }), 10)); }
    catch (e) { show(e.code === 'div0' || e.code === 'math' ? msg(e.code) : '', e.code === 'div0' || e.code === 'math'); }
  }
  function equals() {
    var s = inp.value.trim(); if (!s) return;
    try {
      var v = MathParse.evaluate(s, { angle: angle, ans: ans });
      ans = v; hist.unshift({ e: s, r: v }); hist = hist.slice(0, 15);
      HC.LS.set(HK, JSON.stringify(hist));
      inp.value = plain(v); fresh = true; show(HC.fmt(v, 10)); renderHist();
    } catch (e) { show(msg(e.code) || msg('syntax'), true); }
  }
  function insert(v) {
    if (fresh && /^[0-9.(a-zπ√]/i.test(v)) inp.value = '';
    fresh = false;
    var a = inp.selectionStart == null ? inp.value.length : inp.selectionStart, b = inp.selectionEnd == null ? a : inp.selectionEnd;
    inp.setRangeText(v, a, b, 'end'); preview();
  }
  function back() {
    var a = inp.selectionStart, b = inp.selectionEnd;
    if (a === b && a > 0) { inp.setRangeText('', a - 1, a, 'end'); } else if (a !== b) { inp.setRangeText('', a, b, 'end'); }
    fresh = false; preview();
  }
  function renderHist() {
    if (!list) return;
    list.textContent = '';
    if (!hist.length) { var li = HC.mk('li', 'note', HC.L('No calculations yet.', 'এখনও কোনো হিসাব নেই।')); list.append(li); return; }
    hist.forEach(function (h) {
      var li = HC.mk('li'), b = HC.mk('button'); b.type = 'button';
      b.append(HC.mk('small', '', HC.bnd(h.e)), document.createTextNode('= ' + HC.fmt(h.r, 10)));
      b.addEventListener('click', function () { inp.value = plain(h.r); fresh = true; preview(); inp.focus(); });
      li.append(b); list.append(li);
    });
  }
  function setAngle() { if (angleBtn) angleBtn.textContent = angle === 'deg' ? HC.L('Degrees', 'ডিগ্রি') : HC.L('Radians', 'রেডিয়ান'); }

  box.addEventListener('mousedown', function (e) { if (e.target.closest('.key')) e.preventDefault(); });
  box.addEventListener('click', function (e) {
    var k = e.target.closest('.key'); if (!k) return;
    if (k.dataset.v !== undefined) insert(k.dataset.v);
    else if (k.dataset.act === 'clear') { inp.value = ''; fresh = false; preview(); }
    else if (k.dataset.act === 'back') back();
    else if (k.dataset.act === 'eq') equals();
    inp.focus({ preventScroll: true });
  });
  if (angleBtn) angleBtn.addEventListener('click', function () { angle = angle === 'deg' ? 'rad' : 'deg'; HC.LS.set('hc_angle', angle); setAngle(); preview(); });
  var hc = HC.$('#hist-clear');
  if (hc) hc.addEventListener('click', function () { hist = []; HC.LS.set(HK, '[]'); renderHist(); });
  inp.addEventListener('input', function () { fresh = false; preview(); });
  inp.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); equals(); }
    else if (e.key === 'Escape') { inp.value = ''; preview(); }
  });
  HC.onLang(function () { setAngle(); preview(); renderHist(); });
  setAngle(); renderHist(); preview();
})();

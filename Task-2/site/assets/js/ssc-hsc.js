/* SSC/HSC GPA from marks, with 4th subject handling (see grading.js for the rules). */
(function () {
  'use strict';
  var wrap = HC.$('#sh-rows'); if (!wrap) return;
  var level = HC.$('#sh-level'), out = HC.$('#sh-res');
  var TPL = {
    ssc: [['Bangla', 'বাংলা'], ['English', 'ইংরেজি'], ['Mathematics', 'গণিত'], ['ICT', 'আইসিটি'], ['Religion', 'ধর্ম'], ['Physics', 'পদার্থবিজ্ঞান'], ['Chemistry', 'রসায়ন'], ['Biology', 'জীববিজ্ঞান'], ['Bangladesh & Global Studies', 'বাংলাদেশ ও বিশ্বপরিচয়'], ['Higher Mathematics', 'উচ্চতর গণিত', true]],
    hsc: [['Bangla', 'বাংলা'], ['English', 'ইংরেজি'], ['ICT', 'আইসিটি'], ['Physics', 'পদার্থবিজ্ঞান'], ['Chemistry', 'রসায়ন'], ['Biology', 'জীববিজ্ঞান'], ['Higher Mathematics', 'উচ্চতর গণিত', true]]
  };
  var rows = [];
  function tpl() { rows = TPL[level.value].map(function (t) { return { n: null, t: t, m: '', fourth: !!t[2] }; }); }
  function info(r) {
    var m = HC.parse(r.m);
    if (isNaN(m) || m < 0 || m > 100) return null;
    return BD.fromMarks(Math.floor(m + 1e-9));
  }
  function build() {
    wrap.textContent = '';
    rows.forEach(function (r, i) {
      var row = HC.mk('div', 'row'), name = HC.mk('input'), mk = HC.mk('input'), pre = HC.mk('span', 'rowinfo'), cbl = HC.mk('label', 'chk'), cb = HC.mk('input'), del = HC.mk('button', 'btn ghost del', '✕');
      name.type = 'text'; name.value = r.n === null ? HC.L(r.t[0], r.t[1]) : r.n; name.setAttribute('aria-label', HC.L('Subject name', 'বিষয়ের নাম'));
      name.addEventListener('input', function () { r.n = name.value; });
      mk.type = 'text'; mk.inputMode = 'decimal'; mk.value = r.m; mk.placeholder = HC.L('Marks', 'নম্বর'); mk.style.minWidth = '0'; mk.setAttribute('aria-label', HC.L('Marks out of 100', '১০০ এর মধ্যে নম্বর'));
      function upd() { var g = info(r); pre.textContent = g ? g.l + ' · ' + HC.fmt(g.gp, 2, 2) : '—'; }
      mk.addEventListener('input', function () { r.m = mk.value; upd(); run(); }); upd();
      cb.type = 'checkbox'; cb.checked = r.fourth;
      cb.addEventListener('change', function () { rows.forEach(function (x) { x.fourth = false; }); r.fourth = cb.checked; build(); run(); });
      cbl.append(cb, HC.mk('span', '', HC.L('4th subject', '৪র্থ বিষয়')));
      del.type = 'button'; del.setAttribute('aria-label', HC.L('Remove subject', 'বিষয় মুছুন'));
      del.addEventListener('click', function () { rows.splice(i, 1); build(); run(); });
      var mid = HC.mk('div'); mid.style.cssText = 'display:flex;align-items:center;gap:.5rem;min-width:0'; mid.append(mk, pre);
      row.style.setProperty('--n', 2); row.append(name, mid, cbl, del); wrap.append(row);
    });
  }
  function run() {
    var list = [], total = 0, ok = true;
    rows.forEach(function (r) { var g = info(r); if (!g) ok = false; else { list.push({ gp: g.gp, fourth: r.fourth }); total += HC.parse(r.m); } });
    if (!rows.length || !ok) return HC.render(out, { note: HC.L('Enter marks (0–100) for every subject to see the result.', 'ফলাফল দেখতে প্রতিটি বিষয়ে নম্বর (০–১০০) দিন।') });
    var res = BD.boardGPA(list);
    if (!res) return HC.error(out, HC.L('Add at least one compulsory subject.', 'অন্তত একটি আবশ্যিক বিষয় যোগ করুন।'));
    var fl = list.filter(function (x) { return x.fourth; })[0];
    HC.render(out, { label: HC.L('Your GPA', 'আপনার জিপিএ'), value: res.failed ? HC.L('Failed', 'অকৃতকার্য') + ' (0.00)' : HC.fmt(res.gpa, 2, 2) + ' (' + BD.boardLetter(res.gpa) + ')', rows: [
      [HC.L('Total marks', 'মোট নম্বর'), HC.fmt(total, 0)],
      [HC.L('Compulsory subject points', 'আবশ্যিক বিষয়ের পয়েন্ট'), HC.fmt(res.base, 2, 2) + ' / ' + HC.fmt(res.count * 5, 0)],
      [HC.L('4th subject', '৪র্থ বিষয়'), !fl ? HC.L('None selected', 'বাছাই করা হয়নি') : fl.gp > 2 ? HC.L('Adds ', 'যোগ হয়েছে ') + HC.fmt(fl.gp - 2, 2, 2) : HC.L('No bonus (GP 2 or less)', 'বোনাস নেই (জিপি ২ বা কম)')]
    ], note: res.failed ? HC.L('Marks below 33 in a compulsory subject (grade F) means the result is fail.', 'আবশ্যিক বিষয়ে ৩৩ এর কম নম্বর (গ্রেড F) মানে অকৃতকার্য।') : '' });
  }
  HC.$('#sh-add').addEventListener('click', function () { rows.push({ n: null, t: [HC.L('Subject ', 'বিষয় ') + (rows.length + 1), 'বিষয় ' + (rows.length + 1)], m: '', fourth: false }); build(); run(); });
  level.addEventListener('change', function () { tpl(); build(); run(); });
  HC.onLang(function () { build(); run(); });
  tpl(); build(); run();
})();

/* GPA calculator: pick a grade per subject. Board (5.00) with 4th subject, or university (4.00) weighted by credits. */
(function () {
  'use strict';
  var wrap = HC.$('#gpa-rows'); if (!wrap) return;
  var scale = HC.$('#gpa-scale'), out = HC.$('#gpa-res');
  var NAMES = [['Bangla', 'বাংলা'], ['English', 'ইংরেজি'], ['Mathematics', 'গণিত'], ['Physics', 'পদার্থবিজ্ঞান'], ['Chemistry', 'রসায়ন'], ['Biology', 'জীববিজ্ঞান']];
  var rows = [];
  function tpl(mode) {
    rows = mode === 'board'
      ? NAMES.map(function (n) { return { n: null, t: n, g: '', cr: '', fourth: false }; })
      : [1, 2, 3, 4, 5].map(function (i) { return { n: null, t: ['Course ' + i, 'কোর্স ' + i], g: '', cr: '3', fourth: false }; });
  }
  function table() { return scale.value === 'board' ? BD.BOARD : BD.UNI; }

  function build() {
    var board = scale.value === 'board';
    HC.$('#gpa-note-board').hidden = !board; HC.$('#gpa-note-uni').hidden = board;
    wrap.textContent = '';
    rows.forEach(function (r, i) {
      var row = HC.mk('div', 'row'), name = HC.mk('input'), g = HC.mk('select'), del = HC.mk('button', 'btn ghost del', '✕');
      name.type = 'text'; name.value = r.n === null ? HC.L(r.t[0], r.t[1]) : r.n; name.setAttribute('aria-label', HC.L('Subject name', 'বিষয়ের নাম'));
      name.addEventListener('input', function () { r.n = name.value; });
      var o0 = HC.mk('option', '', HC.L('Grade', 'গ্রেড')); o0.value = ''; g.append(o0);
      table().forEach(function (t) { var o = HC.mk('option', '', t.l + ' (' + t.gp.toFixed(2) + ')'); o.value = t.l; g.append(o); });
      g.value = r.g; g.setAttribute('aria-label', HC.L('Grade', 'গ্রেড'));
      g.addEventListener('change', function () { r.g = g.value; run(); });
      var third;
      if (board) {
        third = HC.mk('label', 'chk'); var cb = HC.mk('input'); cb.type = 'checkbox'; cb.checked = r.fourth;
        cb.addEventListener('change', function () { rows.forEach(function (x) { x.fourth = false; }); r.fourth = cb.checked; build(); run(); });
        third.append(cb, HC.mk('span', '', HC.L('4th subject', '৪র্থ বিষয়')));
      } else {
        third = HC.mk('input'); third.type = 'text'; third.inputMode = 'decimal'; third.value = r.cr; third.placeholder = HC.L('Credits', 'ক্রেডিট'); third.setAttribute('aria-label', HC.L('Credits', 'ক্রেডিট'));
        third.addEventListener('input', function () { r.cr = third.value; run(); });
      }
      del.type = 'button'; del.setAttribute('aria-label', HC.L('Remove subject', 'বিষয় মুছুন'));
      del.addEventListener('click', function () { rows.splice(i, 1); build(); run(); });
      row.style.setProperty('--n', 2); row.append(name, g, third, del); wrap.append(row);
    });
  }
  function run() {
    var board = scale.value === 'board', done = rows.filter(function (r) { return r.g; });
    if (!rows.length || done.length < rows.length) return HC.render(out, { note: HC.L('Choose a grade for every subject to see the result.', 'ফলাফল দেখতে প্রতিটি বিষয়ের গ্রেড বাছাই করুন।') });
    var gp = function (r) { return table().filter(function (t) { return t.l === r.g; })[0].gp; };
    if (board) {
      var res = BD.boardGPA(rows.map(function (r) { return { gp: gp(r), fourth: r.fourth }; }));
      if (!res) return HC.error(out, HC.L('Add at least one compulsory subject.', 'অন্তত একটি আবশ্যিক বিষয় যোগ করুন।'));
      HC.render(out, { label: HC.L('Your GPA', 'আপনার জিপিএ'), value: HC.fmt(res.gpa, 2, 2) + ' (' + BD.boardLetter(res.gpa) + ')', rows: [
        [HC.L('Compulsory subjects', 'আবশ্যিক বিষয়'), HC.fmt(res.count, 0)],
        [HC.L('Points from compulsory subjects', 'আবশ্যিক বিষয়ের পয়েন্ট'), HC.fmt(res.base, 2, 2)],
        [HC.L('4th subject bonus', '৪র্থ বিষয়ের বোনাস'), res.hasFourth ? HC.fmt(res.bonus, 2, 2) : '—']
      ], note: res.failed ? HC.L('A grade F in a compulsory subject means the overall result is fail (GPA 0.00).', 'আবশ্যিক বিষয়ে F মানে সামগ্রিক ফলাফল অকৃতকার্য (জিপিএ ০.০০)।') : '' });
    } else {
      var tc = 0, tp = 0, bad = false;
      rows.forEach(function (r) { var c = HC.parse(r.cr); if (isNaN(c) || c <= 0) bad = true; else { tc += c; tp += c * gp(r); } });
      if (bad) return HC.error(out, HC.L('Enter credits greater than zero for every subject.', 'প্রতিটি বিষয়ের ক্রেডিট শূন্যের বেশি দিন।'));
      var g = tp / tc;
      HC.render(out, { label: HC.L('Your GPA', 'আপনার জিপিএ'), value: HC.fmt(g, 2, 2) + ' (' + BD.uniLetter(g) + ')', rows: [
        [HC.L('Total credits', 'মোট ক্রেডিট'), HC.fmt(tc, 2)], [HC.L('Total grade points', 'মোট গ্রেড পয়েন্ট'), HC.fmt(tp, 2)]] });
    }
  }
  HC.$('#gpa-add').addEventListener('click', function () {
    rows.push({ n: null, t: [HC.L('Subject ', 'বিষয় ') + (rows.length + 1), 'বিষয় ' + (rows.length + 1)], g: '', cr: '3', fourth: false }); build(); run();
  });
  scale.addEventListener('change', function () { tpl(scale.value); build(); run(); });
  HC.onLang(function () { build(); run(); });
  tpl('board'); build(); run();
})();

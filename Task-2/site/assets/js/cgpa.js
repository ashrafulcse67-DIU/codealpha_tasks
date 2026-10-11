/* CGPA = sum(GPA x credits) / sum(credits). Works by semester or by course. */
(function () {
  'use strict';
  var wrap = HC.$('#cg-rows'); if (!wrap) return;
  var out = HC.$('#cg-res'), tabs = HC.$$('#cg-tabs button'), mode = 'sem', rows = [];
  function tpl() {
    rows = [1, 2, 3, 4].map(function (i) { return { n: null, t: mode === 'sem' ? ['Semester ' + i, 'সেমিস্টার ' + i] : ['Course ' + i, 'কোর্স ' + i], v: '', cr: mode === 'sem' ? '' : '3' }; });
  }
  function build() {
    HC.$('#cg-h1').textContent = mode === 'sem' ? HC.L('Semester GPA', 'সেমিস্টার জিপিএ') : HC.L('Grade', 'গ্রেড');
    wrap.textContent = '';
    rows.forEach(function (r, i) {
      var row = HC.mk('div', 'row'), name = HC.mk('input'), val, cr = HC.mk('input'), del = HC.mk('button', 'btn ghost del', '✕');
      name.type = 'text'; name.value = r.n === null ? HC.L(r.t[0], r.t[1]) : r.n; name.addEventListener('input', function () { r.n = name.value; });
      if (mode === 'sem') {
        val = HC.mk('input'); val.type = 'text'; val.inputMode = 'decimal'; val.placeholder = '0.00 – 4.00'; val.value = r.v;
        val.addEventListener('input', function () { r.v = val.value; run(); });
      } else {
        val = HC.mk('select'); var o0 = HC.mk('option', '', HC.L('Grade', 'গ্রেড')); o0.value = ''; val.append(o0);
        BD.UNI.forEach(function (t) { var o = HC.mk('option', '', t.l + ' (' + t.gp.toFixed(2) + ')'); o.value = t.gp; val.append(o); });
        val.value = r.v; val.addEventListener('change', function () { r.v = val.value; run(); });
      }
      val.setAttribute('aria-label', mode === 'sem' ? 'GPA' : HC.L('Grade', 'গ্রেড'));
      cr.type = 'text'; cr.inputMode = 'decimal'; cr.placeholder = HC.L('Credits', 'ক্রেডিট'); cr.value = r.cr; cr.setAttribute('aria-label', HC.L('Credits', 'ক্রেডিট'));
      cr.addEventListener('input', function () { r.cr = cr.value; run(); });
      name.setAttribute('aria-label', HC.L('Name', 'নাম'));
      del.type = 'button'; del.setAttribute('aria-label', HC.L('Remove row', 'সারি মুছুন'));
      del.addEventListener('click', function () { rows.splice(i, 1); build(); run(); });
      row.append(name, val, cr, del); wrap.append(row);
    });
  }
  function run() {
    var tc = 0, tp = 0, used = 0;
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i]; if (r.v === '' && r.cr === '') continue;
      var g = HC.parse(r.v), c = HC.parse(r.cr);
      if (isNaN(g) || isNaN(c) || c <= 0 || g < 0 || g > 4) return HC.error(out, HC.L('Each row needs a GPA between 0 and 4.00 and credits above zero.', 'প্রতিটি সারিতে ০ থেকে ৪.০০ এর মধ্যে জিপিএ এবং শূন্যের বেশি ক্রেডিট দিন।'));
      tc += c; tp += g * c; used++;
    }
    if (!used) return HC.render(out, null);
    var cg = tp / tc;
    HC.render(out, { label: 'CGPA', value: HC.fmt(cg, 2, 2) + ' (' + BD.uniLetter(cg) + ')', rows: [
      [HC.L('Total credits', 'মোট ক্রেডিট'), HC.fmt(tc, 2)], [HC.L('Total grade points', 'মোট গ্রেড পয়েন্ট'), HC.fmt(tp, 2)], [HC.L('Rows counted', 'গণনা করা সারি'), HC.fmt(used, 0)]
    ], note: HC.L('Uses the common 4.00 scale. Your university may set grade cut-offs differently.', 'প্রচলিত ৪.০০ স্কেল ব্যবহার করা হয়েছে; আপনার বিশ্ববিদ্যালয়ের গ্রেড সীমা আলাদা হতে পারে।') });
  }
  tabs.forEach(function (b) {
    b.addEventListener('click', function () {
      mode = b.dataset.mode; tabs.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      tpl(); build(); run();
    });
  });
  HC.$('#cg-add').addEventListener('click', function () {
    rows.push({ n: null, t: [(mode === 'sem' ? 'Semester ' : 'Course ') + (rows.length + 1), (mode === 'sem' ? 'সেমিস্টার ' : 'কোর্স ') + (rows.length + 1)], v: '', cr: mode === 'sem' ? '' : '3' }); build();
  });
  HC.onLang(function () { build(); run(); });
  tpl(); build(); run();
})();

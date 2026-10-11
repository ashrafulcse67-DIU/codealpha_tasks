(function () {
  'use strict';
  var cards = HC.$$('[data-pct]'); if (!cards.length) return;
  var T = {
    of: function (a, b) { return { label: HC.L('Result', 'ফলাফল'), value: HC.fmt(a * b / 100, 6) }; },
    what: function (a, b) {
      if (b === 0) return { err: HC.L('The second number cannot be zero.', 'দ্বিতীয় সংখ্যা শূন্য হতে পারবে না।') };
      return { label: HC.L('Percentage', 'শতকরা'), value: HC.fmt(a / b * 100, 6) + '%' };
    },
    chg: function (a, b) {
      if (a === 0) return { err: HC.L('The starting value cannot be zero.', 'শুরুর মান শূন্য হতে পারবে না।') };
      var p = (b - a) / Math.abs(a) * 100;
      return { label: p >= 0 ? HC.L('Increase', 'বৃদ্ধি') : HC.L('Decrease', 'হ্রাস'), value: HC.fmt(Math.abs(p), 6) + '%',
        rows: [[HC.L('Difference', 'পার্থক্য'), HC.fmt(b - a, 6)]] };
    },
    add: function (a, b, op) {
      var diff = b * a / 100, r = op === 'minus' ? b - diff : b + diff;
      return { label: HC.L('New value', 'নতুন মান'), value: HC.fmt(r, 6), rows: [[op === 'minus' ? HC.L('Amount removed', 'বাদ গেছে') : HC.L('Amount added', 'যোগ হয়েছে'), HC.fmt(diff, 6)]] };
    }
  };
  function run(card) {
    var a = HC.parse(HC.$('[data-k=a]', card).value), b = HC.parse(HC.$('[data-k=b]', card).value),
      opEl = HC.$('[data-k=op]', card), out = HC.$('.result', card);
    if (isNaN(a) || isNaN(b)) return HC.render(out, null);
    var r = T[card.dataset.pct](a, b, opEl && opEl.value);
    if (r.err) HC.error(out, r.err); else HC.render(out, r);
  }
  cards.forEach(function (c) { c.addEventListener('input', function () { run(c); }); c.addEventListener('change', function () { run(c); }); });
  HC.onLang(function () { cards.forEach(run); });
})();

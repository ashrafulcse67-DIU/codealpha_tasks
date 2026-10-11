(function () {
  'use strict';
  var s = HC.$('#dd-start'); if (!s) return;
  var e = HC.$('#dd-end'), inc = HC.$('#dd-inc'), out = HC.$('#dd-res');
  e.value = HC.isoDate(HC.today());
  function run() {
    var a = HC.parseDate(s.value), b = HC.parseDate(e.value);
    if (!a || !b) return HC.render(out, null);
    var swapped = HC.utc(a) > HC.utc(b);
    if (swapped) { var t = a; a = b; b = t; }
    var days = HC.dayDiff(a, b), end = b;
    if (inc.checked) { var n = new Date(HC.utc(b) + 864e5); end = { y: n.getUTCFullYear(), m: n.getUTCMonth(), d: n.getUTCDate() }; days++; }
    var r = HC.ymd(a, end), wk = 0, cur = HC.utc(a), last = HC.utc(end);
    for (; cur < last; cur += 864e5) { var g = new Date(cur).getUTCDay(); if (g !== 0 && g !== 6) wk++; }
    HC.render(out, { label: HC.L('Difference', 'ব্যবধান'),
      value: HC.fmt(r.y, 0) + HC.L(' years ', ' বছর ') + HC.fmt(r.m, 0) + HC.L(' months ', ' মাস ') + HC.fmt(r.d, 0) + HC.L(' days', ' দিন'),
      rows: [
        [HC.L('Total days', 'মোট দিন'), HC.fmt(days, 0)],
        [HC.L('Weeks and days', 'সপ্তাহ ও দিন'), HC.fmt(Math.floor(days / 7), 0) + HC.L(' weeks ', ' সপ্তাহ ') + HC.fmt(days % 7, 0) + HC.L(' days', ' দিন')],
        [HC.L('Weekdays (Mon–Fri)', 'কর্মদিবস (সোম–শুক্র)'), HC.fmt(wk, 0)],
        [HC.L('Total hours', 'মোট ঘণ্টা'), HC.fmt(days * 24, 0)]
      ], note: swapped ? HC.L('The start date was after the end date, so they were swapped.', 'শুরুর তারিখ শেষের তারিখের পরে ছিল, তাই দুটি বদলে নেওয়া হয়েছে।') : '' });
  }
  [s, e, inc].forEach(function (x) { x.addEventListener('input', run); x.addEventListener('change', run); });
  HC.onLang(run);
})();

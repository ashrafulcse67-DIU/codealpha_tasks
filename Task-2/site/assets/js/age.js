(function () {
  'use strict';
  var dob = HC.$('#a-dob'); if (!dob) return;
  var on = HC.$('#a-on'), out = HC.$('#age-res');
  on.value = HC.isoDate(HC.today());
  function run() {
    var a = HC.parseDate(dob.value), b = HC.parseDate(on.value);
    if (!a || !b) return HC.render(out, null);
    if (HC.utc(a) > HC.utc(b)) return HC.error(out, HC.L('The date of birth must be before the "age on" date.', 'জন্মতারিখ অবশ্যই "যে তারিখে বয়স" এর আগে হতে হবে।'));
    var r = HC.ymd(a, b), days = HC.dayDiff(a, b);
    var next = { y: b.y, m: a.m, d: a.d }; if (HC.utc(next) < HC.utc(b)) next.y++;
    var nd = new Date(HC.utc(next)), nx = { y: nd.getUTCFullYear(), m: nd.getUTCMonth(), d: nd.getUTCDate() }, left = HC.dayDiff(b, nx);
    HC.render(out, { label: HC.L('Your age', 'আপনার বয়স'),
      value: HC.fmt(r.y, 0) + HC.L(' years ', ' বছর ') + HC.fmt(r.m, 0) + HC.L(' months ', ' মাস ') + HC.fmt(r.d, 0) + HC.L(' days', ' দিন'),
      rows: [
        [HC.L('Total months', 'মোট মাস'), HC.fmt(r.y * 12 + r.m, 0)],
        [HC.L('Total weeks', 'মোট সপ্তাহ'), HC.fmt(Math.floor(days / 7), 0)],
        [HC.L('Total days', 'মোট দিন'), HC.fmt(days, 0)],
        [HC.L('Total hours', 'মোট ঘণ্টা'), HC.fmt(days * 24, 0)],
        [HC.L('Born on', 'জন্মবার'), HC.fmtDate(a, true)],
        [HC.L('Next birthday', 'পরবর্তী জন্মদিন'), left === 0 ? HC.L('Today!', 'আজই!') : HC.fmtDate(nx, true) + ' (' + HC.L('in ', '') + HC.fmt(left, 0) + HC.L(' days)', ' দিন পর)')]
      ] });
  }
  dob.addEventListener('input', run); on.addEventListener('input', run); HC.onLang(run);
})();

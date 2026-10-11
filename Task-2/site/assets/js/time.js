(function () {
  'use strict';
  var c1 = HC.$('#t-dur'); if (!c1) return;
  function v(id) { var x = HC.$('#' + id).value; return x.trim() === '' ? 0 : HC.parse(x); }
  function two(n) { return HC.bnd(String(n).padStart(2, '0')); }
  function dhms(sec) {
    var neg = sec < 0; sec = Math.abs(Math.round(sec));
    var d = Math.floor(sec / 86400), h = Math.floor(sec % 86400 / 3600), m = Math.floor(sec % 3600 / 60), s = sec % 60;
    return (neg ? '−' : '') + [d ? HC.fmt(d, 0) + HC.L(' d', ' দিন') : '', h ? HC.fmt(h, 0) + HC.L(' h', ' ঘণ্টা') : '', m ? HC.fmt(m, 0) + HC.L(' min', ' মিনিট') : '', HC.fmt(s, 0) + HC.L(' s', ' সেকেন্ড')].filter(Boolean).join(' ');
  }
  function secs(p) { return v(p + 'd') * 86400 + v(p + 'h') * 3600 + v(p + 'm') * 60 + v(p + 's'); }
  function dur() {
    var out = HC.$('#t-dur-res'), a = secs('a'), b = secs('b');
    if (isNaN(a) || isNaN(b)) return HC.error(out, HC.L('Enter numbers only.', 'শুধু সংখ্যা দিন।'));
    var r = HC.$('#t-op').value === 'sub' ? a - b : a + b;
    HC.render(out, { label: HC.L('Result', 'ফলাফল'), value: dhms(r), rows: [
      [HC.L('Total hours', 'মোট ঘণ্টা'), HC.fmt(r / 3600, 4)], [HC.L('Total minutes', 'মোট মিনিট'), HC.fmt(r / 60, 2)], [HC.L('Total seconds', 'মোট সেকেন্ড'), HC.fmt(r, 0)]] });
  }
  function between() {
    var out = HC.$('#t-bt-res'), a = HC.$('#t-from').value, b = HC.$('#t-to').value;
    if (!a || !b) return HC.render(out, null);
    var x = a.split(':'), y = b.split(':'), m1 = +x[0] * 60 + +x[1], m2 = +y[0] * 60 + +y[1], over = m2 < m1;
    var diff = (m2 - m1 + 1440) % 1440;
    HC.render(out, { label: HC.L('Time between', 'মধ্যবর্তী সময়'), value: HC.fmt(Math.floor(diff / 60), 0) + HC.L(' h ', ' ঘণ্টা ') + HC.fmt(diff % 60, 0) + HC.L(' min', ' মিনিট'),
      rows: [[HC.L('In minutes', 'মিনিটে'), HC.fmt(diff, 0)]], note: over ? HC.L('The end time is earlier, so it is counted as the next day.', 'শেষের সময় আগে, তাই পরের দিন ধরা হয়েছে।') : '' });
  }
  function shift() {
    var out = HC.$('#t-sh-res'), t = HC.$('#t-base').value;
    if (!t) return HC.render(out, null);
    var p = t.split(':'), d = v('t-sh-h') * 60 + v('t-sh-m');
    if (isNaN(d)) return HC.error(out, HC.L('Enter numbers only.', 'শুধু সংখ্যা দিন।'));
    var total = +p[0] * 60 + +p[1] + (HC.$('#t-sh-op').value === 'sub' ? -d : d), day = Math.floor(total / 1440), m = ((total % 1440) + 1440) % 1440;
    var h24 = Math.floor(m / 60), mm = m % 60, h12 = h24 % 12 || 12, ap = h24 < 12 ? 'AM' : 'PM';
    HC.render(out, { label: HC.L('New time', 'নতুন সময়'), value: two(h12) + ':' + two(mm) + ' ' + ap,
      rows: [[HC.L('24-hour', '২৪ ঘণ্টা'), two(h24) + ':' + two(mm)], [HC.L('Day', 'দিন'), day === 0 ? HC.L('Same day', 'একই দিন') : (day > 0 ? '+' : '−') + HC.fmt(Math.abs(day), 0) + HC.L(' day', ' দিন')]] });
  }
  var map = [['#t-dur', dur], ['#t-between', between], ['#t-shift', shift]];
  map.forEach(function (m) { var el = HC.$(m[0]); el.addEventListener('input', m[1]); el.addEventListener('change', m[1]); });
  HC.onLang(function () { dur(); between(); shift(); });
  dur();
})();

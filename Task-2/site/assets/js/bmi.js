(function () {
  'use strict';
  var out = HC.$('#bmi-res'); if (!out || !window.Body) return;
  var std = HC.$('#bmi-std');
  var COL = ['#38BDF8', '#22C55E', '#F59E0B', '#EF4444'];
  function run() {
    var b = Body.read();
    if (!b) return HC.render(out, null);
    if (b.bad) return HC.error(out, Body.badMsg());
    var bmi = b.w / (b.h * b.h), asian = std.value === 'asian';
    var cut = asian ? [18.5, 23, 25] : [18.5, 25, 30];
    var names = asian
      ? [HC.L('Underweight', 'কম ওজন'), HC.L('Normal', 'স্বাভাবিক'), HC.L('Overweight', 'বেশি ওজন'), HC.L('Obese', 'স্থূল')]
      : [HC.L('Underweight', 'কম ওজন'), HC.L('Normal', 'স্বাভাবিক'), HC.L('Overweight', 'বেশি ওজন'), HC.L('Obese', 'স্থূল')];
    var i = bmi < cut[0] ? 0 : bmi < cut[1] ? 1 : bmi < cut[2] ? 2 : 3;
    var lo = 18.5 * b.h * b.h, hi = (cut[1] - 0.1) * b.h * b.h;
    HC.render(out, { label: HC.L('Your BMI', 'আপনার বিএমআই'), value: HC.fmt(bmi, 1) + ' – ' + names[i], rows: [
      [HC.L('Healthy weight for your height', 'আপনার উচ্চতায় সুস্থ ওজন'), HC.fmt(lo, 1) + '–' + HC.fmt(hi, 1) + ' kg'],
      [HC.L('Your weight', 'আপনার ওজন'), Body.kg(b.w)]
    ], note: HC.L('BMI is a rough screening number. It does not measure body fat, muscle or health on its own.', 'বিএমআই একটি আনুমানিক স্ক্রিনিং সংখ্যা; এটি একা শরীরের চর্বি, পেশি বা স্বাস্থ্য মাপে না।') });
    /* range bar: 15 to 40 */
    var parts = [cut[0] - 15, cut[1] - cut[0], cut[2] - cut[1], 40 - cut[2]], bar = HC.mk('div', 'bmi-bar');
    bar.setAttribute('aria-hidden', 'true');
    parts.forEach(function (w, k) { var s = HC.mk('i'); s.style.flex = w; s.style.background = COL[k]; bar.append(s); });
    var mark = HC.mk('span', 'bmi-mark'); mark.style.left = Math.max(0, Math.min(100, (bmi - 15) / 25 * 100)) + '%';
    bar.append(mark); out.insertBefore(bar, out.children[1]);
  }
  Body.onChange(function () { run(); }); std.addEventListener('change', run);
  HC.onLang(run);
})();

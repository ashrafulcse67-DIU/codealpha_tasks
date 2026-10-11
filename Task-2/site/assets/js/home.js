(function () {
  'use strict';
  var a = HC.$('#q-a'); if (!a) return;
  var b = HC.$('#q-b'), out = HC.$('#q-res');
  function run() {
    var x = HC.parse(a.value), y = HC.parse(b.value);
    if (isNaN(x) || isNaN(y)) return HC.render(out, null);
    HC.render(out, { label: HC.L('Answer', 'উত্তর'), value: HC.fmt(x * y / 100, 4) });
  }
  a.addEventListener('input', run); b.addEventListener('input', run); HC.onLang(run); run();
})();

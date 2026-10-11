/* Shared height/weight inputs for BMI and calorie pages. */
(function () {
  'use strict';
  var units = HC.$('#bu'); if (!units) return;
  function sync() {
    var m = units.value === 'metric';
    HC.$$('[data-u=metric]').forEach(function (e) { e.hidden = !m; });
    HC.$$('[data-u=imperial]').forEach(function (e) { e.hidden = m; });
  }
  window.Body = {
    /* returns {h: metres, w: kg} or null; sets .error text when something is out of range */
    read: function () {
      var m = units.value === 'metric', h, w;
      if (m) { h = HC.parse(HC.$('#hcm').value) / 100; w = HC.parse(HC.$('#wv').value); }
      else {
        var ft = HC.parse(HC.$('#hft').value), inch = HC.$('#hin').value.trim() === '' ? 0 : HC.parse(HC.$('#hin').value);
        h = (ft * 12 + inch) * 0.0254; w = HC.parse(HC.$('#wv').value) * 0.45359237;
      }
      if (isNaN(h) || isNaN(w)) return null;
      if (h < 0.5 || h > 2.8 || w < 2 || w > 500) return { bad: true };
      return { h: h, w: w };
    },
    badMsg: function () { return HC.L('Please enter a realistic height and weight.', 'বাস্তবসম্মত উচ্চতা ও ওজন দিন।'); },
    kg: function (w) { return HC.fmt(w, 1) + ' kg / ' + HC.fmt(w / 0.45359237, 1) + ' lb'; },
    onChange: function (fn) {
      HC.$$('input,select', HC.$('#bodyform')).forEach(function (e) { e.addEventListener('input', fn); e.addEventListener('change', fn); });
      units.addEventListener('change', function () { sync(); fn(); });
    }
  };
  sync();
})();

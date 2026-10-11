(function () {
  'use strict';
  var out = HC.$('#cal-res'); if (!out || !window.Body) return;
  function run() {
    var b = Body.read(), age = HC.parse(HC.$('#c-age').value);
    if (!b || isNaN(age)) return HC.render(out, null);
    if (b.bad || age < 15 || age > 100) return HC.error(out, age < 15 || age > 100 ? HC.L('This estimate is meant for ages 15 to 100.', 'এই হিসাব ১৫ থেকে ১০০ বছর বয়সের জন্য।') : Body.badMsg());
    var male = HC.$('#c-sex').value === 'male';
    /* Mifflin-St Jeor equation */
    var bmr = 10 * b.w + 6.25 * b.h * 100 - 5 * age + (male ? 5 : -161);
    var tdee = bmr * parseFloat(HC.$('#c-act').value), goal = HC.$('#c-goal').value, adj = goal === 'lose' ? -500 : goal === 'gain' ? 500 : 0;
    var target = tdee + adj, low = target < (male ? 1500 : 1200);
    HC.render(out, { label: HC.L('Daily target', 'দৈনিক লক্ষ্য'), value: HC.fmt(target, 0) + ' kcal', rows: [
      [HC.L('Basal metabolic rate (BMR)', 'বেসাল মেটাবলিক রেট (বিএমআর)'), HC.fmt(bmr, 0) + ' kcal'],
      [HC.L('Maintenance calories', 'ওজন ধরে রাখার ক্যালোরি'), HC.fmt(tdee, 0) + ' kcal']
    ], note: (low ? HC.L('This target is low. Check with a doctor or dietitian before eating this little. ', 'এই লক্ষ্য কম। এত কম খাওয়ার আগে চিকিৎসক বা পুষ্টিবিদের পরামর্শ নিন। ') : '') +
      HC.L('An estimate only; real needs vary from person to person.', 'এটি শুধু আনুমানিক; প্রকৃত প্রয়োজন মানুষভেদে আলাদা।') });
  }
  Body.onChange(run);
  ['#c-act', '#c-goal'].forEach(function (id) { HC.$(id).addEventListener('change', run); });
  HC.onLang(run);
})();

(function () {
  'use strict';
  var f = HC.$('#disc'); if (!f) return;
  var out = HC.$('#disc-res'), out2 = HC.$('#rev-res');
  function p(id) { var v = HC.$('#' + id).value; return v.trim() === '' ? 0 : HC.parse(v); }
  function run() {
    var price = HC.parse(HC.$('#d-price').value), d1 = p('d-pct'), d2 = p('d-extra'), tax = p('d-tax');
    if (isNaN(price) || isNaN(d1) || isNaN(d2) || isNaN(tax)) return HC.render(out, null);
    if (d1 > 100 || d2 > 100 || price < 0) return HC.error(out, HC.L('Check the values: a discount cannot be above 100%.', 'মান যাচাই করুন: ছাড় ১০০% এর বেশি হতে পারে না।'));
    var after = price * (1 - d1 / 100) * (1 - d2 / 100), taxAmt = after * tax / 100;
    HC.render(out, { label: HC.L('You pay', 'আপনি দেবেন'), value: HC.taka(after + taxAmt), rows: [
      [HC.L('You save', 'সাশ্রয়'), HC.taka(price - after)],
      [HC.L('Price after discount', 'ছাড়ের পর দাম'), HC.taka(after)],
      [HC.L('Tax / VAT', 'ট্যাক্স / ভ্যাট'), HC.taka(taxAmt)],
      [HC.L('Effective discount', 'মোট ছাড়'), price ? HC.fmt((price - after) / price * 100, 2) + '%' : '—']
    ] });
  }
  function rev() {
    var o = HC.parse(HC.$('#r-orig').value), s = HC.parse(HC.$('#r-sale').value);
    if (isNaN(o) || isNaN(s)) return HC.render(out2, null);
    if (o <= 0) return HC.error(out2, HC.L('The original price must be above zero.', 'আসল দাম শূন্যের বেশি হতে হবে।'));
    var pc = (o - s) / o * 100;
    HC.render(out2, { label: pc >= 0 ? HC.L('Discount', 'ছাড়') : HC.L('Price increase', 'দাম বৃদ্ধি'), value: HC.fmt(Math.abs(pc), 2) + '%', rows: [[HC.L('Difference', 'পার্থক্য'), HC.taka(Math.abs(o - s))]] });
  }
  f.addEventListener('input', run); HC.$('#rev').addEventListener('input', rev);
  HC.onLang(function () { run(); rev(); });
})();

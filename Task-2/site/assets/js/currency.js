/* Currency converter. Built-in rates are approximate reference values; "Fetch latest" tries a free public API. */
(function () {
  'use strict';
  var amt = HC.$('#cur-amt'); if (!amt) return;
  var CUR = [
    ['BDT', 'Bangladeshi Taka', 'বাংলাদেশি টাকা', 122], ['USD', 'US Dollar', 'মার্কিন ডলার', 1], ['EUR', 'Euro', 'ইউরো', 0.92],
    ['GBP', 'British Pound', 'ব্রিটিশ পাউন্ড', 0.78], ['INR', 'Indian Rupee', 'ভারতীয় রুপি', 84], ['SAR', 'Saudi Riyal', 'সৌদি রিয়াল', 3.75],
    ['AED', 'UAE Dirham', 'সংযুক্ত আরব আমিরাত দিরহাম', 3.6725], ['MYR', 'Malaysian Ringgit', 'মালয়েশীয় রিংগিত', 4.4],
    ['SGD', 'Singapore Dollar', 'সিঙ্গাপুর ডলার', 1.34], ['JPY', 'Japanese Yen', 'জাপানি ইয়েন', 150], ['CNY', 'Chinese Yuan', 'চীনা ইউয়ান', 7.2],
    ['CAD', 'Canadian Dollar', 'কানাডিয়ান ডলার', 1.37], ['AUD', 'Australian Dollar', 'অস্ট্রেলিয়ান ডলার', 1.52]
  ];
  var KEY = 'hc_rates', from = HC.$('#cur-from'), to = HC.$('#cur-to'), res = HC.$('#cur-res'), stat = HC.$('#cur-status'), tbody = HC.$('#cur-rates');
  var state = { rates: {}, src: 'builtin', ts: 0 };
  CUR.forEach(function (c) { state.rates[c[0]] = c[3]; });
  try {
    var saved = JSON.parse(HC.LS.get(KEY, 'null'));
    if (saved && saved.rates) { CUR.forEach(function (c) { if (saved.rates[c[0]] > 0) state.rates[c[0]] = saved.rates[c[0]]; }); state.src = saved.src; state.ts = saved.ts; }
  } catch (e) {}
  function save() { HC.LS.set(KEY, JSON.stringify(state)); }
  function nm(c) { return HC.L(c[1], c[2]); }

  function status(extra) {
    var t = state.src === 'live' ? HC.L('Live rates from open.er-api.com, updated ', 'open.er-api.com থেকে সরাসরি রেট, হালনাগাদ: ') + new Date(state.ts).toLocaleString(HC.lang() === 'bn' ? 'bn-BD' : 'en-GB')
      : state.src === 'custom' ? HC.L('Using rates you entered yourself.', 'আপনার দেওয়া রেট ব্যবহার হচ্ছে।')
      : HC.L('Using built-in reference rates. They are approximate and not live; fetch the latest or edit them below.', 'অন্তর্নির্মিত আনুমানিক রেট ব্যবহার হচ্ছে, এগুলো সরাসরি নয়। সর্বশেষ রেট আনুন বা নিচে নিজে পরিবর্তন করুন।');
    stat.textContent = (extra ? extra + ' ' : '') + t;
  }
  function fill() {
    [from, to].forEach(function (sel, i) {
      var keep = sel.value || ['USD', 'BDT'][i];
      sel.textContent = '';
      CUR.forEach(function (c) { var o = HC.mk('option', '', c[0] + ' – ' + nm(c)); o.value = c[0]; sel.append(o); });
      sel.value = keep;
    });
  }
  function calc() {
    var x = HC.parse(amt.value);
    if (isNaN(x) || x < 0) return HC.render(res, null);
    var a = from.value, b = to.value, r = x / state.rates[a] * state.rates[b], one = state.rates[b] / state.rates[a];
    HC.render(res, { label: HC.fmt(x, 4) + ' ' + a + ' =', value: HC.fmt(r, 4, 2) + ' ' + b,
      note: '1 ' + a + ' = ' + HC.fmt(one, 6) + ' ' + b });
  }
  function rateTable() {
    tbody.textContent = '';
    CUR.forEach(function (c) {
      if (c[0] === 'USD') return;
      var tr = HC.mk('tr'), td = HC.mk('td'), inp = HC.mk('input');
      inp.type = 'text'; inp.inputMode = 'decimal'; inp.value = state.rates[c[0]]; inp.setAttribute('aria-label', c[0] + ' per 1 USD');
      inp.addEventListener('input', function () {
        var v = HC.parse(inp.value);
        if (v > 0) { state.rates[c[0]] = v; state.src = 'custom'; state.ts = Date.now(); save(); status(); calc(); }
      });
      td.append(inp);
      tr.append(HC.mk('td', '', c[0]), HC.mk('td', '', nm(c)), td); tbody.append(tr);
    });
  }
  HC.$('#cur-swap').addEventListener('click', function () { var t = from.value; from.value = to.value; to.value = t; calc(); });
  HC.$('#cur-reset').addEventListener('click', function () {
    CUR.forEach(function (c) { state.rates[c[0]] = c[3]; }); state.src = 'builtin'; state.ts = 0; save(); rateTable(); status(); calc();
  });
  HC.$('#cur-fetch').addEventListener('click', function () {
    var btn = this; btn.disabled = true; stat.textContent = HC.L('Fetching…', 'আনা হচ্ছে…');
    fetch('https://open.er-api.com/v6/latest/USD').then(function (r) { return r.json(); }).then(function (j) {
      if (j.result !== 'success') throw new Error('bad');
      CUR.forEach(function (c) { if (j.rates[c[0]] > 0) state.rates[c[0]] = j.rates[c[0]]; });
      state.src = 'live'; state.ts = (j.time_last_update_unix || Date.now() / 1000) * 1000; save(); rateTable(); status(); calc();
    }).catch(function () {
      status(HC.L('Could not fetch live rates (you may be offline).', 'সরাসরি রেট আনা যায়নি (অফলাইন হতে পারে)।'));
    }).then(function () { btn.disabled = false; });
  });
  [amt, from, to].forEach(function (el) { el.addEventListener('input', calc); el.addEventListener('change', calc); });
  HC.onLang(function () { fill(); rateTable(); status(); calc(); });
  fill(); rateTable(); status(); calc();
})();

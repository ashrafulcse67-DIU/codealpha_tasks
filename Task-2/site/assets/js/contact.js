/* No backend: the form builds a mailto: link and opens the visitor's email app. */
(function () {
  'use strict';
  var f = HC.$('#contact-form'); if (!f) return;
  var msg = HC.$('#cf-msg');
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!f.checkValidity()) { f.reportValidity(); return; }
    var kind = HC.$('input[name=kind]:checked', f), label = kind ? kind.dataset.label : 'General feedback';
    var name = HC.$('#cf-name').value.trim(), mail = HC.$('#cf-email').value.trim(), text = HC.$('#cf-text').value.trim();
    var body = text + '\n\n— ' + name + ' (' + mail + ')';
    window.location.href = 'mailto:' + f.dataset.to + '?subject=' + encodeURIComponent('[' + label + '] HisabCulator') + '&body=' + encodeURIComponent(body);
    msg.textContent = HC.L('Your email app should open with the message ready. Press send there. Nothing is sent from this page itself.', 'আপনার ইমেইল অ্যাপে বার্তাটি তৈরি অবস্থায় খুলবে। সেখান থেকে পাঠিয়ে দিন। এই পাতা থেকে কিছু সরাসরি পাঠানো হয় না।');
  });
})();

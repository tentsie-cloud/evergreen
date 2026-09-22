'use strict';
const toggle = document.querySelector('.menu-toggle');
const menu = document.querySelector('#mobile-menu');
if (toggle) toggle.hidden = false;
function closeMenu() { menu.hidden = true; toggle.setAttribute('aria-expanded', 'false'); }
toggle?.addEventListener('click', () => { const expanded = toggle.getAttribute('aria-expanded') === 'true'; menu.hidden = expanded; toggle.setAttribute('aria-expanded', String(!expanded)); });
menu?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && !menu.hidden) { closeMenu(); toggle.focus(); } });
document.querySelectorAll('[data-enquiry]').forEach(form => {
 form.hidden = false;
 form.addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(form);
  const method = data.get('method');
  const text = `Hi Evergreen, I would like to enquire about ${form.dataset.category}.\n\nDetails: ${String(data.get('details')).trim() || '[please add details]'}\nQuantity / area: ${String(data.get('quantity')).trim() || '[please add quantity]'}\nDelivery or collection: ${method}\nDelivery postcode: ${method === 'Collection' ? 'Collection from nursery' : String(data.get('postcode')).trim() || '[please add postcode]'}`;
  window.location.assign('https://wa.me/447808516747?text=' + encodeURIComponent(text));
 });
 const method = form.querySelector('[name="method"]');
 method.addEventListener('change', () => { const postcode = form.querySelector('[name="postcode"]'); postcode.disabled = method.value === 'Collection'; });
});

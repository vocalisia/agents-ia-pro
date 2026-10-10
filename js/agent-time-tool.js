/* Local-only scenario calculator. No network, storage or analytics calls. */
(function (root) {
  'use strict';
  const fields = {
    volume: { label: 'Tâches par mois', max: 10000000 },
    share: { label: 'Part déléguée', max: 100 },
    minutes: { label: 'Temps actuel par tâche', max: 100000 },
    review: { label: 'Vérification par tâche déléguée', max: 100000 },
    errors: { label: 'Tâches déléguées à reprendre', max: 100 },
    rework: { label: 'Temps supplémentaire par reprise', max: 100000 },
    maintenance: { label: 'Maintenance mensuelle', max: 100000 },
    setup: { label: 'Préparation initiale', max: 100000 }
  };
  function parse(value, key) {
    const definition = fields[key];
    const original = String(value ?? '').trim();
    // Accept French thousands separators only when grouping is well formed.
    const text = (/^\d{1,3}(?:[ \u00a0\u202f]\d{3})+(?:[,.]\d+)?$/.test(original)
      ? original.replace(/[ \u00a0\u202f]/g, '') : original).replace(',', '.');
    if (!/^\d+(?:\.\d+)?$/.test(text)) throw new Error('Saisissez un nombre positif ou zéro.');
    const number = Number(text);
    if (!Number.isFinite(number) || number > definition.max) throw new Error(`Maximum : ${definition.max.toLocaleString('fr-FR')}.`);
    if (key === 'volume' && !Number.isInteger(number)) throw new Error('Saisissez un nombre entier de tâches.');
    return number;
  }
  function calculate(raw) {
    const values = {};
    const errors = {};
    for (const key of Object.keys(fields)) {
      try { values[key] = parse(raw[key], key); } catch (error) { errors[key] = error.message; }
    }
    if (Object.keys(errors).length) return { valid: false, errors };
    const delegated = values.volume * values.share / 100;
    const baseline = values.volume * values.minutes / 60;
    const review = delegated * values.review / 60;
    const rework = delegated * values.errors / 100 * values.rework / 60;
    const avoided = delegated * values.minutes / 60;
    const net = avoided - review - rework - values.maintenance;
    const contributionMinutes = values.minutes - values.review - values.errors / 100 * values.rework;
    const minimumVolume = values.share > 0 && contributionMinutes > 0
      ? Math.floor(values.maintenance * 60 / (values.share / 100 * contributionMinutes)) + 1 : null;
    return { valid: true, values, delegated, baseline, avoided, review, rework, net,
      minimumVolume,
      remaining: baseline - net, firstMonth: net - values.setup,
      setupMonths: net > 0 ? values.setup / net : null };
  }
  function recommend(ready, task) {
    if (ready !== 'yes') return 'Préparez un pilote : décrivez un résultat acceptable, rassemblez des exemples et désignez la personne qui vérifiera les sorties.';
    const messages = {
      fixed: 'Commencez par un workflow à étapes fixes. Testez les règles et les cas d’exception avant d’ajouter un agent.',
      draft: 'Testez un assistant supervisé : il prépare un brouillon, une personne contrôle et valide avant toute utilisation.',
      adaptive: 'Évaluez un agent au périmètre limité : outils autorisés, arrêt explicite, journal des actions et validation humaine des actions sensibles.'
    };
    return messages[task] || 'Décrivez d’abord la tâche à déléguer.';
  }
  const api = { calculate, parse, recommend, fields };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (!root.document) return;
  const form = root.document.getElementById('agent-time-form');
  if (!form) return;
  const result = root.document.getElementById('agent-time-result');
  const summary = root.document.getElementById('agent-time-errors');
  const download = root.document.getElementById('agent-time-download');
  const fmt = value => new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 2 }).format(Object.is(value, -0) ? 0 : value);
  let current = null;
  function invalidate() {
    current = null; download.disabled = true; result.hidden = true;
  }
  form.addEventListener('input', invalidate);
  form.addEventListener('change', invalidate);
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const raw = Object.fromEntries(new FormData(form));
    const calculation = calculate(raw);
    for (const key of Object.keys(fields)) {
      const input = form.elements.namedItem(key);
      input.setAttribute('aria-invalid', calculation.errors?.[key] ? 'true' : 'false');
      root.document.getElementById(`time-error-${key}`).textContent = calculation.errors?.[key] || '';
    }
    if (!calculation.valid) {
      invalidate(); summary.textContent = 'Corrigez les champs indiqués pour calculer votre scénario.';
      form.elements.namedItem(Object.keys(calculation.errors)[0]).focus(); return;
    }
    summary.textContent = '';
    const orientation = recommend(raw.ready, raw.task);
    current = { ...calculation, orientation, task: raw.task, ready: raw.ready };
    const set = (id, value) => { root.document.getElementById(id).textContent = value; };
    set('time-net', `${fmt(calculation.net)} h / mois`);
    set('time-verdict', calculation.net > 0 ? 'Temps humain libéré dans ce scénario' : calculation.net < 0 ? 'Ce scénario ajoute du travail humain' : 'Aucun gain net dans ce scénario');
    set('time-baseline', `${fmt(calculation.baseline)} h`);
    set('time-remaining', `${fmt(calculation.remaining)} h`);
    set('time-review-total', `${fmt(calculation.review)} h`);
    set('time-rework-total', `${fmt(calculation.rework)} h`);
    set('time-avoided', `${fmt(calculation.avoided)} h`);
    set('time-maintenance-total', `${fmt(calculation.values.maintenance)} h`);
    set('time-threshold', calculation.minimumVolume === null
      ? 'Augmenter le volume ne suffit pas : réduisez le contrôle ou les reprises, ou revoyez la part déléguée.'
      : calculation.minimumVolume > fields.volume.max
      ? 'Le seuil de gain positif dépasse les 10 millions de tâches par mois pris en charge par ce simulateur.'
      : `Seuil de gain positif : ${fmt(calculation.minimumVolume)} tâches par mois, à part déléguée et durées constantes. Préparation initiale exclue.`);
    set('time-first', `${fmt(calculation.firstMonth)} h`);
    set('time-payback', calculation.values.setup === 0 ? 'Aucune préparation initiale déclarée.' : calculation.setupMonths === null ? 'Préparation non compensée : le gain mensuel doit être positif.' : `Préparation compensée en ${fmt(calculation.setupMonths)} mois, si le rythme reste identique.`);
    set('time-orientation', orientation);
    result.hidden = false; download.disabled = false; result.focus();
  });
  root.document.getElementById('agent-time-example').addEventListener('click', function () {
    const example = { volume: 400, share: 60, minutes: 10, review: 1, errors: 10, rework: 5, maintenance: 2, setup: 8 };
    for (const [key, value] of Object.entries(example)) form.elements.namedItem(key).value = value;
    form.elements.namedItem('ready').value = 'yes'; form.elements.namedItem('task').value = 'draft';
    form.requestSubmit();
  });
  form.addEventListener('reset', function () {
    invalidate(); summary.textContent = '';
    for (const key of Object.keys(fields)) {
      form.elements.namedItem(key).removeAttribute('aria-invalid');
      root.document.getElementById(`time-error-${key}`).textContent = '';
    }
  });
  download.addEventListener('click', function () {
    if (!current) return;
    const report = { source: 'agents-ia.pro/marketplace-agent-ia#simulateur-temps', version: 2,
      createdAt: new Date().toISOString(), status: 'SCENARIO_NON_MESURE',
      formula: 'N * (a/100) * (t - r - (e/100)*c) / 60 - m',
      units: { volume: 'tâches/mois', share: '%', minutes: 'min/tâche', review: 'min/tâche déléguée', errors: '% des tâches déléguées', rework: 'min/reprise supplémentaire', maintenance: 'h/mois', setup: 'h initiales' },
      assumptions: current.values, orientation: current.orientation, pilot: {ready:current.ready, task:current.task},
      results: { netHoursPerMonth: current.net, remainingHoursPerMonth: current.remaining, baselineHoursPerMonth: current.baseline, firstMonthNetHours: current.firstMonth, setupMonths: current.setupMonths,
        avoidedHours:current.avoided, reviewHours:current.review, reworkHours:current.rework, maintenanceHours:current.values.maintenance, minimumMonthlyVolumeForPositiveGain:current.minimumVolume },
      limitations: 'Hypothèses saisies, sans garantie de performance ni évaluation financière. Frais logiciels et temps machine exclus.' };
    const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' }));
    const link = root.document.createElement('a'); link.href = url; link.download = 'scenario-temps-agent-ia.json';
    root.document.body.appendChild(link); link.click(); link.remove();
    root.setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
})(typeof window === 'undefined' ? globalThis : window);

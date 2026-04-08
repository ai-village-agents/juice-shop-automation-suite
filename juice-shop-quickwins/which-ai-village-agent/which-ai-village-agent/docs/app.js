const $ = (id) => document.getElementById(id);

function clamp(x, lo, hi){ return Math.max(lo, Math.min(hi, x)); }

function encode(obj){
  const json = JSON.stringify(obj);
  return btoa(unescape(encodeURIComponent(json))).replaceAll('=', '');
}
function decode(str){
  const pad = str + '==='.slice((str.length + 3) % 4);
  const json = decodeURIComponent(escape(atob(pad)));
  return JSON.parse(json);
}

function dot(a,b){
  let s = 0;
  for (const k of Object.keys(a)) s += (a[k]||0) * (b[k]||0);
  return s;
}
function norm(a){
  return Math.sqrt(dot(a,a)) || 1;
}
function cosine(a,b){
  return dot(a,b) / (norm(a) * norm(b));
}

function emptyVector(dimIds){
  return Object.fromEntries(dimIds.map(d => [d, 0]));
}

function likertToScore(v){
  // v in [1..5] -> [-1..+1]
  return (clamp(v,1,5) - 3) / 2;
}

function computeDimMaxAbs(questions, dimIds){
  // Maximum possible absolute contribution per dimension, given the question weights.
  // Since likertToScore() returns in [-1..+1] and forced_choice uses {-1,+1},
  // each question can contribute at most |w| to a dimension.
  const maxAbs = Object.fromEntries(dimIds.map(d => [d, 0]));
  for (const q of questions){
    for (const [dim, w] of Object.entries(q.weights)){
      if (maxAbs[dim] == null) maxAbs[dim] = 0;
      maxAbs[dim] += Math.abs(w);
    }
  }
  return maxAbs;
}

function computeVector(answers, questions, dimIds){
  const vec = emptyVector(dimIds);
  for (const q of questions){
    const a = answers[q.id];
    if (a == null) continue;

    if (q.type === 'likert'){
      const s = likertToScore(a);
      for (const [dim, w] of Object.entries(q.weights)) vec[dim] += s * w;
    } else if (q.type === 'forced_choice'){
      // a is 0 or 1.
      // By default Option1 is treated as the "positive" direction (+1).
      // Some questions invert this via option1IsPositive=false (meaning Option0 is +1).
      const option1IsPositive = (q.option1IsPositive !== false);
      const s = option1IsPositive ? ((a === 1) ? 1 : -1) : ((a === 0) ? 1 : -1);
      for (const [dim, w] of Object.entries(q.weights)) vec[dim] += s * w;
    }
  }

  // Normalize into per-dimension [-1..+1] for both display and matching.
  // (Avoids the prior global-max normalization, which distorted relative dimensions
  // and made cosine matching unstable.)
  const maxAbs = computeDimMaxAbs(questions, dimIds);
  for (const k of Object.keys(vec)){
    const denom = maxAbs[k] || 0;
    vec[k] = denom ? clamp(vec[k] / denom, -1, 1) : 0;
  }
  return vec;
}

function agentVectorToPm1(agentVec, dimIds){
  // Agent vectors are *ideally* stored in [0..1] per dimension.
  // Convert to [-1..+1] so they live in the same space as the quiz output.
  //
  // Compatibility: if an agent value is already outside [0..1], treat it as already
  // being in [-1..+1] and clamp. (This avoids accidental "double mapping".)
  const out = {};
  for (const d of dimIds){
    const v = agentVec[d];
    if (v == null) out[d] = 0;
    else if (v >= 0 && v <= 1) out[d] = (v - 0.5) * 2;
    else out[d] = clamp(v, -1, 1);
  }
  return out;
}

function bestMatch(vec, agents, dimIds){
  let best = null;
  for (const a of agents){
    const score = cosine(vec, agentVectorToPm1(a.vector, dimIds));
    if (!best || score > best.score) best = { agent: a, score };
  }
  return best;
}

function renderResult({agent, score, vec, dimensions}){
  const dimById = Object.fromEntries(dimensions.map(d => [d.id, d]));

  const badges = Object.keys(vec).map(id => {
    const d = dimById[id];
    const v = vec[id];
    const label = v >= 0 ? d.right : d.left;
    const pct = Math.round(Math.abs(v) * 100);
    return `<span class="badge">${d.label}: ${label} (${pct}%)</span>`;
  }).join('');

  const share = new URL(window.location.href);
  share.searchParams.set('r', agent.id);
  share.searchParams.set('v', encode(vec));

  $('result').innerHTML = `
    <h2>Your match: ${agent.name}</h2>
    <p class="sub">${agent.tagline}</p>
    <div>${badges}</div>
    <div class="hr"></div>

    <h3>Why this match</h3>
    <ul>${agent.why.map(x => `<li>${x}</li>`).join('')}</ul>

    <h3>Strengths</h3>
    <ul>${agent.strengths.map(x => `<li>${x}</li>`).join('')}</ul>

    <h3>Watch-outs</h3>
    <ul>${agent.watchouts.map(x => `<li>${x}</li>`).join('')}</ul>

    <div class="hr"></div>
    <h3>Share your result</h3>
    <p class="small">Copy this link:</p>
    <div class="code">${share.toString()}</div>

    <div class="nav" style="margin-top:14px">
      <button id="restartBtn" class="secondary">Restart</button>
      <a href="${share.toString()}" target="_blank" rel="noreferrer"><button>Open share link</button></a>
    </div>
    <p class="small">Note: this is a beta scoring model; agent portrayals will be updated after sign-off.</p>
  `;

  $('restartBtn').addEventListener('click', () => {
    window.location.search = '';
  });
}

async function main(){
  const cacheBust = (typeof window !== 'undefined' && window.__AV_CACHE_BUST)
    ? window.__AV_CACHE_BUST
    : Date.now().toString();

  const [dims, qs, agentsData] = await Promise.all([
    fetch(`data/dimensions.json?v=${cacheBust}`, { cache: 'no-store' }).then(r=>r.json()),
    fetch(`data/questions.json?v=${cacheBust}`, { cache: 'no-store' }).then(r=>r.json()),
    fetch(`data/agents.json?v=${cacheBust}`, { cache: 'no-store' }).then(r=>r.json())
  ]);

  const dimensions = dims.dimensions;
  const questions = qs.questions;
  const dimIds = qs.dimensions;
  const agents = agentsData.agents;

  $('loading').classList.add('hidden');

  // Share link mode
  const params = new URLSearchParams(window.location.search);
  const r = params.get('r');
  const v = params.get('v');
  if (r && v){
    const agent = agents.find(a => a.id === r);
    if (agent){
      const vec = decode(v);
      $('result').classList.remove('hidden');
      renderResult({agent, score: 1, vec, dimensions});
      return;
    }
  }

  $('start').classList.remove('hidden');

  let idx = 0;
  const answers = {};
  let currentSelection = null;

  function setSelection(sel){
    currentSelection = sel;
    for (const el of document.querySelectorAll('.option')){
      el.classList.toggle('selected', el.dataset.value == String(sel));
    }
    $('nextBtn').disabled = (sel == null);
  }

  function renderQuestion(){
    const q = questions[idx];
    $('quiz').classList.remove('hidden');
    $('start').classList.add('hidden');
    $('result').classList.add('hidden');

    $('progress').textContent = `Question ${idx+1} / ${questions.length}`;
    $('prompt').textContent = q.prompt;

    $('backBtn').disabled = idx === 0;
    $('nextBtn').textContent = (idx === questions.length-1) ? 'Finish' : 'Next';

    const optionsEl = $('options');
    optionsEl.innerHTML = '';

    if (q.type === 'likert'){
      const labels = [
        'Strongly disagree',
        'Disagree',
        'Neutral',
        'Agree',
        'Strongly agree'
      ];
      labels.forEach((lab, i) => {
        const v = i+1;
        const div = document.createElement('div');
        div.className = 'option';
        div.dataset.value = String(v);
        div.textContent = lab;
        div.addEventListener('click', () => setSelection(v));
        optionsEl.appendChild(div);
      });
    } else {
      q.options.forEach((lab, i) => {
        const div = document.createElement('div');
        div.className = 'option';
        div.dataset.value = String(i);
        div.textContent = lab;
        div.addEventListener('click', () => setSelection(i));
        optionsEl.appendChild(div);
      });
    }

    const prev = answers[q.id];
    setSelection(prev ?? null);
  }

  function finish(){
    const vec = computeVector(answers, questions, dimIds);
    const match = bestMatch(vec, agents, dimIds);

    $('quiz').classList.add('hidden');
    $('result').classList.remove('hidden');
    renderResult({agent: match.agent, score: match.score, vec, dimensions});
  }

  $('startBtn').addEventListener('click', () => renderQuestion());

  $('backBtn').addEventListener('click', () => {
    const q = questions[idx];
    if (currentSelection != null) answers[q.id] = currentSelection;
    idx = Math.max(0, idx-1);
    renderQuestion();
  });

  $('nextBtn').addEventListener('click', () => {
    const q = questions[idx];
    if (currentSelection == null) return;
    answers[q.id] = currentSelection;

    if (idx === questions.length-1) return finish();
    idx += 1;
    renderQuestion();
  });
}

main().catch(err => {
  console.error(err);
  $('loading').classList.remove('hidden');
  $('loading').innerHTML = `<p style="color: var(--danger)">Failed to load quiz data. Open console for details.</p>`;
});

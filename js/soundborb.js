/* Soundborb v0.7. Static audio soundboard; no trackers or external services. */
(() => {
  'use strict';
  const root = document.getElementById('soundborb');
  if (!root) return;
  const $ = (id) => document.getElementById(id);
  const audio = new Audio();
  audio.preload = 'none';
  audio.volume = 0.8;
  const state = { clips: [], byId: new Map(), favourites: new Set(), filter: 'all', query: '', queue: [], playing: null, machine: false, machineIndex: -1, requestedToken: 0, party: false, partyDeck: [], partyRound: 0, partyLast: null, partyFailures: 0 };
  const storageKey = 'channelchirp-soundborb-favourites-v1';
  try { const saved = JSON.parse(localStorage.getItem(storageKey) || '[]'); if (Array.isArray(saved)) state.favourites = new Set(saved.filter((s) => typeof s === 'string')); } catch (_) { /* Private browsing may block local storage. */ }
  const status = (message) => { $('sb-status').textContent = message; };
  const fullUrl = (relative) => new URL(relative, root.dataset.audioRoot.endsWith('/') ? new URL(root.dataset.audioRoot, location.href) : new URL(root.dataset.audioRoot + '/', location.href)).href;
  const humanCount = (n) => n + (n === 1 ? ' sound' : ' sounds');
  function saveFavourites() { try { localStorage.setItem(storageKey, JSON.stringify([...state.favourites])); } catch (_) {} }
  function shuffle(array) { const copy = [...array]; for (let i = copy.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [copy[i], copy[j]] = [copy[j], copy[i]]; } return copy; }
  function icon(isPlaying) { return isPlaying ? '<i class="fas fa-pause" aria-hidden="true"></i>' : '<i class="fas fa-play" aria-hidden="true"></i>'; }
  function makeClipCard(clip, index) {
    const card = document.createElement('article'); card.className = 'sb-card'; card.dataset.clipId = clip.id;
    const top = document.createElement('div'); top.className = 'sb-card-top';
    const number = document.createElement('span'); number.className = 'sb-card-number'; number.textContent = 'NO. ' + String(index + 1).padStart(2, '0');
    const fav = document.createElement('button'); fav.className = 'sb-card-fav'; fav.type = 'button'; fav.dataset.action = 'favourite'; fav.dataset.id = clip.id; fav.title = 'Toggle favourite'; fav.setAttribute('aria-label', 'Favourite ' + clip.title); fav.setAttribute('aria-pressed', String(state.favourites.has(clip.id))); fav.innerHTML = state.favourites.has(clip.id) ? '<i class="fas fa-heart" aria-hidden="true"></i>' : '<i class="far fa-heart" aria-hidden="true"></i>';
    top.append(number, fav);
    const title = document.createElement('h3'); title.className = 'sb-card-title'; title.textContent = clip.title;
    const info = document.createElement('div'); info.className = 'sb-card-sub'; info.textContent = clip.collection + ' · ' + clip.duration.toFixed(1) + 's';
    const waveform = document.createElement('div'); waveform.className = 'sb-waveform'; waveform.setAttribute('aria-hidden', 'true');
    const peak = Math.max(0.01, ...(clip.waveform || []));
    (clip.waveform || [0.2,0.6,0.4,0.8,0.3]).forEach((w) => { const bar = document.createElement('span'); bar.style.height = Math.max(7, Math.round(100 * w / peak)) + '%'; waveform.append(bar); });
    const actions = document.createElement('div'); actions.className = 'sb-card-actions';
    const play = document.createElement('button'); play.type = 'button'; play.className = 'sb-play'; play.dataset.action = 'play'; play.dataset.id = clip.id; play.innerHTML = icon(false) + ' <span>Play</span>'; play.setAttribute('aria-label', 'Play ' + clip.title);
    const add = document.createElement('button'); add.type = 'button'; add.className = 'sb-queue-add'; add.dataset.action = 'add'; add.dataset.id = clip.id; add.title = 'Add ' + clip.title + ' to queue'; add.setAttribute('aria-label', 'Add ' + clip.title + ' to queue'); add.innerHTML = '<i class="fas fa-plus" aria-hidden="true"></i>';
    actions.append(play, add); card.append(top, title, info, waveform, actions); return card;
  }
  function renderCards() {
    const filtered = state.clips.filter((clip) => (state.filter !== 'favourites' || state.favourites.has(clip.id)) && (clip.title + ' ' + clip.collection + ' ' + clip.id).toLowerCase().includes(state.query));
    const container = $('sb-clips'); container.replaceChildren(...filtered.map((c) => makeClipCard(c, state.clips.indexOf(c))));
    $('sb-empty').hidden = filtered.length !== 0; $('sb-count').textContent = humanCount(filtered.length);
    $('sb-fav-count').textContent = String(state.favourites.size);
    updatePlayingUI();
  }
  function updatePlayingUI() {
    root.querySelectorAll('.sb-card').forEach((card) => {
      const active = state.playing === card.dataset.clipId && !audio.paused;
      card.classList.toggle('is-playing', active);
      const play = card.querySelector('.sb-play');
      play.innerHTML = icon(active) + '<span>' + (active ? 'Pause' : 'Play') + '</span>';
      play.setAttribute('aria-label', (active ? 'Pause ' : 'Play ') + state.byId.get(card.dataset.clipId).title);
    });
    $('sb-play-queue').innerHTML = (state.machine && !audio.paused ? '<i class="fas fa-pause" aria-hidden="true"></i> Pause queue' : '<i class="fas fa-play" aria-hidden="true"></i> Play queue');
    const partyButton = $('sb-party');
    partyButton.setAttribute('aria-pressed', String(state.party));
    partyButton.classList.toggle('is-active', state.party);
    partyButton.innerHTML = state.party
      ? '<i class="fas fa-stop" aria-hidden="true"></i> Stop Party Parrot'
      : '<i class="fas fa-dove" aria-hidden="true"></i> Party Parrot';
    $('sb-queue-ten').disabled = !state.clips.length;
    $('sb-queue').querySelectorAll('.sb-queue-item').forEach((li) => li.classList.toggle('is-current', state.machine && Number(li.dataset.index) === state.machineIndex));
  }
  let handledErrorToken = -1;
  function handlePlaybackError(token) {
    if (token !== state.requestedToken || handledErrorToken === token) return;
    handledErrorToken = token;
    if (state.party) {
      state.partyFailures++;
      if (state.partyFailures >= state.clips.length) stopPlayback('Party Parrot stopped because the sounds could not be loaded.');
      else playNextParty();
    } else {
      stopPlayback('Could not play this sound. Please try another.');
    }
  }
  async function playClip(id, asMachine = false, asParty = false) {
    const clip = state.byId.get(id); if (!clip) return;
    const token = ++state.requestedToken;
    audio.pause(); state.playing = id;
    if (!asMachine) { state.machine = false; state.machineIndex = -1; }
    if (!asParty) { state.party = false; state.partyDeck = []; state.partyRound = 0; }
    audio.src = fullUrl(clip.src); audio.load();
    $('sb-now-title').textContent = clip.title; $('sb-progress').style.width = '0%';
    try {
      await audio.play();
      if (token !== state.requestedToken) return;
      state.partyFailures = 0;
      status((state.party ? 'Party Parrot: ' : 'Playing ') + clip.title);
    } catch (_) { handlePlaybackError(token); return; }
    updatePlayingUI(); renderQueue();
  }
  function stopPlayback(message = 'Playback stopped') {
    state.requestedToken++; audio.pause(); audio.removeAttribute('src'); audio.load();
    state.playing = null; state.machine = false; state.machineIndex = -1;
    state.party = false; state.partyDeck = []; state.partyRound = 0; state.partyLast = null; state.partyFailures = 0;
    $('sb-now-title').textContent = 'Pick a chirp!'; $('sb-progress').style.width = '0%'; status(message); updatePlayingUI(); renderQueue();
  }
  function togglePlay(id) {
    // Manually selecting a chirp leaves Party Parrot mode, even if it is the currently playing sound.
    if (state.party) { void playClip(id); return; }
    if (state.playing === id) { if (!audio.paused) { audio.pause(); state.machine = false; status('Paused ' + state.byId.get(id).title); updatePlayingUI(); return; } audio.play().then(updatePlayingUI).catch(() => status('Audio could not resume.')); return; }
    void playClip(id);
  }
  function playNextParty() {
    if (!state.party || !state.clips.length) return;
    if (!state.partyDeck.length) {
      const nextDeck = shuffle(state.clips.map((clip) => clip.id));
      // No immediate repeat at the boundary between two shuffled passes.
      if (nextDeck.length > 1 && nextDeck[0] === state.partyLast) {
        const swapAt = 1 + Math.floor(Math.random() * (nextDeck.length - 1));
        [nextDeck[0], nextDeck[swapAt]] = [nextDeck[swapAt], nextDeck[0]];
      }
      state.partyDeck = nextDeck;
      state.partyRound++;
    }
    const id = state.partyDeck.shift();
    state.partyLast = id;
    void playClip(id, false, true);
  }
  function toggleParty() {
    if (state.party) { stopPlayback('Party Parrot stopped'); return; }
    if (!state.clips.length) { status('Sounds are still loading.'); return; }
    stopPlayback('Starting Party Parrot');
    state.party = true;
    playNextParty();
  }
  function fillQueueToTen() {
    if (!state.clips.length) return;
    const wanted = Math.max(0, 10 - state.queue.length);
    if (!wanted) { status('Your queue already has 10 or more sounds.'); return; }
    const existing = new Set(state.queue);
    const picks = shuffle(state.clips.filter((c) => !existing.has(c.id))).slice(0, wanted).map((c) => c.id);
    state.queue.push(...picks);
    renderQueue();
    status(picks.length + ' random sounds added to your queue');
  }
  function playQueueFrom(index) {
    if (index < 0 || index >= state.queue.length) { stopPlayback('Queue finished'); return; }
    state.machine = true; state.machineIndex = index; void playClip(state.queue[index], true);
  }
  function renderQueue() {
    const list = $('sb-queue'); list.replaceChildren();
    if (state.queue.length === 0) { const li = document.createElement('li'); li.className = 'sb-queue-placeholder'; li.innerHTML = "It's quiet in here…<br>Add chirps using the <strong>+</strong> buttons."; list.append(li); }
    state.queue.forEach((id, index) => {
      const clip = state.byId.get(id); if (!clip) return;
      const li = document.createElement('li'); li.className = 'sb-queue-item'; li.dataset.index = String(index); if (state.machine && index === state.machineIndex) li.classList.add('is-current');
      const number = document.createElement('span'); number.className = 'sb-queue-index'; number.textContent = String(index + 1).padStart(2, '0');
      const label = document.createElement('span'); label.className = 'sb-queue-text'; label.textContent = clip.title;
      const remove = document.createElement('button'); remove.className = 'sb-queue-remove'; remove.dataset.removeIndex = String(index); remove.title = 'Remove ' + clip.title; remove.setAttribute('aria-label', 'Remove ' + clip.title + ' from queue'); remove.type = 'button'; remove.innerHTML = '<i class="fas fa-times" aria-hidden="true"></i>';
      li.append(number,label,remove); list.append(li);
    });
    $('sb-queue-count').textContent = humanCount(state.queue.length);
    for (const id of ['sb-play-queue', 'sb-shuffle', 'sb-clear']) $(id).disabled = state.queue.length === 0;
    $('sb-queue-ten').disabled = state.clips.length === 0;
    updatePlayingUI();
  }
  $('sb-clips').addEventListener('click', (event) => {
    const button = event.target.closest('button[data-action]'); if (!button) return;
    const {action, id} = button.dataset;
    if (action === 'play') togglePlay(id);
    if (action === 'add') { state.queue.push(id); renderQueue(); status(state.byId.get(id).title + ' added to queue'); }
    if (action === 'favourite') { state.favourites.has(id) ? state.favourites.delete(id) : state.favourites.add(id); saveFavourites(); renderCards(); status('Favourites updated'); }
  });
  $('sb-queue').addEventListener('click', (event) => {
    const button = event.target.closest('button[data-remove-index]'); if (!button) return;
    const index = Number(button.dataset.removeIndex);
    state.queue.splice(index, 1);
    if (state.machine) { if (index < state.machineIndex) state.machineIndex--; else if (index === state.machineIndex) { stopPlayback('Current queue item removed'); return; } }
    renderQueue();
  });
  $('sb-random').addEventListener('click', () => { if (state.clips.length) { const id = state.clips[Math.floor(Math.random() * state.clips.length)].id; void playClip(id); } });
  $('sb-surprise').addEventListener('click', () => { if (!state.clips.length) return; state.queue = shuffle(state.clips).slice(0, 10).map((c) => c.id); renderQueue(); playQueueFrom(0); });
  $('sb-queue-ten').addEventListener('click', fillQueueToTen);
  $('sb-party').addEventListener('click', toggleParty);
  $('sb-stop').addEventListener('click', () => stopPlayback());
  $('sb-play-queue').addEventListener('click', () => {
    if (!state.queue.length) return;
    if (state.machine && !audio.paused) { audio.pause(); updatePlayingUI(); status('Queue paused'); return; }
    if (state.machine && audio.paused && state.playing) { audio.play().then(() => { updatePlayingUI(); status('Queue resumed'); }).catch(() => playQueueFrom(0)); return; }
    playQueueFrom(0);
  });
  $('sb-shuffle').addEventListener('click', () => { stopPlayback('Queue shuffled'); state.queue = shuffle(state.queue); renderQueue(); });
  $('sb-clear').addEventListener('click', () => { stopPlayback('Queue cleared'); state.queue = []; renderQueue(); });
  $('sb-volume').addEventListener('input', (event) => { audio.volume = Number(event.target.value) / 100; });
  $('sb-search').addEventListener('input', (event) => { state.query = event.target.value.trim().toLowerCase(); renderCards(); });
  root.querySelectorAll('[data-filter]').forEach((button) => button.addEventListener('click', () => { state.filter = button.dataset.filter; root.querySelectorAll('[data-filter]').forEach((b) => { const on = b === button; b.classList.toggle('is-active',on); b.setAttribute('aria-pressed',String(on)); }); renderCards(); }));
  audio.addEventListener('timeupdate', () => { $('sb-progress').style.width = (audio.duration && Number.isFinite(audio.duration) ? 100*audio.currentTime/audio.duration : 0) + '%'; });
  audio.addEventListener('play', updatePlayingUI); audio.addEventListener('pause', updatePlayingUI);
  audio.addEventListener('ended', () => {
    if (state.party) playNextParty();
    else if (state.machine && state.machineIndex + 1 < state.queue.length) playQueueFrom(state.machineIndex + 1);
    else stopPlayback(state.machine ? 'Queue finished' : 'Chirp finished');
  });
  audio.addEventListener('error', () => { if (audio.src) handlePlaybackError(state.requestedToken); });
  async function init() {
    try {
      const response = await fetch(root.dataset.manifest, { cache: 'no-cache' });
      if (!response.ok) throw Error('HTTP ' + response.status);
      const data = await response.json();
      if (!Array.isArray(data.clips) || !data.clips.length) throw Error('No chirps found');
      state.clips = data.clips.filter((c) => c.id && c.src && typeof c.title === 'string');
      state.byId = new Map(state.clips.map((c) => [c.id,c]));
      renderCards(); renderQueue(); status(humanCount(state.clips.length) + ' ready');
    } catch (error) { $('sb-clips').textContent = 'Sorry, the chirps could not load. Please refresh this page.'; $('sb-count').textContent = 'Unavailable'; status('Failed to load chirps: ' + error.message); }
  }
  void init();
})();
---
layout: default
title: Soundborb
permalink: /soundborb/
show_hero: false
hide_title: true
body_class: soundborb-page
exclude_search: true
---
<link rel="stylesheet" href="{{ '/css/soundborb.css' | relative_url }}">

<div id="soundborb" class="sb" data-manifest="{{ '/assets/soundborb/clips.json' | relative_url }}" data-audio-root="{{ '/assets/soundborb/' | relative_url }}">
  <header class="sb-hero">
    <div class="sb-hero-copy">
      <span class="sb-kicker"><span class="sb-kicker-dot" aria-hidden="true"></span> THE LITTLE FLOCK SOUND MACHINE <span class="sb-version">v0.6</span></span>
      <h1>Sound<span>borb.</span></h1>
      <p>Little beeps, big personalities. A pocket-sized collection of real chirps, chatter, mimicry and a few silly call-and-response noises from the Channel Chirp flock and one of the borb parents.</p>
      <div class="sb-hero-buttons">
        <button class="sb-btn sb-btn-primary" type="button" id="sb-random"><i class="fas fa-random" aria-hidden="true"></i> Random borb</button>
        <button class="sb-btn sb-btn-secondary" type="button" id="sb-surprise"><i class="fas fa-music" aria-hidden="true"></i> Surprise me (10)</button>
        <button class="sb-btn sb-btn-party" type="button" id="sb-party" aria-pressed="false"><i class="fas fa-dove" aria-hidden="true"></i> Party Parrot</button>
      </div>
      <p class="sb-hero-hint">Tap a sound to play it. Try 10 surprises, fill a queue with 10 random sounds, or let Party Parrot shuffle through the whole collection on repeat.</p>
    </div>
    <div class="sb-flock" aria-label="The Channel Chirp flock">
      <a href="{{ '/pudge/' | relative_url }}" class="sb-bird sb-bird-a" aria-label="Meet Pudge. Pudge is the bird at the back of the thumbnail.">
        <img src="{{ '/images/pudge.jpg' | relative_url }}" alt="Pudge the bird" loading="lazy">
        <strong class="sb-bird-name">Pudge</strong>
        <span class="sb-bird-arrow" aria-hidden="true">↖ at the back</span>
      </a>
      <a href="{{ '/tillie/' | relative_url }}" class="sb-bird sb-bird-b" aria-label="Meet Tillie"><img src="{{ '/images/tillie.jpg' | relative_url }}" alt="Tillie the bird" loading="lazy"><strong class="sb-bird-name">Tillie</strong></a>
      <a href="{{ '/chip/' | relative_url }}" class="sb-bird sb-bird-c" aria-label="Meet Chip"><img src="{{ '/images/chip.jpg' | relative_url }}" alt="Chip the bird" loading="lazy"><strong class="sb-bird-name">Chip</strong></a>
      <div class="sb-bird sb-bird-d sb-bird-human" aria-label="Placeholder for one of the borb parents who made some playful noises back at the birds.">
        <div class="sb-human-icon" aria-hidden="true"><i class="fas fa-comment-dots"></i></div>
        <strong class="sb-bird-name">Borb parent</strong>
        <small>Placeholder for the silly noises made back at the flock.</small>
      </div>
      <div class="sb-flock-spark sb-flock-spark-1" aria-hidden="true">✦</div><div class="sb-flock-spark sb-flock-spark-2" aria-hidden="true">✳</div>
    </div>
  </header>

  <section class="sb-player" aria-label="Sound playback controls">
    <div class="sb-player-icon" id="sb-player-icon"><i class="fas fa-volume-up" aria-hidden="true"></i></div>
    <div class="sb-now"><span class="sb-overline">NOW CHIRPING</span><strong id="sb-now-title">Pick a chirp!</strong><div class="sb-playing-progress"><span id="sb-progress"></span></div></div>
    <button type="button" class="sb-icon-button sb-stop" id="sb-stop" aria-label="Stop playing"><i class="fas fa-stop" aria-hidden="true"></i></button>
    <label class="sb-volume"><i class="fas fa-volume-down" aria-hidden="true"></i><span class="sr-only">Volume</span><input id="sb-volume" aria-label="Playback volume" type="range" min="0" max="100" value="80"><i class="fas fa-volume-up" aria-hidden="true"></i></label>
  </section>

  <div class="sb-main-grid">
    <section class="sb-library" aria-labelledby="sb-library-heading">
      <div class="sb-section-head"><div><span class="sb-overline">THE SOUND LIBRARY</span><h2 id="sb-library-heading">Tiny noises, <em>huge character.</em></h2><p>Real recordings, split into individually playable moments. Most identities for these sounds still haven't been confirmed, and some of the playful noises are from one of the borb parents joining in.</p></div><div class="sb-count" id="sb-count" aria-live="polite">336 sounds</div></div>
      <div class="sb-filters"><div class="sb-tabs" role="group" aria-label="Filter sounds"><button type="button" class="sb-tab is-active" data-filter="all" aria-pressed="true">All chirps</button><button type="button" class="sb-tab" data-filter="favourites" aria-pressed="false"><i class="far fa-heart" aria-hidden="true"></i> Favourites <span id="sb-fav-count">0</span></button></div><label class="sb-search"><i class="fas fa-search" aria-hidden="true"></i><span class="sr-only">Search chirps</span><input id="sb-search" type="search" placeholder="Find a chirp…" autocomplete="off"></label></div>
      <div class="sb-clips" id="sb-clips" aria-live="off"><p class="sb-loading">Preparing your little flock of sounds…</p></div>
      <p class="sb-empty" id="sb-empty" hidden>No chirps here yet. Try a different search or filter.</p>
    </section>

    <aside class="sb-machine" aria-labelledby="sb-machine-heading">
      <div class="sb-machine-head"><div class="sb-machine-tag">THE BORB MACHINE <span aria-hidden="true">✳</span></div><h2 id="sb-machine-heading">Make some <em>noise.</em></h2><p>Queue up your favourite sounds, or fill to 10 randomly. Party Parrot plays the full library in shuffled rounds.</p></div>
      <div class="sb-machine-queue"><div class="sb-queue-heading"><strong>PLAY QUEUE</strong><span id="sb-queue-count">0 sounds</span></div><button type="button" class="sb-queue-ten" id="sb-queue-ten" disabled><i class="fas fa-random" aria-hidden="true"></i> Fill queue to 10</button><ol id="sb-queue" aria-label="Queued sounds"><li class="sb-queue-placeholder">It's quiet in here…<br>Add chirps using the <strong>+</strong> buttons.</li></ol></div>
      <div class="sb-machine-actions"><button class="sb-btn sb-btn-primary sb-machine-play" type="button" id="sb-play-queue" disabled><i class="fas fa-play" aria-hidden="true"></i> Play queue</button><div class="sb-machine-secondary"><button type="button" id="sb-shuffle" disabled><i class="fas fa-random" aria-hidden="true"></i> Shuffle</button><button type="button" id="sb-clear" disabled><i class="fas fa-trash-alt" aria-hidden="true"></i> Clear</button></div></div>
      <div class="sb-machine-footer"><i class="fas fa-heart" aria-hidden="true"></i> Made for the little personalities behind every beep.</div>
    </aside>
  </div>
  <footer class="sb-footer"><span>Channel Chirp · Soundborb v0.6</span><span>Original recordings preserved. Made with love for Pudge, Tillie, Chip, and one of the borb parents.</span></footer>
  <p class="sb-status sr-only" id="sb-status" role="status" aria-live="polite"></p>
</div>
<script src="{{ '/js/soundborb.js' | relative_url }}" defer></script>
---
layout: default
title: Search
show_hero: false
permalink: /search/
exclude_search: true
---

<div id="search"></div>
<script>
  window.addEventListener('DOMContentLoaded', () => {
    new PagefindUI({
      element: "#search",
      showSubResults: true,
      // Optional: show more results per page on the full‑width page
      autofocus: true
    });
  });
</script>
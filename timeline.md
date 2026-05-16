---
layout: default
title: Our Adventures Timeline
hide_sidebar: true
show_hero: false
body_class: timeline-page
permalink: /timeline/
exclude_search: true
---

<div class="timeline">

  {% assign sorted_posts = site.posts | sort: "date" %}
  {% for post in sorted_posts %}
  <div class="timeline-event">
    <span class="timeline-date">
      {% include ordinal_date.html date=post.date %}
    </span>
    <h3 class="timeline-title">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h3>
  </div>
  {% endfor %}

</div>
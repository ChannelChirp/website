---
layout: default
title: Our Adventures Timeline
hide_sidebar: true
show_hero: false
body_class: timeline-page
permalink: /timeline/
---

<div class="timeline">

  {% assign sorted_posts = site.posts | sort: "date" %}
  {% for post in sorted_posts %}
  <div class="timeline-event">
    <span class="timeline-date">
      {{ post.date | date: "%d %B %Y, %-I:%M %p" }}
    </span>
    <h3 class="timeline-title">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h3>
  </div>
  {% endfor %}

</div>
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
    <div class="timeline-content">
      <span class="timeline-date">{{ post.date | date: "%B %Y" }}</span>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      {% if post.excerpt %}
        <p>{{ post.excerpt | strip_html | truncatewords: 30 }}</p>
      {% endif %}
    </div>
  </div>
  {% endfor %}

</div>
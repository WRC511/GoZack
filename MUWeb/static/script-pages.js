(function () {
  'use strict';

  var PRODUCTS_URL = (function () {
    var base = document.querySelector('script[src*="script-pages.js"]');
    if (base && base.src) {
      var path = base.src.replace(/\/[^/]+$/, '/');
      return path + 'products.json';
    }
    return 'static/products.json';
  })();
  var LIKES_KEY = 'gozack-liked-ids';

  function getLikedIds() {
    try {
      var raw = localStorage.getItem(LIKES_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }

  function setLikedIds(ids) {
    localStorage.setItem(LIKES_KEY, JSON.stringify(ids));
  }

  function isLiked(id) {
    return getLikedIds().indexOf(id) !== -1;
  }

  function toggleLike(id) {
    var ids = getLikedIds();
    var i = ids.indexOf(id);
    if (i === -1) ids.push(id);
    else ids.splice(i, 1);
    setLikedIds(ids);
    return ids.indexOf(id) !== -1;
  }

  function getLikeCount(id, items) {
    return isLiked(id) ? 1 : 0;
  }

  function renderCard(item) {
    var liked = isLiked(item.id);
    var url = 'view.html?id=' + item.id;
    return (
      '<div class="col-md-4 mb-4">' +
        '<a href="' + url + '" class="card-link text-decoration-none">' +
          '<div class="card item-card" data-id="' + item.id + '">' +
            '<img src="' + item.image + '" class="card-img-top img-fluid" alt="' + item.title.replace(/"/g, '&quot;') + '">' +
            '<div class="card-body text-center">' +
              '<h5 class="card-title">' + item.title + '</h5>' +
              '<a href="' + url + '" class="btn btn-primary">View Details</a>' +
            '</div>' +
          '</div>' +
        '</a>' +
      '</div>'
    );
  }

  function initHome() {
    var el = document.getElementById('popular-items');
    if (!el) return;
    window.Pages.getProducts().then(function (items) {
      var liked = getLikedIds();
      items = items.slice().sort(function (a, b) {
        var aL = liked.indexOf(a.id) !== -1 ? 1 : 0;
        var bL = liked.indexOf(b.id) !== -1 ? 1 : 0;
        return bL - aL || (b.rating - a.rating);
      });
      items = items.slice(0, 3);
      el.innerHTML = items.map(renderCard).join('');
    });
  }

  function initSearch() {
    var resultsEl = document.getElementById('search-results');
    var queryEl = document.getElementById('search-query-text');
    if (!resultsEl) return;
    var params = new URLSearchParams(window.location.search);
    var q = (params.get('q') || '').trim().toLowerCase();
    if (queryEl) queryEl.textContent = q || '(empty)';
    window.Pages.getProducts().then(function (items) {
      var filtered = q
        ? items.filter(function (item) {
            return (
              item.title.toLowerCase().indexOf(q) !== -1 ||
              item.description.toLowerCase().indexOf(q) !== -1 ||
              (item.sizes && item.sizes.join(',').toLowerCase().indexOf(q) !== -1) ||
              (item.price && item.price.toLowerCase().indexOf(q) !== -1)
            );
          })
        : [];
      if (filtered.length === 0) {
        resultsEl.innerHTML = '<p class="text-center">No results found.</p>';
      } else {
        resultsEl.innerHTML = filtered.map(renderCard).join('');
      }
    });
  }

  function initView() {
    var container = document.getElementById('view-item-container');
    if (!container) return;
    var params = new URLSearchParams(window.location.search);
    var id = parseInt(params.get('id'), 10);
    if (!id) {
      container.innerHTML = '<p>Item not found.</p>';
      return;
    }
    window.Pages.getProducts().then(function (items) {
      var item = items.filter(function (i) { return i.id === id; })[0];
      if (!item) {
        container.innerHTML = '<p>Item not found.</p>';
        return;
      }
      var liked = isLiked(item.id);
      var likesNum = liked ? 1 : 0;
      container.innerHTML =
        '<h1 class="item-title mb-4">' + item.title + '</h1>' +
        '<div class="row align-items-start">' +
          '<div class="col-md-6">' +
            '<img src="' + item.image + '" class="img-fluid rounded shadow-sm w-100" alt="' + item.title.replace(/"/g, '&quot;') + '">' +
          '</div>' +
          '<div class="col-md-6">' +
            '<div class="card h-100">' +
              '<div class="card-body d-flex flex-column">' +
                '<p class="card-text"><strong>Description:</strong> ' + item.description + '</p>' +
                '<p><strong>Price:</strong> ' + item.price + '</p>' +
                '<p><strong>Rating:</strong> ' + item.rating + ' ⭐</p>' +
                '<p><strong>Sizes Available:</strong> ' + (item.sizes ? item.sizes.join(', ') : '') + '</p>' +
                '<p><strong>Similar Items:</strong> ' + (item.similar_items ? item.similar_items.join(', ') : '') + '</p>' +
                '<div class="mt-auto">' +
                  '<button class="btn btn-primary like-btn-pages" data-id="' + item.id + '">' +
                    (liked ? 'Unlike' : 'Like') + ' (<span id="likes-' + item.id + '">' + likesNum + '</span>)' +
                  '</button>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>';
      var btn = container.querySelector('.like-btn-pages');
      var span = document.getElementById('likes-' + item.id);
      if (btn && span) {
        btn.addEventListener('click', function () {
          var nowLiked = toggleLike(item.id);
          btn.textContent = (nowLiked ? 'Unlike' : 'Like') + ' (' + (nowLiked ? 1 : 0) + ')';
          span.textContent = nowLiked ? 1 : 0;
        });
      }
    });
  }

  function initLikes() {
    var el = document.getElementById('liked-items');
    if (!el) return;
    var likedIds = getLikedIds();
    window.Pages.getProducts().then(function (items) {
      var liked = items.filter(function (i) { return likedIds.indexOf(i.id) !== -1; });
      if (liked.length === 0) {
        el.innerHTML = '<p class="text-center">You haven\'t liked any items yet.</p>';
        return;
      }
      el.innerHTML = liked.map(function (item) {
        var url = 'view.html?id=' + item.id;
        return (
          '<div class="col-md-4 mb-4">' +
            '<div class="card item-card" data-id="' + item.id + '">' +
              '<img src="' + item.image + '" class="card-img-top img-fluid" alt="' + item.title.replace(/"/g, '&quot;') + '">' +
              '<div class="card-body">' +
                '<div class="card-content">' +
                  '<h5 class="card-title">' + item.title + '</h5>' +
                  '<p><strong>Price:</strong> ' + item.price + '</p>' +
                  '<p><strong>Rating:</strong> ' + item.rating + ' ⭐</p>' +
                '</div>' +
                '<div class="card-footer text-center">' +
                  '<a href="' + url + '" class="btn btn-primary view-btn">View Details</a> ' +
                  '<button type="button" class="btn btn-danger delete-btn-pages" data-id="' + item.id + '">Remove</button>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</div>'
        );
      }).join('');
      el.querySelectorAll('.delete-btn-pages').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var id = parseInt(btn.getAttribute('data-id'), 10);
          toggleLike(id);
          initLikes();
        });
      });
    });
  }

  function initNav() {
    var form = document.getElementById('search-form-pages');
    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var input = document.getElementById('search-input-pages');
        var q = (input && input.value) ? input.value.trim() : '';
        window.location.href = 'search.html?q=' + encodeURIComponent(q);
      });
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    initNav();
    initHome();
    initSearch();
    initView();
    initLikes();
  });

  window.Pages = window.Pages || {};
  window.Pages.getProducts = function () {
    return fetch(PRODUCTS_URL).then(function (r) { return r.json(); });
  };
  window.Pages.getLikedIds = getLikedIds;
  window.Pages.isLiked = isLiked;
  window.Pages.toggleLike = toggleLike;
  window.Pages.getLikeCount = getLikeCount;
  window.Pages.productUrl = function (id) { return 'view.html?id=' + id; };
  window.Pages.searchUrl = function (q) { return 'search.html?q=' + encodeURIComponent(q); };
  window.Pages.likesUrl = 'likes.html';
  window.Pages.homeUrl = 'index.html';
})();

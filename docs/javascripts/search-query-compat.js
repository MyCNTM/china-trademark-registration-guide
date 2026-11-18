// Preserve older goods links before Material interprets q as a site-wide search.
(function () {
  var url = new URL(window.location.href);
  if (url.searchParams.has('q')) {
    if (!url.searchParams.has('goods')) url.searchParams.set('goods', url.searchParams.get('q'));
    url.searchParams.delete('q');
    window.history.replaceState(null, '', url.pathname + url.search + url.hash);
  }
})();

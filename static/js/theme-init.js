/* Apply saved theme before first paint. Load synchronously in <head>. */
(function () {
    try {
        var light = localStorage.getItem('theme') === 'light';
        document.documentElement.classList.toggle('dark', !light);
    } catch (e) {
        document.documentElement.classList.add('dark');
    }
})();
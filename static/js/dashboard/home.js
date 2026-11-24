/**
 * OfficeSync - Dashboard filtering, live search and counts
 */
(function () {
    'use strict';

    var activeStatus = 'all';

    function cards() {
        return document.querySelectorAll('#faculty-grid .faculty-card');
    }

    function apply() {
        var input = document.getElementById('live-search-input');
        var term = input ? input.value.trim().toLowerCase() : '';
        var counts = { all: 0, IN_OFFICE: 0, IN_CLASS: 0, ON_BREAK: 0, OUT: 0 };
        var visible = 0;
        var total = 0;

        cards().forEach(function (card) {
            total++;
            var haystack = (card.dataset.search || card.textContent).toLowerCase();
            var matchesSearch = !term || haystack.indexOf(term) !== -1;
            if (matchesSearch) {
                counts.all++;
                if (counts[card.dataset.status] !== undefined) counts[card.dataset.status]++;
            }
            var show = matchesSearch && (activeStatus === 'all' || card.dataset.status === activeStatus);
            card.style.display = show ? 'flex' : 'none';
            if (show) visible++;
        });

        document.querySelectorAll('.filter-pill-btn').forEach(function (btn) {
            var c = btn.querySelector('.pill-count');
            if (c) c.textContent = counts[btn.dataset.filter];
        });

        var v = document.getElementById('visible-faculty-count');
        var t = document.getElementById('total-faculty-count');
        if (v) v.textContent = visible;
        if (t) t.textContent = total;

        var empty = document.getElementById('empty-state');
        if (empty) empty.hidden = visible !== 0 || total === 0;
    }

    function setStatus(status) {
        activeStatus = status;
        document.querySelectorAll('.filter-pill-btn').forEach(function (btn) {
            var on = btn.dataset.filter === status;
            btn.classList.toggle('active', on);
            btn.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        apply();
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.filter-pill-btn').forEach(function (btn) {
            btn.addEventListener('click', function () { setStatus(btn.dataset.filter); });
        });

        var input = document.getElementById('live-search-input');
        if (input) {
            input.addEventListener('input', apply);
            // Press "/" to jump to search (unless already typing in a field)
            document.addEventListener('keydown', function (e) {
                var tag = (document.activeElement && document.activeElement.tagName) || '';
                if (e.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(tag)) {
                    e.preventDefault();
                    input.focus();
                }
            });
        }

        var reset = document.getElementById('reset-filters');
        if (reset) {
            reset.addEventListener('click', function () {
                if (input) input.value = '';
                setStatus('all');
            });
        }

        // Open the native time picker on click
        var backAtInput = document.getElementById('back-at-time');
        if (backAtInput && typeof backAtInput.showPicker === 'function') {
            backAtInput.addEventListener('click', function () {
                try { backAtInput.showPicker(); } catch (e) { /* already open or restricted */ }
            });
        }

        apply();
    });
})();
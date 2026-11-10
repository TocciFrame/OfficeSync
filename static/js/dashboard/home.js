/**
 * OfficeSync - Dashboard Interactive Filtering
 */
function filterStatus(status) {
    const cards = document.querySelectorAll('.faculty-card');
    const filterBtns = document.querySelectorAll('.filter-pill-btn');
    
    filterBtns.forEach(btn => btn.classList.remove('active'));

    if (event && event.currentTarget) {
        event.currentTarget.classList.add('active');
    }

    let visibleCount = 0;
    cards.forEach(card => {
        if (status === 'all' || card.dataset.status === status) {
            card.style.display = 'flex';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });

    const countElem = document.getElementById('visible-faculty-count');
    if (countElem) {
        countElem.textContent = visibleCount;
    }
}
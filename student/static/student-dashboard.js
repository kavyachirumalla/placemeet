function toggleMenu() {
    const sidebar = document.getElementById("sidebar");
    if (!sidebar) return;
    sidebar.classList.toggle("open");
}

    function showSection(menuItem) {
        const target = menuItem.dataset.target;

        document.querySelectorAll('.section').forEach(sec => {
            sec.classList.remove('active');
        });
        document.getElementById(target).classList.add('active');

        document.querySelectorAll('.sidebar li').forEach(li => {
            li.classList.remove('active');
        });
        menuItem.classList.add('active');
    }
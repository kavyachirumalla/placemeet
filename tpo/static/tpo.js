function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("open");
}

// handle sidebar sections
function showSection(liElement) {
    const targetId = liElement.getAttribute("data-target");

    // sidebar active state
    document.querySelectorAll("#sidebar li").forEach(li => {
        li.classList.remove("active");
    });
    liElement.classList.add("active");

    // sections
    document.querySelectorAll(".section").forEach(sec => {
        sec.classList.remove("active");
    });
    const target = document.getElementById(targetId);
    if (target) target.classList.add("active");
}
// Toggle sidebar open / close
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("hidden");
}

// Switch sections based on sidebar click
function showSection(clickedLi) {
    const targetId = clickedLi.getAttribute("data-target");

    // update active item in sidebar
    document.querySelectorAll(".sidebar li").forEach(li => {
        li.classList.remove("active");
    });
    clickedLi.classList.add("active");

    // show / hide sections
    document.querySelectorAll(".section").forEach(sec => {
        sec.classList.remove("active");
    });
    const targetSection = document.getElementById(targetId);
    if (targetSection) {
        targetSection.classList.add("active");
        // when on small screens, hide sidebar after choosing
        if (window.innerWidth <= 960) {
            document.getElementById("sidebar").classList.add("hidden");
        }
    }
}

// Dummy JS hooks for buttons, so they don’t crash.
// You’ll wire these to Django views with AJAX or normal forms later.

function shortlistCandidate(btn) {
    const appId = btn.getAttribute("data-app-id");
    console.log("Shortlist application: ", appId);
    // TODO: send POST request to Django to mark as shortlisted
    alert("Shortlist logic will go here (connect to backend).");
}

function removeFromFinal(btn) {
    const finalId = btn.getAttribute("data-final-id");
    console.log("Remove from final list: ", finalId);
    // TODO: send POST request to Django to remove from final list
    alert("Remove-from-final logic will go here (connect to backend).");
}
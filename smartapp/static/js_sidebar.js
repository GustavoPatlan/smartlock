let sidebar = document.getElementById("sidebar");
let toggleIcon = document.getElementById("togle_icon");
let backdrop = document.getElementById("backdrop");

function toggleSidebar() {
    sidebar.classList.toggle("collapsed");

    if (sidebar.classList.contains("collapsed")) {
        toggleIcon.setAttribute("name", "menu-outline");
        backdrop.style.display = "none";
    } else {
        toggleIcon.setAttribute("name", "close-outline");
        backdrop.style.display = "block";
    }
}

function ajustarSidebar() {
    if (window.innerWidth <= 900) {
        sidebar.classList.add("collapsed");
        toggleIcon.setAttribute("name", "menu-outline");
        backdrop.style.display = "none";
    } else {
        sidebar.classList.remove("collapsed");
        toggleIcon.setAttribute("name", "close-outline");
        backdrop.style.display = "block";
    }
}

function openDialog() {
    let dialog = document.getElementById("logoutDialog");
    dialog.showModal();
}

function closeDialog() {
    let dialog = document.getElementById("logoutDialog");
    dialog.close();
}

ajustarSidebar();

window.addEventListener("resize", ajustarSidebar);
document.getElementById('menu-toggle').addEventListener('click', function() {
    const menu = document.querySelector('.menu');
    window.CloseAllModalWindows()
    menu.classList.toggle('show');
});

window.addEventListener("beforeunload", () => {
    localStorage.setItem("scrollPositon", document.querySelector(".tasks_list").scrollTop);
});

window.addEventListener("load", () => {
    document.querySelector(".tasks_list").scrollTop = localStorage.getItem("scrollPositon") || 0;
});
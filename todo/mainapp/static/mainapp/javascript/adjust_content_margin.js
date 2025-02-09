window.addEventListener("resize", adjustContentMargin); // Adjust on window resize
window.addEventListener("load", adjustContentMargin);    // Adjust when the page loads

function adjustContentMargin() {
    const menu = document.querySelector(".menu");
    const content = document.querySelector(".content");

    if (menu && content) {
        const menuWidth = menu.offsetWidth; // Get the width of the menu
        content.style.marginLeft = `${menuWidth}px`; // Set margin-left of content
    }
}
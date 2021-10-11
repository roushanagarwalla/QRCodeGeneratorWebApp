function remove_result() {
    let img = document.getElementById('results').remove();
}

const color_mode = localStorage.getItem('color-mode');
if (color_mode != null) {
    document.documentElement.setAttribute('color-mode', color_mode);
}

if (window.CSS && CSS.supports("color", "var(--primary)")) {
    var toggleColorMode = function toggleColorMode(e) {
        if (e.currentTarget.classList.contains("light--hidden")) {
            document.documentElement.setAttribute("color-mode", "light");

            localStorage.setItem("color-mode", "light");
            return;
        }
        document.documentElement.setAttribute("color-mode", "dark");

        localStorage.setItem("color-mode", "dark");
    };

    var toggleColorButtons = document.querySelectorAll(".color-mode__btn");

    toggleColorButtons.forEach(function (btn) {
        btn.addEventListener("click", toggleColorMode);
    });
} else {
    var btnContainer = document.querySelector(".color-mode__header");
    btnContainer.style.display = "none";
}
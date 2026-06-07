/* Loading state management for AI-generation forms */
(function () {
    "use strict";

    function showLoading(btn, label) {
        btn.disabled = true;
        btn.dataset.originalHtml = btn.innerHTML;
        btn.innerHTML = '<span class="spinner-xs"></span>' + label;
    }

    function restoreBtn(btn) {
        btn.disabled = false;
        if (btn.dataset.originalHtml) {
            btn.innerHTML = btn.dataset.originalHtml;
            delete btn.dataset.originalHtml;
        }
    }

    // Prompt form — generate user story
    const promptForm = document.getElementById("prompt-form");
    if (promptForm) {
        promptForm.addEventListener("submit", function () {
            const textarea = promptForm.querySelector("textarea[name='prompt']");
            if (!textarea || !textarea.value.trim()) return;
            const btn = promptForm.querySelector("[type='submit']");
            if (btn) showLoading(btn, "Generando historia…");
        });
    }

    // Generate-tasks forms (one per story row)
    document.querySelectorAll(".form-generate-tasks").forEach(function (form) {
        form.addEventListener("submit", function () {
            const btn = form.querySelector("button[type='submit']");
            if (btn) {
                btn.classList.add("btn-generate");
                showLoading(btn, "Generando…");
            }
        });
    });
})();

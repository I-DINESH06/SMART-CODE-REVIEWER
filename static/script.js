// ===============================
// COPY OPTIMIZED CODE
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const copyButton = document.getElementById("copyButton");

    if (copyButton) {

        copyButton.addEventListener("click", function () {

            const code = document.getElementById("optimizedCode").innerText;

            navigator.clipboard.writeText(code)
                .then(() => {

                    const originalText = copyButton.innerHTML;

                    copyButton.innerHTML = "✅ Copied!";

                    copyButton.style.background = "#16a34a";

                    setTimeout(() => {

                        copyButton.innerHTML = originalText;

                        copyButton.style.background = "#2563eb";

                    }, 2000);

                })
                .catch(err => {

                    alert("Failed to copy code.");

                    console.error(err);

                });

        });

    }

});
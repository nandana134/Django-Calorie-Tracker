// Auto-hide success/error messages
document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        }, 3000); // 3 seconds
    });
});

// Confirm delete popup
function confirmDelete(event) {
    if (!confirm("Are you sure you want to delete this item?")) {
        event.preventDefault();
    }
}

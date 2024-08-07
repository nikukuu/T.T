document.addEventListener('DOMContentLoaded', () => {
    // Get the popup elements
    const popups = {
        addExpense: document.getElementById("add-expense-popup"),
        settleMethod: document.getElementById("settle-method-popup"),
        settleDetails: document.getElementById("settle-details-popup"),
        customAmount: document.getElementById("custom-amount-popup"),
        editExpense: document.getElementById("edit-expense-popup")
    };

    // Show or hide popup
    function showPopup(popup) {
        popup.style.display = "block";
    }

    function hidePopup(popup) {
        popup.style.display = "none";
    }

    // Add Expense Popup
    document.querySelector(".button-container button:first-of-type").onclick = () => showPopup(popups.addExpense);
    popups.addExpense.querySelector(".close").onclick = () => hidePopup(popups.addExpense);

    // Settle Up Popups
    document.querySelector(".button-container button:last-of-type").onclick = () => showPopup(popups.settleMethod);
    document.getElementById("cash").onclick = () => {
        hidePopup(popups.settleMethod);
        showPopup(popups.settleDetails);
    };
    document.getElementById("e-wallet").onclick = () => {
        hidePopup(popups.settleMethod);
        showPopup(popups.settleDetails);
    };
    popups.settleMethod.querySelector(".close-settle-method").onclick = () => hidePopup(popups.settleMethod);
    popups.settleDetails.querySelector(".close-settle-details").onclick = () => hidePopup(popups.settleDetails);

    // Custom Amount Popup
    document.getElementById("split").onchange = function() {
        if (this.value === "custom") {
            showPopup(popups.customAmount);
        } else {
            hidePopup(popups.customAmount);
        }
    };
    popups.customAmount.querySelector(".close-custom-amount").onclick = () => hidePopup(popups.customAmount);

    // Edit Expense Popup
    document.querySelectorAll(".expense-item button:first-of-type").forEach(button => {
        button.onclick = () => showPopup(popups.editExpense);
    });
    popups.editExpense.querySelector(".close-edit-expense").onclick = () => hidePopup(popups.editExpense);

    // Close popups if clicking outside
    window.onclick = function(event) {
        Object.values(popups).forEach(popup => {
            if (event.target === popup) {
                hidePopup(popup);
            }
        });
    };

    // Populate user options
    const users = ['User1', 'User2', 'User3']; // Replace with actual user list
    ['paid-by', 'paid-to'].forEach(id => {
        const select = document.getElementById(id);
        users.forEach(user => {
            const option = document.createElement('option');
            option.value = user;
            option.textContent = user;
            select.appendChild(option);
        });
    });
});
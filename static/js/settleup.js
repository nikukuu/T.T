// Function to open the Add Expense popup
function openAddExpensePopup(roomId) {
    document.getElementById('popupRoomId').value = roomId;
    document.getElementById('addExpensePopup').style.display = 'block';
}

// Function to close the Add Expense popup
function closeAddExpensePopup() {
    document.getElementById('addExpensePopup').style.display = 'none';
}

// Function to open the Settle Up popup
function openSettleUpPopup(roomId) {
    document.getElementById('settleUpPopup').style.display = 'block';
}

// Function to close the Settle Up popup
function closeSettleUpPopup() {
    document.getElementById('settleUpPopup').style.display = 'none';
}

// Close the popups when clicking outside of the popup content
window.onclick = function(event) {
    if (event.target == document.getElementById('addExpensePopup')) {
        closeAddExpensePopup();
    } else if (event.target == document.getElementById('settleUpPopup')) {
        closeSettleUpPopup();
    }
}

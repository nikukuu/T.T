// Function to open the Add Expense popup
function openAddExpensePopup(roomId) {
    document.getElementById('popupRoomId').value = roomId;
    document.getElementById('addExpensePopup').style.display = 'block';
}

// Function to close the Add Expense popup
function closeAddExpensePopup() {
    document.getElementById('addExpensePopup').style.display = 'none';
}

// Close the popup when clicking outside of the popup content
window.onclick = function(event) {
    if (event.target == document.getElementById('addExpensePopup')) {
        closeAddExpensePopup();
    }
}

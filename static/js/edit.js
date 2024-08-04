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
    // Set the room ID if necessary or handle according to your needs
    document.getElementById('settleUpPopup').style.display = 'block';
}

// Function to close the Settle Up popup
function closeSettleUpPopup() {
    document.getElementById('settleUpPopup').style.display = 'none';
}

// Function to open the Edit Expense popup
function openEditExpensePopup(expenseId, description, amount, paidBy) {
    document.getElementById('editExpenseId').value = expenseId;
    document.getElementById('editDescription').value = description;
    document.getElementById('editAmount').value = amount;
    document.getElementById('editPaidBy').value = paidBy;
    document.getElementById('editExpensePopup').style.display = 'block';
}

// Function to close the Edit Expense popup
function closeEditExpensePopup() {
    document.getElementById('editExpensePopup').style.display = 'none';
}

// Close the popups when clicking outside of the popup content
window.onclick = function(event) {
    if (event.target == document.getElementById('addExpensePopup')) {
        closeAddExpensePopup();
    } else if (event.target == document.getElementById('settleUpPopup')) {
        closeSettleUpPopup();
    } else if (event.target == document.getElementById('editExpensePopup')) {
        closeEditExpensePopup();
    }
}

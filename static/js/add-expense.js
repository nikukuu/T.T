document.addEventListener('DOMContentLoaded', () => {
    const addExpenseBtn = document.querySelector('.add-expense');
    const addExpensePopup = document.getElementById('add-expense-popup');
    const editExpenseButtons = document.querySelectorAll('.edit-expense');
    const editExpensePopup = document.getElementById('edit-expense-popup');
    const settleUpBtn = document.querySelector('.settle-up');
    const settleMethodPopup = document.getElementById('settle-method-popup');
    const settleDetailsPopup = document.getElementById('settle-details-popup');
    const cashBtn = document.getElementById('cash');
    const eWalletBtn = document.getElementById('e-wallet');
    const closeButtons = document.querySelectorAll('.close');
    const cancelSettleDetailsBtn = document.getElementById('cancel-settle-details');
    const cancelCustomAmountBtn = document.getElementById('cancel-custom-amount');
    
    // Show the Add Expense popup
    addExpenseBtn.addEventListener('click', () => {
        addExpensePopup.style.display = 'block';
    });

    // Show the Edit Expense popup
    editExpenseButtons.forEach(button => {
        button.addEventListener('click', () => {
            editExpensePopup.style.display = 'block';
        });
    });

    // Show the Settle Method popup
    settleUpBtn.addEventListener('click', () => {
        settleMethodPopup.style.display = 'block';
    });

    // Show the Settle Details popup when "Cash" is selected
    cashBtn.addEventListener('click', () => {
        settleMethodPopup.style.display = 'none';
        settleDetailsPopup.style.display = 'block';
    });

    // Show the Settle Details popup when "E-wallet" is selected
    eWalletBtn.addEventListener('click', () => {
        settleMethodPopup.style.display = 'none';
        settleDetailsPopup.style.display = 'block';
    });

    // Close the popup when clicking on the close button
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.parentElement.parentElement.style.display = 'none';
        });
    });

    // Close the popup when clicking on the cancel button in the settle details form
    cancelSettleDetailsBtn.addEventListener('click', () => {
        settleDetailsPopup.style.display = 'none';
    });

    // Close the popup when clicking on the cancel button in the custom amount form
    cancelCustomAmountBtn.addEventListener('click', () => {
        document.getElementById('custom-amount-popup').style.display = 'none';
    });

    // Close the popup when clicking outside of the popup content
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('popup')) {
            event.target.style.display = 'none';
        }
    });
});

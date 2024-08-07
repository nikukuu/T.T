document.addEventListener('DOMContentLoaded', () => {
    // Popup elements
    const addExpenseBtn = document.querySelector('.add-expense');
    const addExpensePopup = document.getElementById('add-expense-popup');
    const editExpenseButtons = document.querySelectorAll('.edit-expense');
    const editExpensePopup = document.getElementById('edit-expense-popup');
    const settleUpBtn = document.querySelector('.settle-up');
    const settleForm = document.getElementById('settle-form'); // Directly accessible settle form
    const closeButtons = document.querySelectorAll('.close');
    const cancelSettleDetailsBtn = document.getElementById('cancel-settle-details');
    const editExpenseForm = document.getElementById('editExpenseForm');
    const removeExpenseButtons = document.querySelectorAll('.remove-expense');

    // Show the Add Expense popup
    addExpenseBtn.addEventListener('click', () => {
        addExpensePopup.style.display = 'block';
    });

    // Show the Edit Expense popup
    editExpenseButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const expenseItem = e.target.closest('.expense-item');
            const expenseId = expenseItem.dataset.id;
            const description = expenseItem.querySelector('.item').textContent;
            const amount = expenseItem.querySelector('.price').textContent;
            const paidBy = expenseItem.querySelector('.paid-by').textContent.replace('Paid by: ', '');

            // Fill the form with existing data
            document.getElementById('expense_id').value = expenseId;
            document.getElementById('edit_description').value = description;
            document.getElementById('edit_amount').value = amount;
            document.getElementById('edit_paid_by').value = paidBy;

            // Show the popup
            editExpensePopup.style.display = 'block';
        });
    });

    // Handle the Edit Expense form submission
    editExpenseForm.onsubmit = async function (e) {
        e.preventDefault();

        const expenseId = document.getElementById('expense_id').value;
        const description = document.getElementById('edit_description').value;
        const amount = document.getElementById('edit_amount').value;
        const paidBy = document.getElementById('edit_paid_by').value;

        const response = await fetch(`/session/{{ room_id }}/edit_expense/${expenseId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ description, amount, paid_by: paidBy }),
        });

        if (response.ok) {
            // Update the expense item in the list
            const expenseItem = document.querySelector(`.expense-item[data-id="${expenseId}"]`);
            expenseItem.querySelector('.item').textContent = description;
            expenseItem.querySelector('.price').textContent = amount;
            expenseItem.querySelector('.paid-by').textContent = `Paid by: ${paidBy}`;

            // Close the popup
            editExpensePopup.style.display = 'none';
        } else {
            alert('Failed to edit expense');
        }
    };

    // Handle the Remove Expense button clicks
    removeExpenseButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            const expenseItem = e.target.closest('.expense-item');
            const expenseId = expenseItem.dataset.id;

            const response = await fetch(`/session/{{ room_id }}/remove_expense/${expenseId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                // Remove the expense item from the list
                expenseItem.remove();
            } else {
                alert('Failed to remove expense');
            }
        });
    });

    // Show the Settle Form directly
    settleUpBtn.addEventListener('click', () => {
        settleForm.style.display = 'block';
    });

    // Handle the Settle Form submission
    settleForm.onsubmit = async function (e) {
        e.preventDefault();

        const amount = document.getElementById('settle_amount').value;
        const paidBy = document.getElementById('settle_paid_by').value;
        const receivedBy = document.getElementById('settle_received_by').value;
        const date = document.getElementById('settle_date').value;

        const response = await fetch(`/session/{{ room_id }}/settle`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount, paid_by: paidBy, received_by: receivedBy, date }),
        });

        if (response.ok) {
            // Handle successful settlement (e.g., update UI, show message)
            alert('Settlement successful');
            settleForm.style.display = 'none';
        } else {
            alert('Failed to settle');
        }
    };

    // Close the popup when clicking the close button
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.parentElement.parentElement.style.display = 'none';
        });
    });

    // Close the popup when clicking outside of the popup content
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('popup-overlay')) {
            event.target.style.display = 'none';
        }
    });
});

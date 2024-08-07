document.addEventListener('DOMContentLoaded', () => {
    const settleForm = document.getElementById('settle-form');
    const cancelSettleDetailsBtn = document.getElementById('cancel-settle-details');

    // Handle the Settle Form submission
    settleForm.onsubmit = async function (e) {
        e.preventDefault();

        const payer = document.getElementById('payer').value;
        const recipient = document.getElementById('recipient').value;
        const amount = document.getElementById('amount').value;
        const date = document.getElementById('date').value;
        const paymentMethod = document.getElementById('payment_method').value;

        const response = await fetch(`/session/{{ room_id }}/settle`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ payer, recipient, amount, date, payment_method: paymentMethod }),
        });

        const result = await response.json();

        if (result.status === 'success') {
            alert('Settlement successful');
            settleForm.reset(); // Reset the form
        } else {
            alert('Failed to settle');
        }
    };

    // Handle the Cancel button click
    cancelSettleDetailsBtn.addEventListener('click', () => {
        settleForm.reset(); // Reset the form
    });
});

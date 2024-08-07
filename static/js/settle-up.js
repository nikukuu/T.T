document.getElementById("settle-method-popup").onclick = function(e) {
    if (e.target.id === 'cash' || e.target.id === 'e-wallet') {
        document.getElementById('settle-method-popup').style.display = 'none';
        document.getElementById('settle-details-popup').style.display = 'block';
    }
};

// Populate members in settle-up popup
const members = {{ members | tojson }};
const paidBySelect = document.getElementById('settle-paid-by');
const paidToSelect = document.getElementById('settle-paid-to');

members.forEach(member => {
    const option = document.createElement('option');
    option.value = member.username;
    option.textContent = member.username;
    paidBySelect.appendChild(option);

    const optionTo = option.cloneNode(true);
    paidToSelect.appendChild(optionTo);
});

// Handle settle-up form submission
document.getElementById("settle-details-form").onsubmit = async function (e) {
    e.preventDefault();

    const paidBy = document.getElementById("settle-paid-by").value;
    const paidTo = document.getElementById("settle-paid-to").value;
    const amountPaid = document.getElementById("amount-paid").value;
    const date = document.getElementById("date").value;
    const roomId = {{ room_info['room_id'] }}; // Ensure room_id is passed correctly

    const response = await fetch(`/settle/${roomId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ paid_by: paidBy, paid_to: paidTo, amount: amountPaid, date: date }),
    });

    if (response.ok) {
        const newSettlement = await response.json();
        // Add the new settlement to the expense list or handle accordingly

        // Close the popup and reset the form
        document.getElementById('settle-details-popup').style.display = 'none';
        document.getElementById('settle-details-form').reset();

        window.location.reload();
    } else {
        alert("Error in settlement");
    }
};

// Close popups
document.querySelectorAll('.close').forEach(button => {
    button.onclick = function () {
        this.parentElement.parentElement.style.display = 'none';
    }
});

// Cancel buttons
document.getElementById('cancel-settle-details').onclick = function () {
    document.getElementById('settle-details-popup').style.display = 'none';
};

function addExpense() {
  let name = document.getElementById("name").value.trim();
  let amount = parseFloat(document.getElementById("amount").value);
  let errorMessage = document.getElementById("error-message");

  if (!name || isNaN(amount) || amount <= 0) {
    errorMessage.textContent = "Please enter a valid name and positive amount.";
    return;
  }

  errorMessage.textContent = "";

  fetch("/add_expense", {
    method: "POST",
    body: JSON.stringify({ name, amount }),
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        errorMessage.textContent = data.error;
      } else {
        alert(data.message);
        document.getElementById("name").value = "";
        document.getElementById("amount").value = "";
        fetchBalances();
      }
    });
}

function fetchBalances() {
  fetch("/get_balances")
    .then((response) => response.json())
    .then((data) => {
      let balanceList = document.getElementById("balance-list");
      balanceList.innerHTML = "";

      if (data.error) {
        balanceList.innerHTML = `<li>${data.error}</li>`;
        return;
      }

      for (let name in data) {
        let balance = data[name].toFixed(2);
        let listItem = document.createElement("li");
        if (balance > 0) {
          listItem.textContent = `${name} should receive ₹${balance}`;
          listItem.style.color = "green";
        } else if (balance < 0) {
          listItem.textContent = `${name} should pay ₹${-balance}`;
          listItem.style.color = "red";
        } else {
          listItem.textContent = `${name} is settled.`;
        }
        balanceList.appendChild(listItem);
      }
    });
}

document.addEventListener("DOMContentLoaded", fetchBalances);

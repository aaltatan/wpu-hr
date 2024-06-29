resetTableIdx();
addEventListenersToDeleteBtns();

function addEventListenersToDeleteBtns() {
  const event = "htmx:afterRequest";
  const listener = () => {
    document.getElementById("messages").click();
    document.getElementById("staff-reset-btn").click();
    decreaseTotals();
    resetTableIdx();
  };
  var deleteBtns = document.querySelectorAll('button[itemprop="delete"]');
  deleteBtns.forEach((btn) => {
    btn.removeEventListener(event, listener);
    btn.addEventListener(event, listener);
  });
}

function decreaseTotals() {
  const filteredTotalSpan = document.getElementById('filtered-total');
  const totalSpan = document.getElementById('total');

  let total = +totalSpan.innerHTML;
  
  if (total > 0) {
    let newTotal = --total;
    totalSpan.innerHTML = newTotal;
    filteredTotalSpan.innerHTML = newTotal;
  }
}

function resetTableIdx() {
  const rowIdxs = document.querySelectorAll(".row-idx");
  let idx = 1;
  if (rowIdxs.length) {
    rowIdxs.forEach((el) => {
      el.parentElement
        .querySelector("button[id^=staff-countable-toggle-btn-]")
        .setAttribute("hx-headers", `{"row-idx": "${idx}"}`);
      el.innerHTML = idx++;
    });
  }
}

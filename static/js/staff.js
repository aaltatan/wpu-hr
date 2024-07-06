resetTableIdx();
addEventListenersToBtns();

function addEventListenersToBtns() {
  const event = "htmx:afterRequest";

  const deleteListener = () => {
    document.getElementById("messages").click();
    document.getElementById("staff-reset-btn").click();
    decreaseTotals();
    resetTableIdx();
  };

  var deleteBtns = document.querySelectorAll('button[itemprop="delete"]');
  deleteBtns.forEach((btn) => {
    btn.removeEventListener(event, deleteListener);
    btn.addEventListener(event, deleteListener);
  });

  var navigationBtns = document.querySelectorAll('button[role="navigation"]');
  navigationBtns.forEach((btn) => {
    btn.removeEventListener(event, resetTableIdx);
    btn.addEventListener(event, resetTableIdx);
  });

}

function decreaseTotals() {
  const filteredTotalSpan = document.getElementById("filtered-total");
  const totalSpan = document.getElementById("total");

  let total = +totalSpan.innerHTML;
  let filteredTotal = +filteredTotalSpan.innerHTML;

  if (total > 0) {
    total = total - 1;
    filteredTotal = filteredTotal - 1;

    totalSpan.innerHTML = total;
    filteredTotalSpan.innerHTML = filteredTotal;
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

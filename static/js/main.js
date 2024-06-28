resetTableIdx();

function removeErrorList() {
  const errorLists = document.querySelectorAll(".errorlist");
  errorLists.forEach((el) => el.remove());
}

function resetTableIdx() {
  const rowIdxs = document.querySelectorAll(".row-idx");
  let idx = 1;
  if (rowIdxs.length) {
    rowIdxs.forEach((el) => {
      el
        .parentElement
        .querySelector('button[id^=staff-countable-toggle-btn-]')
        .setAttribute('hx-headers', `{"row-idx": "${idx}"}`)
      el.innerHTML = idx++;
    });
  }
}

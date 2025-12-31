// Common JS (depends on jQuery being loaded before this file)
$(function () {
  // Insert today's date on biodata page
  const $date = $("#currentDate");
  if ($date.length) {
    const today = new Date();
    $date.text(today.toLocaleDateString());
  }

  // Small UX: highlight current nav link
  const path = window.location.pathname.split("/").pop();
  $(".nav-links a").each(function () {
    const href = $(this).attr("href");
    if (href === path)
      $(this).css({ "font-weight": "600", color: "var(--accent)" });
  });
});

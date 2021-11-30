"use strict";

function setLightMode() {
  localStorage.setItem("dark_mode_on", "0");

  // set icons to the correct color
  // $("#dark-mode-icon").attr("src", "../static/images/DarkMode.svg");
  // $(".printer-icon").attr("src", "../static/images/Printer_dark.svg");
  // $(".caret-down-icon").attr("src", "../static/images/CaretDown_dark.svg");
  // $(".plus-icon").attr("src", "../static/images/Plus_dark.svg");
  // $(".lab-summary-options").attr(
  //   "src",
  //   "../static/images/GearSix_dark.svg"
  // );
  $(".light-icon").addClass("invisible-icon");
  $(".dark-icon").removeClass("invisible-icon");

  if (localStorage.getItem("menu_open") === "1")
  $(".hamburger-icon").addClass("invisible-icon")
  else $(".x-icon").addClass("invisible-icon")

<<<<<<< HEAD
  if (localStorage.getItem("money_mode_on") === "1") {
    $(".money-mode-icon").addClass("invisible-icon")
    $(".green-icon").removeClass("invisible-icon")
  }
  else $(".green-icon").addClass("invisible-icon")

  $(".report-widget-internal-container").addClass("light-report-widget-nest");
  $(".report-widget-internal-container").removeClass("report-widget-nest");
=======
  if (localStorage.getItem("money_mode_on") === "1")
    $("#money-mode-icon").attr("src", "../static/images/MoneyMode_green.svg");
  else {
    $("#money-mode-icon").attr("src", "../static/images/MoneyMode_dark.svg");

    $(".report-widget-internal-container").addClass("light-report-widget-nest");
    $(".report-widget-internal-container").removeClass("report-widget-nest");
  }
>>>>>>> 6297c5c5955d7441524e477142d9dbe946e94585

  // change remaining css
  $("body, a").css({ color: "#2A2A2A" });
  $("#dashboard").css({
    background:
      "linear-gradient(29.82deg, #EEEEEE -3.61%, rgba(238, 238, 238, 0.5) 103.96%)",
  });
  $(".dark").css({ background: "white" });

  // ensure power consump widget stays white
  $(".power-consumption-widget").css({ color: "white" });
}

function setDarkMode() {
  localStorage.setItem("dark_mode_on", "1");

  // set icons to the correct color
  // $("#dark-mode-icon").attr("src", "../static/images/LightMode.svg");
  // $(".printer-icon").attr("src", "../static/images/Printer.svg");
  // $(".caret-down-icon").attr("src", "../static/images/CaretDown.svg");
  // $(".plus-icon").attr("src", "../static/images/Plus.svg");
  // $(".lab-summary-options").attr("src", "../static/images/GearSix.svg");

  $(".dark-icon").addClass("invisible-icon");
  $(".light-icon").removeClass("invisible-icon");

  if (localStorage.getItem("menu_open") === "1")
    $(".hamburger-icon").addClass("invisible-icon")
  else $(".x-icon").addClass("invisible-icon")

<<<<<<< HEAD
  if (localStorage.getItem("money_mode_on") === "1") {
    $(".money-mode-icon").addClass("invisible-icon")
    $(".green-icon").removeClass("invisible-icon")
  }
  else $(".green-icon").addClass("invisible-icon")

  $(".report-widget-internal-container").addClass("report-widget-nest");
  $(".report-widget-internal-container").removeClass("light-report-widget-nest");
=======
  if (localStorage.getItem("money_mode_on") === "1")
    $("#money-mode-icon").attr("src", "../static/images/MoneyMode_green.svg");
  else {
    $("#money-mode-icon").attr("src", "../static/images/MoneyMode.svg");

    $(".report-widget-internal-container").addClass("report-widget-nest");
    $(".report-widget-internal-container").removeClass(
      "light-report-widget-nest"
    );
  }
>>>>>>> 6297c5c5955d7441524e477142d9dbe946e94585

  // change remaining css
  $("body, a").css({ color: "white" });
  $("#dashboard").css({
    background:
      "linear-gradient(32.82deg, #2a2a2a -7.28%, rgba(42, 42, 42, 0.75) 107.76%)",
  });
  $(".dark").css({ background: "#2a2a2a" });
}

function toggleDarkMode() {
  // LightMode icon shows in dark mode, and vice versa
  let dark_mode_on = localStorage.getItem("dark_mode_on") ?? "1";
  if (dark_mode_on === "0") setDarkMode();
  else setLightMode();

  // If a barchart is located on the page, it will update the colors
  try {
    buildAllCharts();
  } catch {}
  try {
    buildAllReportCharts();
  } catch {}
}

function setMenuClosed() {
  localStorage.setItem("menu_open", "0");
  $(".menu-hidden").hide();
  $(".menu-visible").show();
  // if dark mode is on, display white svg. else display gray one
  if (localStorage.getItem("dark_mode_on") === "0") {
    $(".dark-icon").removeClass("invisible-icon");
    $(".x-icon").addClass("invisible-icon");
    $(".light-icon").addClass("invisible-icon");
  } else {
    $(".light-icon").removeClass("invisible-icon");
    $(".x-icon").addClass("invisible-icon");
    $(".dark-icon").addClass("invisible-icon");
  }

  if (localStorage.getItem("money_mode_on") === "1") {
    $(".dark-money-icon").addClass("invisible-icon");
    $(".light-money-icon").addClass("invisible-icon");
  }
}

function setMenuOpen() {
  localStorage.setItem("menu_open", "1");
  $(".menu-hidden").show();
  $(".menu-visible").hide();
  // if dark mode is on, display white svg. else display gray one
  if (localStorage.getItem("dark_mode_on") === "0") {
    $(".dark-icon").removeClass("invisible-icon");
    $(".hamburger-icon").addClass("invisible-icon");
    $(".light-icon").addClass("invisible-icon");
  } else {
    $(".light-icon").removeClass("invisible-icon");
    $(".hamburger-icon").addClass("invisible-icon");
    $(".dark-icon").addClass("invisible-icon");
  }

  if (localStorage.getItem("money_mode_on") === "1") {
    $(".dark-money-icon").addClass("invisible-icon");
    $(".light-money-icon").addClass("invisible-icon");
  }
}

function toggleMenu() {
  let menu_open = localStorage.getItem("menu_open") ?? "0";
  menu_open === "0" ? setMenuOpen() : setMenuClosed();
}

function setMoneyMode() {
  localStorage.setItem("money_mode_on", "1");

  // set icons to the correct color
  $(".money-mode-icon").addClass("invisible-icon");
  $(".green-icon").removeClass("invisible-icon");
}

function setNonMoneyMode() {
  localStorage.setItem("money_mode_on", "0");
  // set icons to the correct color
  $(".green-icon").addClass("invisible-icon");
  if (localStorage.getItem("dark_mode_on") === "0")
<<<<<<< HEAD
    $(".dark-money-icon").removeClass("invisible-icon");
  else
    $(".light-money-icon").removeClass("invisible-icon");
=======
    $(".money-mode-icon").attr("src", "../static/images/MoneyMode_dark.svg");
  else $(".money-mode-icon").attr("src", "../static/images/MoneyMode.svg");
>>>>>>> 6297c5c5955d7441524e477142d9dbe946e94585
}

function toggleMoneyMode() {
  // LightMode icon shows in dark mode, and vice versa
  let money_mode_on = localStorage.getItem("money_mode_on") ?? "0";
  if (money_mode_on === "0") setMoneyMode();
  else setNonMoneyMode();

  // If a barchart is located on the page, it will update the colors
  try {
    buildAllCharts();
  } catch {}
  try {
    buildAllReportCharts();
  } catch {}
}

function setup() {
  $(".dark-mode-icon").on("click", toggleDarkMode);
  $(".hamburger-icon").on("click", toggleMenu);
  $(".x-icon").on("click", toggleMenu);
  $(".money-mode-icon").on("click", toggleMoneyMode);
  console.log("setup");

  // reset dark mode status, default to dark mode
  if (localStorage.getItem("dark_mode_on") === "0") setLightMode();
  // reset money mode status, default to off
  if (localStorage.getItem("money_mode_on") === "1") setMoneyMode();
  // reset menu open status, default to closed
  // if (localStorage.getItem('menu_open') === '1') setMenuOpen();
  // reset menu to closed
  setMenuClosed();

  // reloads page if navigated to from the "back" button
  // important for persisting menu_open and dark_mode_on
  window.addEventListener("pageshow", function (event) {
    let historyTraversal =
      event.persisted ||
      (typeof window.performance != "undefined" &&
        window.performance.navigation.type === 2);
    if (historyTraversal) window.location.reload();
  });
}

$("document").ready(setup);

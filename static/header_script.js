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
    $("#hamburger-icon").attr("src", "../static/images/X_dark.svg");
  else $("#hamburger-icon").attr("src", "../static/images/List_dark.svg");

  if (localStorage.getItem("money_mode_on") === "1")
    $("#money-mode-icon").attr("src", "../static/images/MoneyMode_green.svg");
  else { $("#money-mode-icon").attr("src", "../static/images/MoneyMode_dark.svg");

  $(".report-widget-internal-container").addClass("light-report-widget-nest");
  $(".report-widget-internal-container").removeClass("report-widget-nest");
}

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
    $("#hamburger-icon").attr("src", "../static/images/X.svg");
  else $("#hamburger-icon").attr("src", "../static/images/List.svg");

  if (localStorage.getItem("money_mode_on") === "1")
    $("#money-mode-icon").attr("src", "../static/images/MoneyMode_green.svg")
  else  { $("#money-mode-icon").attr("src", "../static/images/MoneyMode.svg")

  $(".report-widget-internal-container").addClass("report-widget-nest");
  $(".report-widget-internal-container").removeClass("light-report-widget-nest");
}


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
}

function setMenuClosed() {
  localStorage.setItem("menu_open", "0");
  $(".menu-hidden").hide();
  $(".menu-visible").show();
  // if dark mode is on, display white svg. else display gray one
  if (localStorage.getItem("dark_mode_on") === "0")
    $("#hamburger-icon").attr("src", "../static/images/List_dark.svg");
  else $("#hamburger-icon").attr("src", "../static/images/List.svg");
}

function setMenuOpen() {
  localStorage.setItem("menu_open", "1");
  $(".menu-hidden").show();
  $(".menu-visible").hide();
  // if dark mode is on, display white svg. else display gray one
  if (localStorage.getItem("dark_mode_on") === "0")
    $("#hamburger-icon").attr("src", "../static/images/X_dark.svg");
  else $("#hamburger-icon").attr("src", "../static/images/X.svg");
}

function toggleMenu() {
  let menu_open = localStorage.getItem("menu_open") ?? "0";
  menu_open === "0" ? setMenuOpen() : setMenuClosed();
}

function setMoneyMode() {
  localStorage.setItem("money_mode_on", "1");

  // set icons to the correct color
  $(".money-mode-icon").attr("src", "../static/images/MoneyMode_green.svg");
}

function setNonMoneyMode() {
  localStorage.setItem("money_mode_on", "0");
  // set icons to the correct color
  if (localStorage.getItem("dark_mode_on") === "0")
    $(".money-mode-icon").attr("src", "../static/images/MoneyMode_dark.svg");
  else
    $(".money-mode-icon").attr("src", "../static/images/MoneyMode.svg");
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
}

function setup() {
  $(".dark-mode-icon").on("click", toggleDarkMode);
  $(".hamburger-icon").on("click", toggleMenu);
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

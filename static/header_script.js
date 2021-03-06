"use strict";

function setLightMode() {
  localStorage.setItem("dark_mode_on", "0");

  $(".light-icon").addClass("invisible-icon");
  $(".dark-icon").removeClass("invisible-icon");

  if (localStorage.getItem("menu_open") === "1")
    $(".hamburger-icon").addClass("invisible-icon");
  else $(".x-icon").addClass("invisible-icon");

  if (localStorage.getItem("money_mode_on") === "1") {
    $(".money-mode-icon").addClass("invisible-icon");
    $(".green-icon").removeClass("invisible-icon");
  } else $(".green-icon").addClass("invisible-icon");

  $(".report-widget-internal-container").addClass("light-report-widget-nest");
  $(".report-widget-internal-container").removeClass("report-widget-nest");

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

  $(".dark-icon").addClass("invisible-icon");
  $(".light-icon").removeClass("invisible-icon");

  if (localStorage.getItem("menu_open") === "1")
    $(".hamburger-icon").addClass("invisible-icon");
  else $(".x-icon").addClass("invisible-icon");

  if (localStorage.getItem("money_mode_on") === "1") {
    $(".money-mode-icon").addClass("invisible-icon");
    $(".green-icon").removeClass("invisible-icon");
  } else $(".green-icon").addClass("invisible-icon");

  $(".report-widget-internal-container").addClass("report-widget-nest");
  $(".report-widget-internal-container").removeClass(
    "light-report-widget-nest"
  );

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
    lab_graph_setup();
    // let cached_rt_data = JSON.parse(localStorage.getItem("real_time_data"));
    // for (const [key, value] of Object.entries(cached_rt_data)) {
    //   if (key == "fumehoods") {
    //     for (let i = 0; i < value.length; i++) {
    //       let id = value[i]["id"];
    //       id = "fumehood" + i;
    //       for (const [fkey, fvalue] of Object.entries(value[i])) {
    //         if (fkey.endsWith("-chart-data")) {
    //           try {
    //             buildAllCharts(fvalue, "#" + id + "-chart");
    //           } catch {}
    //         }
    //       }
    //     }
    //   }
    //   if (key.endsWith("-chart-data")) {
    //     let end = key.indexOf("-chart-data");
    //     try {
    //       buildAllCharts(value, "#" + key.substring(0, end) + "-chart");
    //     } catch {}
    //     continue;
    //   }
    // }
    // buildAllCharts();
  } catch {}
  try {
    // buildAllReportCharts();
    get_report_data();
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
    $(".dark-money-icon").removeClass("invisible-icon");
  else $(".light-money-icon").removeClass("invisible-icon");
}

function toggleMoneyMode() {
  // LightMode icon shows in dark mode, and vice versa
  let money_mode_on = localStorage.getItem("money_mode_on") ?? "0";
  if (money_mode_on === "0") setMoneyMode();
  else setNonMoneyMode();

  const labs = ['rabinowitz_icahn_201', 'rabinowitz_icahn_202'];
  labs.forEach((lab) => {
    let cached_rt_data = localStorage.getItem(lab + "_real_time_data");
    if (cached_rt_data != null) handle_rt_resp(JSON.parse(cached_rt_data));
  });

  // If a barchart is located on the page, it will update the colors
  if (window.location.pathname != '/report') {
  try {
    lab_graph_setup();
  } catch {}
  try {
    // buildAllReportCharts();
    get_report_data();
  } catch {}
}
}

function setup() {
  $(".dark-mode-icon").on("click", toggleDarkMode);
  $(".hamburger-icon").on("click", toggleMenu);
  $(".x-icon").on("click", toggleMenu);
  $(".money-mode-icon").on("click", toggleMoneyMode);
  $(".rotate").click(function () {
    $(this).toggleClass("down");
  });

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

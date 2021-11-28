"use strict";

function setLightMode() {
  localStorage.setItem("dark_mode_on", "0");

  // set icons to the correct color
  $("#dark-mode-icon").attr("src", "../static/images/DarkMode.svg");
  $(".lab-summary-options").attr(
    "src",
    "../static/images/GearSix_dark.svg"
  );

  if (localStorage.getItem("menu_open") === "1")
    $("#hamburger-icon").attr("src", "../static/images/X_dark.svg");
  else $("#hamburger-icon").attr("src", "../static/images/List_dark.svg");

  if (localStorage.getItem("money_mode_on") === "1")
    $("#money-mode-icon").attr("src", "../static/images/MoneyMode_green.svg")
  else ("#money-mode-icon").attr("src", "../static/images/MoneyMode_dark.svg")

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
  $("#dark-mode-icon").attr("src", "../static/images/LightMode.svg");
  $(".lab-summary-options").attr("src", "../static/images/GearSix.svg");
  if (localStorage.getItem("menu_open") === "1")
    $("#hamburger-icon").attr("src", "../static/images/X.svg");
  else $("#hamburger-icon").attr("src", "../static/images/List.svg");

  if (localStorage.getItem("money_mode_on") === "1")
    $("#money-mode-icon").attr("src", "../static/images/MoneyMode_green.svg")
  else  { $("#money-mode-icon").attr("src", "../static/images/MoneyMode.svg")
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
  $("#money-mode-icon").attr("src", "../static/images/MoneyMode_green.svg");
}

function setNonMoneyMode() {
  localStorage.setItem("money_mode_on", "0");
  // set icons to the correct color
  if (localStorage.getItem("dark_mode_on") === "0")
    $("#money-mode-icon").attr("src", "../static/images/MoneyMode_dark.svg");
  else
    $("#money-mode-icon").attr("src", "../static/images/MoneyMode.svg");
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

// get time and date data
function get_date() {
  let dt = new Date();
  let datePart = dt.toLocaleDateString().replaceAll("/", ".");
  datePart =
    datePart.slice(0, datePart.lastIndexOf(".") + 1) +
    datePart.slice(datePart.lastIndexOf(".") + 3);

  $(".consumption-date").text(datePart);
}

let request = null;

function handle_rerender(response) {
  console.log("rerender");
  $("#dashboard").html(response);
  $(".activate_rabinowitz_icahn_201").on("click", lab_summary);
}

function lab_summary() {
  let url = "/lab_summary?lab_name=rabinowitz_icahn_201";
  if (request != null) request.abort();

  request = $.ajax({
    type: "GET",
    url: url,
    success: handle_rerender,
  });
}

// --------------------------------------------------------
// Real time data fetching code
// --------------------------------------------------------

// Change to url params in the future
const labNames = ["rabinowitz_icahn_201"];
const fumehoodId = "fumehood0";

// get fumehood # from url params
// const queryString = window.location.search;
// const urlParams = new URLSearchParams(queryString);
// const fumehoodId = urlParams.get('fumehood_id')

// try to cram data into the corresponding tag with id
function handle_rt_resp(response) {
  for (const [key, value] of Object.entries(response)) {
    // color fumehood open status the correct color
    if (key.endsWith("-mini-status")) {
      let closed = value == "CLOSED";
      $("#" + key)
        .children("span")
        .text(value);
      $("#" + key)
        .children("span")
        .addClass(closed ? "green" : "red");
      $("#" + key)
        .children("span")
        .removeClass(closed ? "red" : "green");
      $("#" + key)
        .children("img")
        .attr(
          "src",
          closed
            ? "../static/images/GreenDot.svg"
            : "../static/images/RedDot.svg"
        );
      continue;
    }
    if (key.endsWith("-status")) {
      $("#" + key).addClass(value == "OPEN" ? "red" : "green");
      $("#" + key).removeClass(value == "OPEN" ? "green" : "red");
    }
    if (key.endsWith("-chart-data")) {
      let end = key.indexOf("-chart-data");
      try {
        buildAllCharts(value, "#" + key.substring(0, end) + "-chart");
      } catch {
        continue;
      }
    }
    if (key.endsWith("-number")) {
      let numOpen = 0;
      for (const key of Object.keys(value)) {
        if (value[key] == "OPEN") {
          numOpen++;
        }
      }
      $("#" + key).text(numOpen + " of " + Object.keys(value).length);
      continue;
    }
    if (key == "fumehoods") {
      for (let i = 0; i < value.length; i++) {
        let id = value[i]["id"];
        id = "fumehood" + i;
        for (const [fkey, fvalue] of Object.entries(value[i])) {
          $("#" + id + "-" + fkey).text(fvalue);
          if (fkey.endsWith("-chart-data")) {
            let end = fkey.indexOf("-chart-data");
            try {
              buildAllCharts(fvalue, "#" + id + "-chart");
            } catch {
              continue;
            }
          }
        }
      }
    }

    // shunt in the correct value into the html
    $("#" + key).text(value);
  }
}

// retrieve real time data
function get_rt_data() {
  labNames.forEach((labName) => {
    let url = "/real_time_data?lab_name=" + labName;
    url += "&fumehood_id=" + fumehoodId;
    request = $.ajax({
      type: "GET",
      url: url,
      success: handle_rt_resp,
    });
  });
}

function setup() {
  // reset dark mode status, default to dark mode
  if (localStorage.getItem("dark_mode_on") === "0") setLightMode();
  // reset money mode status, default to off
  if (localStorage.getItem("money_mode_on") === "1") setMoneyMode();
  // reset menu to closed
  setMenuClosed();

  $("#dark-mode-icon").on("click", toggleDarkMode);
  $("#hamburger-icon").on("click", toggleMenu);
  $("#money-mode-icon").on("click", toggleMoneyMode);

  get_rt_data();
  window.setInterval(get_rt_data, 1000);
  get_date();
  window.setInterval(get_date(), 3600000);

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
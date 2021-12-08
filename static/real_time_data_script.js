"use strict";

let request = null;

// --------------------------------------------------------
// Based on the value, decide whether to color it red or green
// --------------------------------------------------------
function lab_summary() {
  let url = "/lab_summary?lab_id=rabinowitz_icahn_201";
  if (request != null) request.abort();
}

const RED_GREEN_THRESH = {
  "-today-kwh": 550,
  "-nrg-trend": 0,
  "-current-kw": 30,
  "-number": 2,
  "-ave-nrg": 19,
  "-kwh": 10,
  "-today": 3,
  "-today": 4,
  "-avg-day": 4,
};

function extract_floats_from_string(str) {
  let regex = /[+-]?\d+(\.\d+)?/g;
  let floats = str.match(regex).map(function (v) {
    return parseFloat(v);
  });
  return floats;
}

function remove_parent_color(object) {
  object.removeClass(["red", "green", "red-grad", "green-grad"]);
}

function handle_red_green(key, value) {
  let floats;
  try {
    floats = extract_floats_from_string(value);
  } catch {}

  // ----- today-wkh -----
  if (key.endsWith("-today-kwh")) {
    remove_parent_color($("#" + key).parent());
    if (parseFloat(floats[0]) > RED_GREEN_THRESH["-today-kwh"]) {
      $("#" + key)
        .parent()
        .addClass("red");
    } else {
      $("#" + key)
        .parent()
        .addClass("green");
    }

    // ----- nrg-trend -----
  } else if (key.endsWith("-nrg-trend")) {
    if ($("#" + key).hasClass("lab-summary-inner-nrg-trend")) {
      remove_parent_color($("#" + key));
      remove_parent_color($("#" + key).siblings());
      if (parseFloat(floats[0]) > RED_GREEN_THRESH["-nrg-trend"]) {
        $("#" + key).addClass("red");
        $("#" + key)
          .siblings()
          .addClass("red");
      } else {
        $("#" + key).addClass("green");
        $("#" + key)
          .siblings()
          .addClass("green");
      }
    } else {
      remove_parent_color(
        $("#" + key)
          .parent()
          .parent()
      );
      if (parseFloat(floats[0]) > RED_GREEN_THRESH["-nrg-trend"]) {
        $("#" + key)
          .parent()
          .parent()
          .addClass("red-grad");
      } else {
        $("#" + key)
          .parent()
          .parent()
          .addClass("green-grad");
      }
    }

    // ----- current-kw ------
  } else if (key.endsWith("-current-kw")) {
    if ($("#" + key).hasClass("lab-summary-current-kw")) {
      remove_parent_color($("#" + key));
      remove_parent_color($("#" + key).siblings());
      if (parseFloat(floats[0]) > RED_GREEN_THRESH["-current-kw"]) {
        $("#" + key).addClass("red");
        $("#" + key)
          .siblings()
          .addClass("red");
        return;
      } else {
        $("#" + key).addClass("green");
        $("#" + key)
          .siblings()
          .addClass("green");
      }
    } else {
      remove_parent_color(
        $("#" + key)
          .parent()
          .parent()
      );
      if (parseFloat(floats[0]) > RED_GREEN_THRESH["-current-kw"]) {
        $("#" + key)
          .parent()
          .parent()
          .addClass("red-grad");
      } else {
        $("#" + key)
          .parent()
          .parent()
          .addClass("green-grad");
      }
    }

    // ----- number -----
  } else if (key.endsWith("-number")) {
    let num = 0;
    for (let i = 0; i < Object.values(value).length; i++) {
      if (Object.values(value)[i] == "OPEN") {
        num++;
      }
    }
    remove_parent_color($("#" + key).parent());
    remove_parent_color(
      $("#" + key)
        .parent()
        .siblings()
    );
    if (num <= RED_GREEN_THRESH["-number"]) {
      $("#" + key)
        .parent()
        .addClass("green");
    } else {
      $("#" + key)
        .parent()
        .addClass("red");
    }

    // ----- ave-nrg -----
  } else if (key.endsWith("-ave-nrg")) {
    if (!$("#" + key).hasClass("widget-medium")) {
      return;
    }
    remove_parent_color($("#" + key));
    remove_parent_color($("#" + key).siblings());
    if (floats[0] > RED_GREEN_THRESH["-ave-nrg"]) {
      $("#" + key).addClass("red");
      $("#" + key)
        .siblings()
        .addClass("red");
    } else {
      $("#" + key).addClass("green");
      $("#" + key)
        .siblings()
        .addClass("green");
    }
    // ----- kwh -----
  } else if (key.endsWith("-kwh")) {
    remove_parent_color($("#" + key).parent());
    if (value > RED_GREEN_THRESH["-kwh"]) {
      $("#" + key)
        .parent()
        .addClass("red");
    } else {
      $("#" + key)
        .parent()
        .addClass("green");
    }
    // ----- today -----
  } else if (key.endsWith("-today")) {
    remove_parent_color($("#" + key).parent());
    if (value > RED_GREEN_THRESH["-today"]) {
      $("#" + key)
        .parent()
        .addClass("red");
    } else {
      $("#" + key)
        .parent()
        .addClass("green");
    }
    // ----- today -----
  } else if (key.endsWith("-avg-day")) {
    remove_parent_color($("#" + key).parent());
    if (value > RED_GREEN_THRESH["-avg-day"]) {
      $("#" + key)
        .parent()
        .addClass("red");
    } else {
      $("#" + key)
        .parent()
        .addClass("green");
    }
  }
}

// --------------------------------------------------------
// Real time data fetching code
// --------------------------------------------------------

// Change to url params in the future
// const labNames = ["rabinowitz_icahn_201", "rabinowitz_icahn_202"];
const labNames = ["rabinowitz_icahn_201"];
const fumehoodId = "fumehood0";

// get fumehood # from url params
// const queryString = window.location.search;
// const urlParams = new URLSearchParams(queryString);
// const fumehoodId = urlParams.get('fumehood_id')

// try to cram data into the corresponding tag with id
function handle_rt_resp(response) {
  localStorage.setItem("real_time_data", JSON.stringify(response));
  for (const [key, value] of Object.entries(response)) {
    handle_red_green(key, value);
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
      } catch {}
      continue;
    }
    if (key.endsWith("-number")) {
      let numOpen = 0;
      let i = 0;
      for (const vkey of Object.keys(value)) {
        $("#fumehood" + i + "-mini-status").removeClass("red");
        $("#fumehood" + i + "-mini-status").removeClass("green");
        let html;
        if (value[vkey] == "OPEN") {
          html =
            "<p style='font-weight: bold'>" +
            value[vkey] +
            "</p><img src='../static/images/RedDot.svg'></img>";
          $("#fumehood" + i + "-mini-status").addClass("red");
        } else {
          html =
            "<p style='font-weight: bold'>" +
            value[vkey] +
            "</p><img src='../static/images/GreenDot.svg'></img>";
          $("#fumehood" + i + "-mini-status").addClass("green");
        }
        $("#fumehood" + i + "-mini-status").html(html);
        i += 1;
        if (value[vkey] == "OPEN") {
          numOpen++;
        }
      }
      $("#" + key).text(numOpen + " of " + Object.keys(value).length);
      continue;
    }
    if (key == "fumehoods") {
      let fIdx = 0;
      Object.entries(value).forEach((arr) => {
        let fkey = arr[0];
        let fvalue = arr[1];
        let id = "fumehood" + fIdx;

        $("#" + id + "-name").text("Fumehood " + fkey.slice(-2));

        if (localStorage.getItem("money_mode_on") === "1") {
          let money_value = convert_to_money(fvalue[1]);
          $("#" + id + "-kw").text(money_value + " kW");
        } else {
          console.log(fvalue);
          $("#" + id + "-kw").text(fvalue.toFixed(2) + " kW");
        }
        fIdx++;
        $("#" + id + "-kwh").text(3 + " kWh");
        $("#" + id + "-today").text(4 + " Hrs");
        $("#" + id + "-avg-day").text(5 + " Hrs");
      });
    }
    // if kW or kWh, convert to money mode
    if (
      localStorage.getItem("money_mode_on") === "1" &&
      typeof value === "string"
    ) {
      if (value.endsWith("kW") || value.endsWith("kWh")) {
        let money_value = convert_to_money(value);
        $("#" + key).text(money_value);
        continue;
      }
    }
    // shunt in the correct value into the html
    $("#" + key).text(value);
  }
}

function convert_to_money(value) {
  let dollar_equiv = 2.25 * parseFloat(value.replace(/[^\d.-]/g, ""));
  // round to 2 decimal places
  dollar_equiv = dollar_equiv.toFixed(2);
  return "$" + dollar_equiv;
}

// retrieve real time data
function get_rt_data() {
  labNames.forEach((labName) => {
    let url = "/real_time_data?lab_id=" + labName;
    url += "&fumehood_id=" + fumehoodId;
    request = $.ajax({
      type: "GET",
      url: url,
      success: handle_rt_resp,
    });
  });
}

function get_date() {
  let dt = new Date();
  let datePart = dt.toLocaleDateString().replaceAll("/", ".");
  datePart =
    datePart.slice(0, datePart.lastIndexOf(".") + 1) +
    datePart.slice(datePart.lastIndexOf(".") + 3);

  $(".consumption-date").text(datePart);
}

// set up document
function setup() {
  let cached_rt_data = localStorage.getItem("real_time_data");
  if (cached_rt_data != null) handle_rt_resp(JSON.parse(cached_rt_data));

  get_rt_data();
  window.setInterval(get_rt_data, 5 * 1000);
  get_date();
  window.setInterval(get_date, 3600 * 1000);
}

$("document").ready(setup);

"use strict";

let request = null;

function lab_summary() {
    let url = "/lab_summary?lab_name=rabinowitz_icahn_201";
    if (request != null) request.abort();

    request = $.ajax({
      type: "GET",
      url: url,
      success: handle_rerender,
    });
  }

function handle_rerender(response) {
  console.log("rerender");
  $("#dashboard").html(response);
  $(".activate_rabinowitz_icahn_201").on("click", lab_summary);
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
  get_rt_data();
  window.setInterval(get_rt_data, 1000);
  get_date();
  window.setInterval(getDate(), 3600000);
}

$("document").ready(setup);
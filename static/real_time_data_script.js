"use strict";

let request = null;

function lab_summary() {
  let url = "/emapp/lab_summary?lab_name=rabinowitz_icahn_201";
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
  console.log(response);
  localStorage.setItem("real_time_data", JSON.stringify(response));
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
      for (let i = 0; i < value.length; i++) {
        let id = value[i]["id"];
        $("#fumehood" + i + "-name").text("Fumehood " + id.slice(-2));
        id = "fumehood" + i;
        for (const [fkey, fvalue] of Object.entries(value[i])) {
          if (fkey == "id") {
            $("#" + id + "-mini-status")
              .siblings(".mini-fume-name")
              .text("Fumehood " + fvalue.substring(2));
            continue;
          }
          $("#" + id + "-" + fkey).text(fvalue);
          if (fkey.endsWith("-chart-data")) {
            try {
              buildAllCharts(fvalue, "#" + id + "-chart");
            } catch {}
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
  let cached_rt_data = localStorage.getItem("real_time_data");
  // console.log(cached_rt_data);
  if (cached_rt_data != null) handle_rt_resp(cached_rt_data);

  // get_rt_data();
  // window.setInterval(get_rt_data, 5000);
  get_date();
  window.setInterval(get_date, 3600000);
}

$("document").ready(setup);

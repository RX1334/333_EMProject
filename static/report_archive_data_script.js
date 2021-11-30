// "use strict";

// let request = null;


// // --------------------------------------------------------
// // Real time data fetching code
// // --------------------------------------------------------

// // Change to url params in the future
// const labNames = ["rabinowitz_icahn_201"];
// const fumehoodId = "fumehood0";

// // get fumehood # from url params
// // const queryString = window.location.search;
// // const urlParams = new URLSearchParams(queryString);
// // const fumehoodId = urlParams.get('fumehood_id')

// // try to cram data into the corresponding tag with id
// function handle_report_archive_resp(response) {
//     console.log(response);
// //   for (const [key, value] of Object.entries(response)) {
// //     // color fumehood open status the correct color
// //     if (key.endsWith("-mini-status")) {
// //       let closed = value == "CLOSED";
// //       $("#" + key)
// //         .children("span")
// //         .text(value);
// //       $("#" + key)
// //         .children("span")
// //         .addClass(closed ? "green" : "red");
// //       $("#" + key)
// //         .children("span")
// //         .removeClass(closed ? "red" : "green");
// //       $("#" + key)
// //         .children("img")
// //         .attr(
// //           "src",
// //           closed
// //             ? "../static/images/GreenDot.svg"
// //             : "../static/images/RedDot.svg"
// //         );
// //       continue;
// //     }
// //     if (key.endsWith("-status")) {
// //       $("#" + key).addClass(value == "OPEN" ? "red" : "green");
// //       $("#" + key).removeClass(value == "OPEN" ? "green" : "red");
// //     }
// //     if (key.endsWith("-chart-data")) {
// //       let end = key.indexOf("-chart-data");
// //       try {
// //         buildAllCharts(value, "#" + key.substring(0, end) + "-chart");
// //       } catch {
// //         continue;
// //       }
// //     }
// //     if (key.endsWith("-number")) {
// //       let numOpen = 0;
// //       for (const key of Object.keys(value)) {
// //         if (value[key] == "OPEN") {
// //           numOpen++;
// //         }
// //       }
// //       $("#" + key).text(numOpen + " of " + Object.keys(value).length);
// //       continue;
// //     }
// //     if (key == "fumehoods") {
// //       for (let i = 0; i < value.length; i++) {
// //         let id = value[i]["id"];
// //         id = "fumehood" + i;
// //         for (const [fkey, fvalue] of Object.entries(value[i])) {
// //           $("#" + id + "-" + fkey).text(fvalue);
// //           if (fkey.endsWith("-chart-data")) {
// //             let end = fkey.indexOf("-chart-data");
// //             try {
// //               buildAllCharts(fvalue, "#" + id + "-chart");
// //             } catch {
// //               continue;
// //             }
// //           }
// //         }
// //       }
// //     }

// //     // shunt in the correct value into the html
// //     $("#" + key).text(value);
// //   }
// }

// // retrieve real time data
// function get_report_archive_data() {
//     let url = "/report_archive_data";
//     request = $.ajax({
//       type: "GET",
//       url: url,
//       success: handle_report_archive_resp,
//     });
// }

// // set up document
// function setup() {
//   get_report_archive_data();
// }

// $("document").ready(setup);
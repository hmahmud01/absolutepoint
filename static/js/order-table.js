
"use strict";

document.addEventListener("DOMContentLoaded", function () {
    const cryptoDatatable = new simpleDatatables.DataTable("#cryptoDatatable", {
        columns: [
            // Disable sorting on the first column
            // { select: [0], sortable: false },
        ],
    });

    const stripeDatatable = new simpleDatatables.DataTable("#stripeDatatable", {
        columns: [
            // Disable sorting on the first column
            // { select: [0], sortable: false },
        ],
    });



    cryptoDatatable.on("datatable.init", function () {});
    stripeDatatable.on("datatable.init", function () {});


    cryptoDatatable.on("datatable.init", function (args) {
        document.getElementById("cryptoDatatable").closest(".preload-wrapper").classList.add("opacity-10");
    });

    stripeDatatable.on("datatable.init", function (args) {
        document.getElementById("stripeDatatable").closest(".preload-wrapper").classList.add("opacity-10");
    });
});

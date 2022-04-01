
"use strict";

document.addEventListener("DOMContentLoaded", function () {
    const dueTable = new simpleDatatables.DataTable("#dueTable", {
        columns: [],
    });

    const failedTable = new simpleDatatables.DataTable("#failedTable", {
        columns: [],
    });

    const fraudTable = new simpleDatatables.DataTable("#fraudTable", {
        columns: [],
    });

    const doneTable = new simpleDatatables.DataTable("#doneTable", {
        columns: [],
    });

    dueTable.on("datatable.init", function () {});

    dueTable.on("datatable.init", function (args) {
        document.getElementById("ordersDatatable").closest(".preload-wrapper").classList.add("opacity-10");
    });

    failedTable.on("datatable.init", function () {});

    failedTable.on("datatable.init", function (args) {
        document.getElementById("ordersDatatable").closest(".preload-wrapper").classList.add("opacity-10");
    });

    fraudTable.on("datatable.init", function () {});

    fraudTable.on("datatable.init", function (args) {
        document.getElementById("ordersDatatable").closest(".preload-wrapper").classList.add("opacity-10");
    });

    doneTable.on("datatable.init", function () {});

    doneTable.on("datatable.init", function (args) {
        document.getElementById("ordersDatatable").closest(".preload-wrapper").classList.add("opacity-10");
    });
});

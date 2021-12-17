$("#settings-button").click(function () {
    $("#settings-button").fadeOut(150);
    $("#main").fadeOut(150).promise().done(function () {
        $("#settings").fadeIn(150);
        $("#home-button").fadeIn(150);
    });
});

$("#home-button").click(function () {
    $("#home-button").fadeOut(150);
    $("#settings").fadeOut(150).promise().done(function () {
        $("#main").fadeIn(150);
        $("#settings-button").fadeIn(150);
    });
});

function networkError() {
    alertBox("Erreur réseau", "Impossible de se connecter...", `
        <button class="btn btn-sp primary btn-align-right ripple-effect"
        onclick="document.location.reload();">Fermer</button>`);
}

var source = new EventSource("/listen");

$(document).ready(function () {
    loader(true);

    $.ajax({
        type: "POST",
        url: "/api/status",

        success: function () {
            loader(false);
        },

        error: function () {
            loader(false);
            networkError();
        },

        timeout: 3000
    });
});

source.onmessage = function (msg) {

    console.log(msg.data);

    gondolaStatus = msg.data.split(":")[1].split(",")[0];
    speed = parseInt(msg.data.split(":")[2]);

    console.log(gondolaStatus);
    console.log(speed);

    if (gondolaStatus == "enabled") {
        $("#gondola-toggle input").prop("checked", true);
    } else if (gondolaStatus == "disabled") {
        $("#gondola-toggle input").prop("checked", false);
    }

    displaySpeed("#speed-progress", speed);
}

source.onerror = function () {
    networkError();
}

$("#gondola-toggle input").change(function () {
    if (this.checked) {
        console.log("gg");
        changeState(true);
    }
    else {
        changeState(false);
    }
});

$("#slower-button").click(function () {
    slower();
});

$("#speed-selector .dropdown-content .btn").click(function () {
    var requestedSpeed = parseInt($(this).data("value"));
    setSpeed(requestedSpeed);
});

$("#faster-button").click(function () {
    faster();
});

$("body").keydown(function(e) {
    if (e.which == 37) {
        slower();
    } else if (e.which == 39) {
        faster();
    } else if (e.which == 13 || e.which == 32) {
        if ($("#gondola-toggle input").prop("checked")) {
            changeState(false);
        } else {
            changeState(true);
        }
    } else if (e.which == 49) {
        setSpeed(1);
    } else if (e.which == 50) {
        setSpeed(2);
    } else if (e.which == 51) {
        setSpeed(3);
    } else if (e.which == 52) {
        setSpeed(4);
    } else if (e.which == 53) {
        setSpeed(5);
    } else if (e.which == 54) {
        setSpeed(6);
    } else if (e.which == 55) {
        setSpeed(7);
    } else if (e.which == 56) {
        setSpeed(8);
    } else if (e.which == 57) {
        setSpeed(9);
    } else if (e.which == 48) {
        setSpeed(10);
    }
});

function changeState(wantToEnable) {

    loader(true);

    $.ajax({
        type: "POST",
        url: "/api/enable",
        data: JSON.stringify({ enable: wantToEnable }),
        contentType: "application/json",

        success: function () {
            loader(false);
        },

        error: function () {
            loader(false);
            networkError();
        },

        timeout: 3000
    });
}

function slower() {
    var actualSpeed = parseInt($("#speed-selector .btn-badge").text());
    if (actualSpeed != 1) {
        setSpeed(actualSpeed - 1);
    }
}

function faster() {
    var actualSpeed = parseInt($("#speed-selector .btn-badge").text());
    if (actualSpeed != 10) {
        setSpeed(actualSpeed + 1);
    }
}

function setSpeed(requestedSpeed) {

    loader(true);

    $.ajax({
        type: "POST",
        url: "/api/speed",
        data: JSON.stringify({ speed: requestedSpeed }),
        contentType: "application/json",


        success: function () {
            loader(false);
        },

        error: function () {
            loader(false);
            networkError();
        },

        timeout: 3000
    });
}

function displaySpeed(progress, speed) {
    $("#speed-selector .btn-badge").text(speed);

    $(progress).closest(".progress-bar").removeClass("success");
    $(progress).closest(".progress-bar").removeClass("warning");
    $(progress).closest(".progress-bar").removeClass("danger");

    if (speed < 3) {
        $(progress).closest(".progress-bar").addClass("danger");
    } else if (speed == 10 || speed < 6) {
        $(progress).closest(".progress-bar").addClass("warning");
    } else {
        $(progress).closest(".progress-bar").addClass("success");
    }
    $(progress).css("width", speed * 10 + "%");
}
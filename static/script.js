/////////////////////////////////////////
//////////// TWO SECTIONS ///////////////
/////////////////////////////////////////

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


/////////////////////////////////////////
//////////// ERROR MANAGEMENT ///////////
/////////////////////////////////////////

function networkError() {
    alertBox("Erreur réseau", "Impossible de se connecter...", `
        <button class="btn btn-sp primary btn-align-right ripple-effect"
        onclick="document.location.reload();">Fermer</button>`);
}


/////////////////////////////////////////
//////////// SERVER SENT EVENTS /////////
/////////////////////////////////////////

var source = new EventSource("/listen");

askStatusWhenReady();

function askStatusWhenReady() {
    if (source.readyState) {
        askStatus
    } else {
        setTimeout(askStatus, 200);
    }
}

function askStatus() {

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
}

source.onmessage = function (msg) {

    var gondolaStatus = msg.data.split(":")[1].split(",")[0];
    var speed = parseInt(msg.data.split(":")[2]);
    var lightsStatus = msg.data.split(":")[3];

    if (gondolaStatus == "enabled") {
        $("#gondola-toggle input").prop("checked", true);
    } else {
        $("#gondola-toggle input").prop("checked", false);
    }

    if (lightsStatus == "enabled") {
        $("#lights-toggle input").prop("checked", true);
    } else {
        $("#lights-toggle input").prop("checked", false);
    }

    displaySpeed("#speed-progress", speed);
}

source.onerror = function () {
    networkError();
}


/////////////////////////////////////////
//////////// BUTTONS, TOGGLES ///////////
/////////////////////////////////////////

$("#gondola-toggle input").change(function () {
    if (this.checked) {
        changeState(true);
    }
    else {
        changeState(false);
    }
});

$("#lights-toggle input").change(function () {
    if (this.checked) {
        enableLights(true);
    }
    else {
        enableLights(false);
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


/////////////////////////////////////////
//////////// KEYBOARD SHORTCUTS /////////
/////////////////////////////////////////

$("body").keydown(function (e) {
    if (e.which == 37) {
        slower();
    } else if (e.which == 39) {
        faster();
    } else if (e.which == 13 || e.which == 32) {
        e.preventDefault();
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
    } else if (e.which == 76) {
        if ($("#lights-toggle input").prop("checked")) {
            enableLights(false);
        }
        else {
            enableLights(true);
        }
    }
});


/////////////////////////////////////////
//////////// ENABLE AND DISABLE /////////
/////////////////////////////////////////

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


/////////////////////////////////////////
//////////// LIGHTS /////////////////////
/////////////////////////////////////////

function enableLights(wantToEnable) {

    loader(true);

    $.ajax({
        type: "POST",
        url: "/api/enablelights",
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

/////////////////////////////////////////
//////////// SPEED CONTROL //////////////
/////////////////////////////////////////

function slower() {
    var actualSpeed = parseInt($("#speed-selector .btn-badge").text());
    if (actualSpeed == 1) {
        changeState(false);
    } else {
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


/////////////////////////////////////////
//////////// BACKGROUND IMAGE ///////////
/////////////////////////////////////////

if (localStorage.getItem("bg-img") == "true") {
    $("body").addClass("bg-img");
    $(".settings-item:has(.dark-theme-toggle-switch)").hide();
    enableDarkTheme(true);
    $("#bg-img-toggle input").prop("checked", true);
}

$("#bg-img-toggle input").change(function() {
    if (this.checked) {
        $("body").addClass("bg-img");
        $(".settings-item:has(.dark-theme-toggle-switch)").hide();
        enableDarkTheme(true);
        localStorage.setItem("bg-img", "true");
    } else {
        $("body").removeClass("bg-img");
        $(".settings-item:has(.dark-theme-toggle-switch)").show();
        localStorage.setItem("bg-img", "false");
    }
});

$("#setImg").click(function(e) {

    e.stopPropagation();

    alertBox("Définir l'image d'arrière-plan", "", `
        <div class="modern-input primary">
            <input type="text" id="new-img" placeholder=" " autocomplete="img-url">
            <p>Entrez l'url de l'image</p>
        </div>
        <button class="btn btn-sp primary ripple-effect cancel" onclick="setImg();">Définir</button>
        <button class="btn btn-ol primary btn-align-right ripple-effect cancel">Fermer</button>`);
});

imgUrl = localStorage.getItem("bg-img-url");

if (imgUrl !== null) {
    $("body").css("--img-url", "url(" + imgUrl + ")");
}

function setImg() {
    imgUrl = $("#new-img").val();
    localStorage.setItem("bg-img-url", imgUrl);
    $("body").css("--img-url", "url(" + imgUrl + ")");
}


/////////////////////////////////////////
//////////// CPU TEMP ///////////////////
/////////////////////////////////////////

function showCPUTemp() {

    loader(true);

    $.ajax({
        type: "GET",
        url: "/api/cpuTemp",

        success: function (response) {
            loader(false);
            $("#cpuTemp-indic").text("Température du CPU: " + response);
        },

        error: function () {
            loader(false);
            networkError();
        },

        timeout: 3000
    });
}

showCPUTemp();

$("#cpuTemp").click(askStatusWhenReady);
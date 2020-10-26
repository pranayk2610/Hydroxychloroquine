$(document).ready(function() {
    $("#building1").hide();
    $("#building2").hide();
    $("#building3").hide();
    $("#building4").hide();
    $("#building5").hide();
    $("#addButton2").hide();
    $("#addButton3").hide();
    $("#addButton4").hide();
    $("#addButton5").hide();
    $("#addButton1").click(function() {
        $("#building1").show();
        $("#addButton1").hide();
        $("#addButton2").show();
    });
    $("#addButton2").click(function() {
        $("#building2").show();
        $("#addButton2").hide();
        $("#addButton3").show();
    });
    $("#addButton3").click(function() {
        $("#building3").show();
        $("#addButton3").hide();
        $("#addButton4").show();
    });
    $("#addButton4").click(function() {
        $("#building4").show();
        $("#addButton4").hide();
        $("#addButton5").show();
    });
    $("#addButton5").click(function() {
        $("#building5").show();
        $("#addButton5").hide();
    });
});

$(() => {
    $(".playlist").on("click", function () {
        window.location.href = `/playlist/${$(this).attr("id")}`;
    });
});
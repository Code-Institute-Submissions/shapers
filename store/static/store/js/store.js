$(document).ready(function () {

    $('#sort-selector').change(function () {
        var selector = $(this);
        var currentUrl = new URL(window.location);
        var selection = selector.val();

        if (selection !== "reset") {
            var sort = selection.split("_")[0];
            var direction = selection.split("_")[1];

            currentUrl.searchParams.set("sort", sort);
            currentUrl.searchParams.set("direction", direction);
            window.location.replace(currentUrl);

        } else {
            currentUrl.searchParams.delete("sort");
            currentUrl.searchParams.delete("direction");
            window.location.replace(currentUrl);
        }
    });

    // User to add 1 to 99 products at a time
    $('#increment-qty').click(function () {
        var productQty = $('#product-qty');
        var currentValue = parseInt(productQty.val());
        if (currentValue < 99) {
            productQty.val(currentValue + 1);
        } else {
            $("#increment-qty").attr("title", "Add 99 max").tooltip('show');
        }
    });
    $('#decrement-qty').click(function () {
        var productQty = $('#product-qty');
        var currentValue = parseInt(productQty.val());
        if (currentValue > 1) {
            productQty.val(currentValue - 1);
        } else {
            $("#decrement-qty").attr("title", "Add 1 minimum").tooltip('show');
        }
    });
    $('#decrement-qty, #increment-qty').mouseleave(function () {
        $('.product-form [data-toggle="tooltip"]').tooltip('dispose');
    });


})

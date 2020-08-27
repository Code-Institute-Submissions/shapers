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

    // Product details quantity input buttons
    $('#increment-qty').click(function () {
        var productQty = $('#product-qty');
        var currentValue = parseInt(productQty.val());
        if (currentValue < 99) {
            productQty.val(currentValue + 1);
        } else {

        }
        handleEnableDisable($('#increment-qty'));
    });
    $('#decrement-qty').click(function () {
        var productQty = $('#product-qty');
        var currentValue = parseInt(productQty.val());
        if (currentValue > 1) {
            productQty.val(currentValue - 1);
        }
        handleEnableDisable($('#decrement-qty'));
    });

})

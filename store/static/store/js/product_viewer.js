$(document).ready(function () {

  let modelViewer = $("#model-viewer");
  let active3d = Boolean(modelViewer.length);
  let imageView = $("#image-view");

  function switchImageSrc(image) {
    imageView.attr('src', $(image).attr('src'));
    $("#viewer-image").attr('src', $(image).attr('src'));
  }

  function switchViewerToImage(image) {
    active3d = false;
    switchImageSrc(image);
    modelViewer.fadeOut(200, 'linear',
      imageView.delay(200).fadeIn(200, 'linear'));
  }

  function switchViewerTo3d() {
    active3d = true;
    imageView.fadeOut(200, 'linear',
      modelViewer.delay(200).fadeIn(200, 'linear'));
  }

  $(".product-tbn").click(function () {

    if ($(this).hasClass('product-tbn-3d')) {

      !active3d ? switchViewerTo3d() : {};

    } else {

      active3d ? switchViewerToImage(this) : switchImageSrc(this);

    }
  });

  function resizeViewer() {
    var heroImage = $("#image-view").get(0);
    var picRatio = heroImage.naturalWidth / heroImage.naturalHeight;

    var maxHeight = window.innerHeight - 100 + "px";

    $("#viewer-content").css("maxHeight", maxHeight);

    var contentMaxWidth = parseInt($("#viewer-content").css('maxHeight')) * picRatio;

    $("#viewer-content").css('maxWidth', contentMaxWidth + "px");

  }

  $("#image-view").click(function () {
    resizeViewer();
    $(window).on("resize", resizeViewer);
    $("#product-viewer").css("display", "block");
  });

  $("#viewer-close").click(function () {
    $(window).off("resize");
    $("#product-viewer").css("display", "none");
  });

  window.toggleFullScreen = function () {
    if (!document.fullscreenElement) {
      document.getElementById("viewer-image").requestFullscreen();
    } else if (document.fullscreenElement) {
      document.exitFullscreen();
      $("#product-viewer").css("display", "none");
    }
  };

});
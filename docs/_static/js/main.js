
// the following code applies a function to each <img> on the page that resets
// the source of the image, thereby reloading it, when the image is clicked.
// this is specifically to reload single-play gifs. 
var allImages = document.querySelectorAll("img");

var reloadImage = function() {
    this.src = this.src;
};

for (var i = 0; i < allImages.length; i++) {
    allImages[i].addEventListener('click', reloadImage, false);
}
document.addEventListener("DOMContentLoaded", function () {
    const imagesContainer = document.querySelector(".slider .slider-content");
    
    const images = imagesContainer ? imagesContainer.querySelectorAll("img") : [];

    const prevButton = document.querySelector("#previous");
    const nextButton = document.querySelector("#next");
    let currentIndex = 0;

    function updateSlider(index) {
        if (images.length === 0) return;
        
        images.forEach((img, i) => {
            img.style.opacity = i === index ? "1" : "0";
            img.style.transform = i === index ? "scale(1)" : "scale(0.9)";
            img.style.transition = "opacity 0.5s ease-in-out, transform 0.5s ease-in-out";
            img.style.display = i === index ? "block" : "none";
        });
    }

    if (images.length > 0) {
        updateSlider(currentIndex);
    }

    prevButton.addEventListener("click", function () {
        if (currentIndex > 0) {
            currentIndex--;
            updateSlider(currentIndex);
        }
    });

    nextButton.addEventListener("click", function () {
        if (currentIndex < images.length - 1) {
            currentIndex++;
            updateSlider(currentIndex);
        }
    });
});

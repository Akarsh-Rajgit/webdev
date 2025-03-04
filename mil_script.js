 let images = document.querySelectorAll(".gallery img");
        let lightbox = document.getElementById("lightbox");
        let lightboxImg = document.getElementById("lightbox-img");
        let currentIndex = 0;

        // Open Lightbox
        function openLightbox(index) {
            currentIndex = index;
            lightboxImg.src = images[currentIndex].src;
            lightbox.classList.add("active");
        }

        // Close Lightbox
        function closeLightbox() {
            lightbox.classList.remove("active");
        }

        // Previous Image
        function prevImage() {
            currentIndex = (currentIndex - 1 + images.length) % images.length;
            lightboxImg.src = images[currentIndex].src;
        }

        // Next Image
        function nextImage() {
            currentIndex = (currentIndex + 1) % images.length;
            lightboxImg.src = images[currentIndex].src;
        }

        // Add click event to all images
        images.forEach((img, index) => {
            img.addEventListener("click", () => openLightbox(index));
        });

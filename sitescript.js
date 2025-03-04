function toggleImage(event) {
            let img = event.currentTarget.querySelector(".service-img");
            if (img) {
                img.style.display = img.style.display === "block" ? "none" : "block";
            }
        }

// VibrocomX Global Scripts

// === Lightbox / Image Zoom ===
(function() {
    // Create lightbox overlay element
    var overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';
    overlay.innerHTML = '<button class="lightbox-close" aria-label="Close zoom"><i class="fas fa-times"></i></button><img src="" alt="Zoomed image">';
    document.body.appendChild(overlay);

    var lightboxImg = overlay.querySelector('img');
    var closeBtn = overlay.querySelector('.lightbox-close');

    function openLightbox(src, alt) {
        lightboxImg.src = src;
        lightboxImg.alt = alt || 'Zoomed image';
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        closeLightbox();
    });

    overlay.addEventListener('click', function(e) {
        if (e.target === overlay || e.target === lightboxImg) {
            closeLightbox();
        }
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeLightbox();
    });

    // Make all .zoomable-image elements clickable
    document.addEventListener('click', function(e) {
        var zoomable = e.target.closest('.zoomable-image');
        if (zoomable) {
            var img = zoomable.querySelector('img');
            if (img) {
                e.preventDefault();
                openLightbox(img.src, img.alt);
            }
        }
    });

    // Also make prose images zoomable (article body images)
    var proseImages = document.querySelectorAll('.prose img');
    for (var i = 0; i < proseImages.length; i++) {
        proseImages[i].style.cursor = 'zoom-in';
        proseImages[i].addEventListener('click', function() {
            openLightbox(this.src, this.alt);
        });
    }
})();

// === Download / Print Article as PDF ===
function downloadArticle() {
    window.print();
}

// === Cartoon Upload Drag & Drop Enhancement ===
(function() {
    var dropZone = document.querySelector('.cartoon-upload-form');
    if (!dropZone) return;

    var fileInput = dropZone.querySelector('input[type="file"]');

    ['dragenter', 'dragover'].forEach(function(eventName) {
        dropZone.addEventListener(eventName, function(e) {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(function(eventName) {
        dropZone.addEventListener(eventName, function(e) {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
        });
    });

    dropZone.addEventListener('drop', function(e) {
        if (fileInput && e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            var nameDisplay = dropZone.querySelector('.file-name-display');
            if (nameDisplay) {
                nameDisplay.textContent = e.dataTransfer.files[0].name;
            }
        }
    });
})();

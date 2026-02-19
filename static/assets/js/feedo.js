(function() {
	"use strict";

    // Preloader JS
    try {
        window.addEventListener('load', function() {
            var preloader = document.getElementById('preloader');
            preloader.classList.add('d-none');
        });
    } catch (err) {}


    // Check if elements with the class "search-toggler" exist
    const searchTogglers = document.querySelectorAll(".search-toggler");
    if (searchTogglers.length > 0) {
        searchTogglers.forEach((searchToggler) => {
            searchToggler.addEventListener("click", function (e) {
            e.preventDefault();
            
                const searchPopup = document.querySelector(".search-popup");
                if (searchPopup) {
                    searchPopup.classList.toggle("active");
                }

                const mobileNavWrapper = document.querySelector(".mobile-nav-wrapper");
                if (mobileNavWrapper) {
                    mobileNavWrapper.classList.remove("expanded");
                }
            });
        });
    }

    window.onload = function() {

        // Scroll Event go Top JS
        try {
            window.addEventListener('scroll', function() {
                var scrolled = window.scrollY;
                var goTopButton = document.querySelector('.go-top');
    
                if (scrolled > 600) {
                    goTopButton.classList.add('active');
                } else {
                    goTopButton.classList.remove('active');
                }
            });
            var goTopButton = document.querySelector('.go-top');
            goTopButton.addEventListener('click', function() {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        } catch (err) {}

        // Counter Js
        try {
            if ("IntersectionObserver" in window) {
                let counterObserver = new IntersectionObserver(function (entries, observer) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                        let counter = entry.target;
                        let target = parseInt(counter.innerText);
                        let step = target / 200;
                        let current = 0;
                        let timer = setInterval(function () {
                            current += step;
                            counter.innerText = Math.floor(current);
                            if (parseInt(counter.innerText) >= target) {
                            clearInterval(timer);
                            }
                        }, 10);
                        counterObserver.unobserve(counter);
                        }
                    });
                });

                let counters = document.querySelectorAll(".counter");
                    counters.forEach(function (counter) {
                    counterObserver.observe(counter);
                });
            }
        } catch (err) {}

        // Hover JS
        try {
            var elements = document.querySelectorAll("[id^='my-element']");
                elements.forEach(function(element) {
                element.addEventListener("mouseover", function() {
                    elements.forEach(function(el) {
                    el.classList.remove("active");
                    });
                    element.classList.add("active");
                });
            });

        } catch (err) {}

    };
    
    // PortFolio Slider JS
    try {
        window.addEventListener('DOMContentLoaded', () => {
            const slides = document.querySelectorAll('.slide');
        
            slides.forEach(slide => {
                slide.addEventListener('mouseover', () => {
                    clearActiveClasses();
                    slide.classList.add('active');
                });
        
                slide.addEventListener('mouseout', () => {
                    slide.classList.remove('active');
                });
            });
        
            function clearActiveClasses() {
                slides.forEach(slide => {
                    slide.classList.remove('active');
                });
            }
        });
    } catch (err) {}

    // Subscribe JS
    try {
        document.querySelector('.email-form').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting the traditional way
        
            const emailInput = document.getElementById('emailInput');
            const messageDiv = document.getElementById('message');
            const email = emailInput.value.trim();
        
            // Simple email validation
            if (!email || !validateEmail(email)) {
                messageDiv.textContent = 'Please enter a valid email address.';
                messageDiv.style.color = 'red';
                return;
            }
        
            // Simulate sending the email to a server (you can replace this with an actual API call)
            setTimeout(() => {
                messageDiv.textContent = 'Thank you for subscribing!';
                messageDiv.style.color = 'green';
                emailInput.value = ''; // Clear the input field
            }, 1000);
        });

        // Function to validate email format
        function validateEmail(email) {
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return regex.test(email);
        }
    } catch (err) {}

    // Award JS
    try {
        document.addEventListener('DOMContentLoaded', () => {
            const serviceItems = document.querySelectorAll('.service-item');
            const serviceImage = document.getElementById('service-image');
    
            serviceItems.forEach((item) => {
                item.addEventListener('mouseenter', () => {
                    const newImage = item.getAttribute('data-image');
                    serviceImage.src = newImage;
                });
            });
        });
    } catch (err) {}

    // Category JS
    var swiper = new Swiper(".categorySlider", {
        slidesPerView: 1,
        spaceBetween: 25,
        loop: true,
        speed: 1500,
        autoplay: {
            delay: 2000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },
        breakpoints: {
            0: {
                slidesPerView: 1
            },
            576: {
                slidesPerView: 1
            },
            768: {
                slidesPerView: 2
            },
            992: {
                slidesPerView: 4
            },
            1200: {
                slidesPerView: 5
            },
            1400: {
                slidesPerView: 5
            }
        }
    });
    
    // Testimoni JS
    var swiper = new Swiper(".testimoniSlider", {
        slidesPerView: 1,
        spaceBetween: 25,
        loop: true,
        speed: 1500,
        autoplay: {
            delay: 2000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
    });
    
    // Testimoni JS
    var swiper = new Swiper(".sellingSlider", {
        slidesPerView: 1,
        spaceBetween: 20,
        loop: true,
        speed: 1500,
        autoplay: {
            delay: 2000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        breakpoints: {
            0: {
                slidesPerView: 1
            },
            576: {
                slidesPerView: 4
            },
            768: {
                slidesPerView: 2
            },
            992: {
                slidesPerView: 2
            },
            1200: {
                slidesPerView: 3
            },
            1400: {
                slidesPerView: 4
            },
            1600: {
                slidesPerView: 5
            },
        }
    });

    // Clients JS
    var swiper = new Swiper(".clientsSlider", {
        slidesPerView: 1,
        spaceBetween: 25,
        loop: true,
        speed: 1500,
        autoplay: {
            delay: 2000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },
        pagination: {
            clickable: true,
            el: ".swiper-pagination",
        },
    });
    
    // Banner JS
    var swiper = new Swiper(".bannerSlider", {
        slidesPerView: 1,
        spaceBetween: 25,
        loop: true,
        speed: 1500,
        autoplay: {
            delay: 2000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },
        pagination: {
            clickable: true,
            el: ".swiper-pagination",
        },
    });

    // Banner JS
    var swiper = new Swiper(".bannerSlider1", {
        slidesPerView: 1,
        spaceBetween: 25,
        loop: true,
        speed: 1500,
        autoplay: {
            delay: 2000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },
        pagination: {
            clickable: true,
            el: ".swiper-pagination",
        },
    });

    // Partner JS
    var swiper = new Swiper(".partnerSlider", {
        slidesPerView: 1,
        spaceBetween: 20,
        loop: true,
        speed: 1500,
        autoplay: {
            delay: 2000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },
        breakpoints: {
            0: {
                slidesPerView: 1
            },
            576: {
                slidesPerView: 4
            },
            768: {
                slidesPerView: 5
            },
            992: {
                slidesPerView: 6
            },
            1200: {
                slidesPerView: 7
            },
            1400: {
                slidesPerView: 8
            }
        }
    });

    // scrollCue
    scrollCue.init();
})();

// Quantities JS
document.addEventListener('DOMContentLoaded', function () {
    try {
        const quantitySelectors = document.querySelectorAll('.quantity-selector');
    
        if (!quantitySelectors || quantitySelectors.length === 0) {
            console.warn('No .quantity-selector elements found.');
            return;
        }
    
        quantitySelectors.forEach(selector => {
            try {
                const quantityInput = selector.querySelector('input[type="number"]');
                const decrementButton = selector.querySelector('.decrement');
                const incrementButton = selector.querySelector('.increment');
            
                if (!quantityInput) {
                    console.warn('Missing quantity input in:', selector);
                    return;
                }
                if (!decrementButton) {
                    console.warn('Missing decrement button in:', selector);
                }
                if (!incrementButton) {
                    console.warn('Missing increment button in:', selector);
                }
            
                // Set default value if empty or invalid
                if (!quantityInput.value || isNaN(quantityInput.value)) {
                    quantityInput.value = 1;
                }
            
                // Ensure min value is respected
                const minValue = parseInt(quantityInput.min) || 1;
            
                if (decrementButton) {
                    decrementButton.addEventListener('click', function () {
                        let currentValue = parseInt(quantityInput.value, 10) || minValue;
                        quantityInput.value = Math.max(minValue, currentValue - 1);
                        quantityInput.dispatchEvent(new Event('change'));
                    });
                }
            
                if (incrementButton) {
                    incrementButton.addEventListener('click', function () {
                        let currentValue = parseInt(quantityInput.value, 10) || minValue;
                        const maxValue = parseInt(quantityInput.max) || Infinity;
                        quantityInput.value = Math.min(maxValue, currentValue + 1);
                        quantityInput.dispatchEvent(new Event('change'));
                    });
                }
            
                // Validate input
                quantityInput.addEventListener('input', function () {
                    this.value = this.value.replace(/[^0-9]/g, '');
                    
                    // Ensure value stays within bounds
                    const numValue = parseInt(this.value) || minValue;
                    const maxValue = parseInt(this.max) || Infinity;
                    
                    if (numValue < minValue) {
                        this.value = minValue;
                    } else if (numValue > maxValue) {
                        this.value = maxValue;
                    }
                });
            
                // Handle blur event in case user leaves empty
                quantityInput.addEventListener('blur', function() {
                    if (!this.value || isNaN(this.value)) {
                        this.value = minValue;
                    }
                });
            } catch (innerError) {
                console.error('Error initializing quantity selector:', selector, innerError);
            }
        });
    } catch (outerError) {
        console.error('Error in quantity selector initialization:', outerError);
    }
});

// For Mobile Navbar JS
const list = document.querySelectorAll('.mobile-menu-list');
function accordion(e) {
    e.stopPropagation(); 
    if(this.classList.contains('active')){
        this.classList.remove('active');
    }
    else if(this.parentElement.parentElement.classList.contains('active')){
        this.classList.add('active');
    }
    else {
        for(i=0; i < list.length; i++){
            list[i].classList.remove('active');
        }
        this.classList.add('active');
    }
}
for(i = 0; i < list.length; i++ ){
    list[i].addEventListener('click', accordion);
}

// Header Sticky
const getHeaderId = document.getElementById("navbar");
if (getHeaderId) {
    window.addEventListener('scroll', event => {
        const height = 150;
        const { scrollTop } = event.target.scrollingElement;
        document.querySelector('#navbar').classList.toggle('sticky', scrollTop >= height);
    });
}


function toggleHamburger(element) {
  const hamburger = element.querySelector('.hamburger-animated');
  hamburger.classList.toggle('open');

  const isHamburgerVisible = $('.navbar-toggler').is(':visible');
  const isScrolledLessThan50 = $(document).scrollTop() < 50;

  // Check if menu is now open (after toggle)
  const isMenuOpen = hamburger.classList.contains('open');

  if (isHamburgerVisible && isScrolledLessThan50 && isMenuOpen) {
      $('.mainNav').addClass('hamburgerclicked');
  } else {
      $('.mainNav').removeClass('hamburgerclicked');
  }
}

$(document).ready(function () {

  // 1. AOS Initialization
  AOS.init({
      duration: 1000,
      once: true,
  });

  // 2. Navbar Shrink on Scroll
  $(window).scroll(function () {
      if ($(document).scrollTop() > 50) {
          $('.mainNav').addClass('scrolled');
      } else {
          $('.mainNav').removeClass('scrolled');
      }
  });

  // 3. Smooth Scrolling for Nav Links
  $('.nav-link').on('click', function (event) {
      if (this.hash !== "") {
          // Prevent default anchor click behavior
          event.preventDefault();
          var hash = this.hash;
          $('html, body').animate({
              scrollTop: $(hash).offset().top - 70 // Adjust for fixed navbar height
          }, 800, function () {
              // window.location.hash = hash; // This line can be distracting
          });
      }
  });

  // 4. Countdown Timer - Dynamic from Django context
  function startCountdown() {
      // Check if the global variable countDownDate exists and is valid
      if (typeof countDownDate !== 'undefined' && !isNaN(countDownDate) && countDownDate > 0) {
          // Update the count down every 1 second
          var x = setInterval(function () {
              var now = new Date().getTime();
              var distance = countDownDate - now;

              // If countdown is finished
              if (distance < 0) {
                  clearInterval(x);
                  $('.countdown-container').html("<h2 style='color: white;'>The Wedding Day is Here!</h2>");
                  return;
              }

              // Time calculations for days, hours, minutes and seconds
              var days = Math.floor(distance / (1000 * 60 * 60 * 24));
              var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
              var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
              var seconds = Math.floor((distance % (1000 * 60)) / 1000);

              // Display the result in the respective elements
              $('#days').html(Math.max(0, days));
              $('#hours').html(Math.max(0, hours));
              $('#minutes').html(Math.max(0, minutes));
              $('#seconds').html(Math.max(0, seconds));
          }, 1000);
      } else {
          console.log('No upcoming event date found');
          $('.countdown-container').html("<h2 style='color: white;'>Check back soon for event details!</h2>");
      }
  }
  
  // Initialize countdown
  startCountdown();

  // 5. Wedding Party Slider (Swiper JS)
  $(function () {
      $('.wedding-party-slider').each(function () {
          new Swiper(this, {
              loop: true,
              slidesPerView: 1,
              spaceBetween: 30,
              pagination: {
                  el: $(this).find('.swiper-pagination')[0],
                  clickable: true
              },
              breakpoints: {
                  640: { slidesPerView: 2, spaceBetween: 20 },
                  768: { slidesPerView: 3, spaceBetween: 40 },
                  1024: { slidesPerView: 4, spaceBetween: 50 }
              }
          });
      });
  });

  // 6. Lightbox2 Initialization
  if (typeof lightbox !== "undefined") {
      lightbox.option({
          resizeDuration: 200,
          wrapAround: true,
          disableScrolling: true
      });
  }
});

window.addEventListener('load', function () {
  const loader = document.getElementById('loader');
  const body = document.body;
  setTimeout(() => {
      if (loader) {
          loader.classList.add('loader-hidden');
          body.classList.remove('loading');
      }
  }, 2500);
});
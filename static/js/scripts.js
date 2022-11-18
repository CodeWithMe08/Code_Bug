// Scripts


window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }
    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 72,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });
});


/*animations and transitions*/
gsap.registerPlugin(ScrollTrigger);
var tl = gsap.timeline();
tl.from('.wrapper', {
    y: '-200%',
    opacity: 0,
    duration: 0.7,
    ease: Power4.easeOut
})
tl.from('.linky', {
    opacity: 0,
    y: -50,
    stagger: .3,
    ease: Power4.easeOut,
    duration: 1.3
}, "-=1.5")

gsap.from(".transition2", {
    scrollTrigger: {
        trigger: '.transition2',
        start: "top bottom"
    },
    y: 100,
    opacity: 0,
    duration: 0.7,
    stagger: .3
})

gsap.from(".transition3", {
    scrollTrigger: {
        trigger: ".transition3",
        start: "top bottom"
    },
    y: 100,
    opacity: 0,
    duration: 1.1,
    stagger: .3
})
gsap.from(".transition4", {
    scrollTrigger: {
        trigger: ".transition4",
        start: "top center"
    },
    y: 50,
    opacity: 0,
    duration: 0.7,
    stagger: .3
})
gsap.from(".transition5", {
    scrollTrigger: {
        trigger: ".transition5",
        start: "center bottom"
    },
    y: 50,
    opacity: 0,
    duration: 0.7,
    stagger: .3
});

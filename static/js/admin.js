/*animations and transitions*/
gsap.registerPlugin(ScrollTrigger);
var tl = gsap.timeline();
tl.from('.wrapper', {
    y: '50%',
    opacity: 0,
    duration: 0.5,
    ease: Power4.easeOut
})
tl.from('.transition6', {
    opacity: 0,
    y: -50,
    stagger: .3,
    ease: Power4.easeOut,
    duration: 1.3
}, "-=1.5")

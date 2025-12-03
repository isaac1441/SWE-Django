const menu = document.querySelector('.post-form');
const button = document.getElementsByClassName('.menu-toggle');

button.addEventListener('click', () => {
    console.log("test");
  menu.classList.toggle('hidden');
});

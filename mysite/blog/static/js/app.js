document.addEventListener('DOMContentLoaded', function() {
    const mobileListTrigger = document.getElementById('mobile-list-trigger');
    const activePlusDropUp = document.getElementById('activePlusDropUp');
    if (mobileListTrigger && activePlusDropUp) {
        mobileListTrigger.addEventListener('click', () => {
            console.log('clicked agin')

            activePlusDropUp.classList.toggle('activePlusTrigger');
            const plusIcon = mobileListTrigger.querySelector('i');
            plusIcon.classList.toggle('fa-plus');
            plusIcon.classList.toggle('fa-minus');
        });
    }
});


function goBack() {
    window.history.back();
}


let collapsebtn = document.getElementById('collapse');
let collapse_body = document.getElementById('collapse-body');

collapsebtn.addEventListener('click', () => {
    collapse_body.style.display = 'block'
})


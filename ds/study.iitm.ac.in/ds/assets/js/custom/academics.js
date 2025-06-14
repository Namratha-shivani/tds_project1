function setGoal(slction) {
    goalFilePath = [
        "", "assets/pdf/Goal_Foundational_Certificate.pdf", "assets/pdf/Goal_Diploma_in_Programming.pdf", 
        "assets/pdf/Goal_Diploma_in_Data_Science.pdf", "assets/pdf/Goal_Both_Diplomas.pdf", "assets/pdf/Goal_BSc_Degree.pdf"
    ]
    selectedGoal = slction.selectedIndex;
    document.getElementById('goal').innerHTML = ('<iframe src="' + goalFilePath[selectedGoal] + '" width=100% height=400px></iframe>');
}

// Handling alignment
let scrollButton = document.getElementById('scrollToTop');

// Add Custom Margin for the main content
// window.addEventListener('DOMContentLoaded', function () {
//     let fixed = document.getElementById("fixedTop");
//     const marginTop = window.getComputedStyle(fixed).getPropertyValue("height");
//     let styles = `
//     p:target::before {
//         content: "";
//     display: block;
//     height: ${marginTop}; /* fixed header height*/
//     margin: -${marginTop} 0 0; /* negative fixed header height */
//                 }
//     h2:target::before {
//         content: "";
//     display: block;
//     height: ${marginTop}; /* fixed header height*/
//     margin: -${marginTop} 0 0; /* negative fixed header height */
//                 }
//     div:target::before {
//         content: "";
//     display: block;
//     height: ${marginTop}; /* fixed header height*/
//     margin: -${marginTop} 0 0; /* negative fixed header height */
//                 }
//     `
//     document.getElementById("mainContent").style.marginTop = marginTop;
//     let styleSheet = document.createElement("style")
//     styleSheet.type = "text/css"
//     styleSheet.innerText = styles
//     document.head.appendChild(styleSheet);
// })
window.onload = function () {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        scrollButton.style.display = "block";
    } else {
        scrollButton.style.display = "none";
    }
    weekShow();
}
window.onresize = function () {
    let fixed = document.getElementById("fixedTop");
    const marginTop = window.getComputedStyle(fixed).getPropertyValue("height");
    let styles = `
    p:target::before {
        content: "";
    display: block;
    height: ${marginTop}; /* fixed header height*/
    margin: -${marginTop} 0 0; /* negative fixed header height */
                }
    h2:target::before {
        content: "";
    display: block;
    height: ${marginTop}; /* fixed header height*/
    margin: -${marginTop} 0 0; /* negative fixed header height */
                }`
    document.getElementById("mainContent").style.marginTop = marginTop;
    let styleSheet = document.createElement("style")
    styleSheet.type = "text/css"
    styleSheet.innerText = styles
    document.head.appendChild(styleSheet)
}
// Checking if to show scroll to top button
window.onscroll = function () {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        scrollButton.style.display = "block";
    } else {
        scrollButton.style.display = "none";
    }
}
function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
// adding data-url to all tr
let rows = document.getElementsByTagName('tr'), url;
for (let i = 0; i < rows.length; i++) {
    rows[i].onclick = function () {
        if (this.getAttribute('data-url'))
            window.location = this.getAttribute('data-url');
    }
}
let tableData = document.getElementsByTagName('td');
for (let i = 0; i < tableData.length; i++) {
    tableData[i].onclick = function () {
        if (this.getAttribute('data-url'))
            window.location = this.getAttribute('data-url');
    }
}

// footer links navigation
let footerLinks = document.getElementsByClassName('footerLinks');
for (let i = 0; i < footerLinks.length; i++) {
    footerLinks[i].addEventListener('click', function () {
        window.location = this.getAttribute('url');
    })
}
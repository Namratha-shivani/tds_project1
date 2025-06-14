let scrollButton = document.getElementById('scrollToTop');
window.addEventListener('DOMContentLoaded', function () {
    // let fixed = document.getElementById("fixedTop");
    // const marginTop = window.getComputedStyle(fixed).getPropertyValue("height");
    // let styles = `
    //     p:target::before {
    //         content: "";
    //           display: block;
    //           height: ${marginTop}; /* fixed header height*/
    //           margin: -${marginTop} 0 0; /* negative fixed header height */
    //     }
    //     div:target::before {
    //         content: "";
    //           display: block;
    //           height: ${marginTop}; /* fixed header height*/
    //           margin: -${marginTop} 0 0; /* negative fixed header height */
    //     }
    //     `
    // document.getElementById("mainContent").style.marginTop = marginTop;
    // let styleSheet = document.createElement("style");
    // styleSheet.type = "text/css";
    // styleSheet.innerText = styles;
    // document.head.appendChild(styleSheet);
    let faqs = document.getElementsByClassName('faqExpand');
    for (let i = 0; i < faqs.length; i++) {
        faqs[i].addEventListener('click', function () {
            let content = this.nextElementSibling;
            this.getElementsByClassName('expandMore')[0].classList.toggle('d-none');
            this.getElementsByClassName('expandMore')[1].classList.toggle('d-none');
            this.getElementsByClassName('expandLess')[0].classList.toggle('d-none');
            this.getElementsByClassName('expandLess')[1].classList.toggle('d-none');
            for (let j = 0; j < faqs.length; j++) {
                if (j != i) {
                    let content = faqs[j].nextElementSibling;
                    if (content.style.maxHeight) {
                        faqs[j].getElementsByClassName('expandMore')[0].classList.toggle('d-none');
                        faqs[j].getElementsByClassName('expandMore')[1].classList.toggle('d-none');
                        faqs[j].getElementsByClassName('expandLess')[0].classList.toggle('d-none');
                        faqs[j].getElementsByClassName('expandLess')[1].classList.toggle('d-none');
                        content.style.maxHeight = null;
                        content.style.marginTop = 0;
                    }
                }
            }
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                content.style.marginTop = 0;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                content.style.marginTop = '1rem';
            }
        });
    }
})
// Add Custom Margin for the main content
window.onload = function () {
    if (window.location.href.split('#')[1]) {
        let faqObject = document.getElementById(`${window.location.href.split('#')[1]}`);
        faqObject.getElementsByClassName('faqExpand')[0].click();
    }
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        scrollButton.style.display = "block";
    } else {
        scrollButton.style.display = "none";
    }

}

// adding  marginTop to anchor elements
// window.onresize = function () {
//     let fixed = document.getElementById("fixedTop");
//     const marginTop = window.getComputedStyle(fixed).getPropertyValue("height");
//     let styles = `
//         p:target::before {
//             content: "";
//               display: block;
//               height: ${marginTop}; /* fixed header height*/
//               margin: -${marginTop} 0 0; /* negative fixed header height */
//         }
//         div:target::before {
//             content: "";
//               display: block;
//               height: ${marginTop}; /* fixed header height*/
//               margin: -${marginTop} 0 0; /* negative fixed header height */
//         }
//         `
//     document.getElementById("mainContent").style.marginTop = marginTop;
//     let styleSheet = document.createElement("style")
//     styleSheet.type = "text/css"
//     styleSheet.innerText = styles
//     document.head.appendChild(styleSheet)
// }

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

function copyToClipboard(url) {
    let dummy = document.createElement("textarea");
    document.body.appendChild(dummy);
    dummy.value = url;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);
    alert('copied!');
}

function showTag(tag) {
    let tags = document.getElementsByClassName('tags');
    let contents = document.getElementsByClassName('contents');
    for (let i = 0; i < tags.length; i++) {
        tags[i].classList.remove('badge-primary');
        tags[i].classList.add('badge-light');
        contents[i].classList.add('d-none');
        contents[i].classList.add('d-none');
    }
    document.getElementById(`${tag}-tag`).classList.remove('badge-light');
    document.getElementById(`${tag}-tag`).classList.add('badge-primary');
    document.getElementById(`${tag}`).classList.remove('d-none');
}

// footer links navigation
let footerLinks = document.getElementsByClassName('footerLinks');
for (let i = 0; i < footerLinks.length; i++) {
    footerLinks[i].addEventListener('click', function () {
        window.location = this.getAttribute('url');
    })
}
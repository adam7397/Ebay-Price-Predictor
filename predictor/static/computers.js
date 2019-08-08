document.addEventListener('DOMContentLoaded', () => {

    console.log("loaded");

    document.querySelector('#search_button').disabled = true;

    document.querySelector('#search_term').onkeyup = () => {
        if (document.querySelector('#search_term').value.length > 0)
            document.querySelector('#search_button').disabled = false;
        else
            document.querySelector('#search_button').disabled = true;
    };
});

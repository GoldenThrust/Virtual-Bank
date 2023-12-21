export function postData(url, form, reload = false) {
    const csrftoken = getCookie('csrftoken');
    let status = null;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: form
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (reload) window.location.reload();
            }
            status = data;
        })

    return status;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}
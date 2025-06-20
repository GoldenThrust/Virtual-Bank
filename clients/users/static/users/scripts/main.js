export async function postData(url, form, reload = false, external = false) {
    let response = null;
    const csrftoken = getCookie('csrftoken');

    const options = {
        method: 'POST',
        body: form,
        credentials: 'include'
    };    if (external) {
        const BASE_URL = window.API_BASE_URL || 'http://localhost:8030';
        url = `${BASE_URL}${url}`;
    } else {
        options.headers = {
            'X-CSRFToken': csrftoken
        };
    }

    try {
        response = await fetch(url, options);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (reload) {
            window.location.reload();
        } else {
            // console.log("Response data:", data);
        }

        return data;
    } catch (err) {
        console.error('Error:', err);
        return err;
    }
}

export async function getData(url, external = false) {
    let response = null;
    const csrftoken = getCookie('csrftoken');    const options = {
        method: 'GET',
        credentials: 'include'
    };

    if (external) {
        const BASE_URL = window.API_BASE_URL || 'http://localhost:8030';
        url = `${BASE_URL}${url}`;
    } else {
        options.headers = {
            'X-CSRFToken': csrftoken
        };
    }

    try {
        response = await fetch(url, options);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (err) {
        console.error('Error:', err);
        return err;
    }
}

export const currency_mapping = {
    USD: "$",   // US Dollar
    EUR: "€",  // Euro
    GBP: "£",  // British Pound
    NGN: "₦", // Nigerian Naira
    JPY: "¥", // Japanese Yen
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



export function createElement(
    parent,
    elem,
    attribute = {},
    content = null,
    prepend = false
) {
    const element = document.createElement(elem);
    if (content) {
        element.innerText = content;
    }

    if (attribute) {
        for (const key in attribute) {
            element.setAttribute(key, attribute[key]);
        }
    }

    if (prepend) {
        parent.prepend(element)
    } else {
        parent.appendChild(element);
    }

    return element;
}